#!/usr/bin/env python3
import os
import sys
import json
import getpass
import argparse
import difflib
import subprocess
import datetime
import yaml
from .model_calls import generic_call
from .pydift_tui import tui


def call_llm_for_summary(diff_text):
    """
    Call the LLM to generate a summary of the diff.

    Args:
        diff_text (str): The unified diff text.

    Returns:
        str: The summary of the diff
    """
    prompt = f"""
The following is the diff generated from a new version of a code file. If there are changes to scalar parameters, changes in choices of functions (such as loss functions) or changes in status of flags - note them first before any other change. Summarize the diff succinctly and accurately:
{diff_text}
"""    
    return generic_call(prompt, model)

# --------------------------------------------------------------------
# Main pydift code
# --------------------------------------------------------------------
def main():
    """
    Main entry point for pydift.

    This script is a simple version-tracking tool for research code development.

    Usage:
        pydift.py script.py
        pydift.py script.py --summary # Send the diff to an LLM for a summary.
        pydift.py script.py --wide   # Track all files in the current directory.
        pydift.py script.py --recursive  # Track all files in the current directory and subdirectories.
        pydift.py --tui  # Launch the pydift TUI.
    """
    # pydift conf should be in hidden folder in the user directory
    conf_path = os.path.join(os.path.expanduser("~"), ".pydift")
    # make sure the conf folder exists
    if not os.path.exists(conf_path):
        os.makedirs(conf_path)
    # make sure the conf file exists
    conf_file_path = os.path.join(conf_path, "pydift_conf.yaml")
    if not os.path.exists(conf_file_path):
        default_config = {
            "model": "Meta Llama 3.3",
            "summary": False,
            "wide": False,
            "recursive": False,
        }
        with open(conf_file_path, "w") as f:
            yaml.dump(default_config, f)
    global conf
    global model
    conf = yaml.safe_load(open(conf_file_path, "r"))
    model = conf["model"]

    # if no arguments, run tui with cwd
    if len(sys.argv) == 1:
        tui(os.getcwd())
        return
    
    parser = argparse.ArgumentParser(
        description="A simple version-tracking tool for research code development."
    )
    parser.add_argument("-p", "--path", dest="script_path", 
                        help="The script to run and track.")
    parser.add_argument("-s", "--summary", action="store_true", 
                        help="If set, send the diff to an LLM for a summary.")
    parser.add_argument("-w", "--wide", action="store_true", 
                        help="If set, track all files in the current directory.")
    parser.add_argument("-r", "--recursive", action="store_true", 
                        help="If set, track all files in the current directory and subdirectories (supercedes '-w,--wide').")
    parser.add_argument("-t", "--tui", action="store_true", 
                        help="If set, launch the pydift TUI.")
    args, unknown_args = parser.parse_known_args()
    script_to_run = args.script_path
    
    # check if script_path is empty, then path is in unknown args
    if not args.script_path:
        script_to_run = unknown_args[0]
        unknown_args = unknown_args[1:]

    # working dir is the directory of the script to run if given, else cwd
    if os.path.isdir(script_to_run): # if script_path is a directory
        wd = script_to_run
        args.tui = True
    elif script_to_run:
        wd = os.path.dirname(script_to_run)
    else:
        wd = os.getcwd()
    # If TUI is requested, launch it
    if args.tui:
        tui(wd)
        return

    generate_summary = args.summary

    # Ensure .pydift folder structure exists
    pydift_dir = os.path.join(wd, ".pydift")
    versions_dir = os.path.join(pydift_dir, "versions")
    diffs_file = os.path.join(pydift_dir, "diffs.jsonl")

    if not os.path.exists(pydift_dir):
        os.makedirs(pydift_dir)
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)

    # Take from conf if not given as arguments
    if not args.summary:
        generate_summary = conf["summary"]
    if not args.wide and not args.recursive:
        args.wide = conf["wide"]
    if not args.recursive:
        args.recursive = conf["recursive"]
    
    # Find relevant files to track
    if args.recursive:
        tracked_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(".py"):
                    tracked_files.append(os.path.relpath(os.path.join(root, file)))
    elif args.wide:
        tracked_files = [f for f in os.listdir('.') if f.endswith(".py") and os.path.isfile(f)]
    else:
        tracked_files = [script_to_run]

    # Check if there is an existing snapshot (do we have any files in versions_dir?)
    first_run = True
    for f in tracked_files:
        if os.path.exists(os.path.join(versions_dir, f)):
            first_run = False
            break

    # If not the first run, generate a diff
    diff_full = ""
    if not first_run:
        for f in tracked_files:
            old_version_path = os.path.join(versions_dir, f)
            if os.path.exists(old_version_path):
                with open(old_version_path, 'r', encoding='utf-8') as old_f:
                    old_content = old_f.readlines()
            else:
                old_content = []

            with open(f, 'r', encoding='utf-8') as new_f:
                new_content = new_f.readlines()

            # Generate unified diff (similar to git diff)
            diff = difflib.unified_diff(
                old_content,
                new_content,
                fromfile=f"old/{f}",
                tofile=f"new/{f}"
            )
            # Accumulate into a single big diff
            diff_text = "".join(diff)
            diff_full += diff_text

    # Create the log entry
    log_entry = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "user": getpass.getuser(),
        "script": script_to_run,
    }

    if first_run:
        # No diffs on first run
        diff_full = "No previous version found. First run."
        log_entry["diff_full"] = diff_full
        log_entry["diff_summary"] = "No changes logged (first run)."
    else:
        # Potentially call LLM for summary if requested
        if generate_summary and diff_full != "":
            summary_text = call_llm_for_summary(diff_full)
            log_entry["diff_summary"] = summary_text
        else:
            # Just store a placeholder or empty
            log_entry["diff_summary"] = "No summary requested."
        if diff_full == "":
            log_entry["diff_full"] = "No changes logged."
        else:
            log_entry["diff_full"] = diff_full

    # Append the log entry to diffs.jsonl
    with open(diffs_file, 'a', encoding='utf-8') as df:
        df.write(json.dumps(log_entry) + "\n")

    # Update the stored versions with current files
    for f in tracked_files:
        # make sure the path exists
        curr_f_path = os.path.join(versions_dir, f)
        if not os.path.exists(os.path.dirname(curr_f_path)):
            os.makedirs(os.path.dirname(curr_f_path))
        with open(f, 'rb') as src, open(curr_f_path, 'wb') as dst:
            dst.write(src.read())

    # Run the script via python
    #    Pass along any extra arguments to the script if needed (unknown_args).
    #    For example: pydift script.py --summary -- some_arg --some_option
    #    We pass `unknown_args` after script_to_run.
    command = [sys.executable, script_to_run] + unknown_args

    # Now execute:
    completed_proc = subprocess.run(command)
    # You can choose to relay the return code from the script:
    sys.exit(completed_proc.returncode)

if __name__ == "__main__":
    main()

