import json, yaml
import os
import difflib
from InquirerPy import inquirer
from .model_calls import available_calls

red = lambda text: f"\033[38;2;235;20;20m{text}\033[38;2;255;255;255m"
green = lambda text: f"\033[38;2;20;235;20m{text}\033[38;2;255;255;255m"
blue = lambda text: f"\033[94m{text}\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_diffs(ppath, log_path=".pydift/diffs.jsonl"):
    full_log_path = os.path.join(ppath, log_path)
    if not os.path.exists(full_log_path):
        return []
    entries = []
    with open(full_log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except:
                pass
    return entries

def reconstruct_code(diff_entry, ppath, versions_dir=".pydift/versions"):
    """
    Given a diff timestamp, create a new script file with the
    same name plus a timestamp suffix, and apply all recorded
    diffs up to that timestamp to reconstruct the code.
    """
    script_name = diff_entry["script"]
    target_timestamp = diff_entry["timestamp"]
    all_diffs = load_diffs(ppath)
    # Filter diffs for this script up to the chosen timestamp
    applicable = [
        d for d in all_diffs
        if d.get("script") == script_name and d.get("timestamp") <= target_timestamp
    ]
    # Sort them chronologically
    applicable.sort(key=lambda x: x["timestamp"])
    # Start with empty code or a baseline if needed
    code_lines = []
    # Apply each stored diff in order
    for record in applicable:
        patch_text = record.get("diff_full", "")
        # Assume 'diff_full' is a unified diff; restore new code from patch
        patch = difflib.unified_diff(code_lines, [], lineterm="")
        # 'patch_text' might need to be combined with 'patch' lines if partial
        # For simplicity, this just sets 'code_lines' to the last known version
        # If your diffs are complete, you can replace this logic with actual patch apply
        patch_lines = patch_text.splitlines()
        code_lines = patch_lines if patch_lines else code_lines
    # Write out the reconstructed code with a timestamp suffix
    suffix = f"_{target_timestamp}"
    base, ext = script_name.rsplit(".", 1)
    new_file = f"{base}{suffix}.{ext}"
    with open(new_file, "w", encoding="utf-8") as out:
        out.write("\n".join(code_lines))
    print(f"Reconstructed {new_file} from history up to {target_timestamp}")

def tui(ppath):
    global pydift_conf_path
    pydift_conf_path = os.path.join(os.path.expanduser("~"), ".pydift/pydift_conf.yaml")

    diffs = load_diffs(ppath)
    if not diffs:
        print("No diffs found.")
        return
    clear_screen()
    choices = ["Quit", "Configure"]
    choices += [
        f"{i+1}) {d['user']} at {d['timestamp']}"
        for i, d in enumerate(diffs)
    ]
    
    while True:
        clear_screen()
        index = inquirer.select(
            message="Select a diff to view or reconstruct:",
            choices=choices,
        ).execute()

        chosen_idx = choices.index(index)
        if chosen_idx == 0:
            clear_screen()
            break
        if chosen_idx == 1:
            clear_screen()            
            conf_options = ["Back", "Model", "Summary", "Wide", "Recursive"]
            while True:
                clear_screen()
                chosen_conf_index = inquirer.select(
                    message="Configure pydift default parameters:",
                    choices=conf_options
                ).execute()
                if chosen_conf_index == "Back":
                    clear_screen()
                    break
                with open(pydift_conf_path, "r") as f:
                    current_conf = yaml.safe_load(f)
                if chosen_conf_index == "Model":
                    current_settings = current_conf.get("model", "Not set!")
                    print(blue(f"\nCurrent value: {current_settings}"))
                    model_choices = ['Back']
                    model_choices += [f"{i+1}) " + m for i, m in enumerate(available_calls)]
                    chosen_call = inquirer.select(
                        message="Set LLM for summaries:",
                        choices=model_choices
                    ).execute()
                    if chosen_call == "Back":
                        continue
                    chosen_call_idx = model_choices.index(chosen_call)-1
                    with open(pydift_conf_path, "r") as f:
                        current_conf = yaml.safe_load(f)
                        current_conf["model"] = available_calls[chosen_call_idx]
                    with open(pydift_conf_path, "w") as f:
                        yaml.dump(current_conf, f)
                    input("\n"+blue("Press Enter to continue..."))
                elif chosen_conf_index == "Summary":
                    current_settings = current_conf.get("summary", "Not set!")
                    print(blue(f"\nCurrent value: {current_settings}"))
                    summary_options = ["Back", "True", "False"]
                    chosen_summary = inquirer.select(
                        message="Produce summaries of diffs by default:",
                        choices=summary_options
                    ).execute()
                    if chosen_summary == "Back":
                        continue
                    with open(pydift_conf_path, "r") as f:
                        current_conf = yaml.safe_load(f)
                        current_conf["summary"] = chosen_summary == "True"
                    with open(pydift_conf_path, "w") as f:
                        yaml.dump(current_conf, f)
                    input("\n"+blue("Press Enter to continue..."))
                elif chosen_conf_index == "Wide":
                    current_settings = current_conf.get("wide", "Not set!")
                    print(blue(f"\nCurrent value: {current_settings}"))
                    wide_options = ["Back", "True", "False"]
                    chosen_wide = inquirer.select(
                        message="Diff all files in directory by default:",
                        choices=wide_options
                    ).execute()
                    if chosen_wide == "Back":
                        continue
                    with open(pydift_conf_path, "r") as f:
                        current_conf = yaml.safe_load(f)
                        current_conf["wide"] = chosen_wide == "True"
                    with open(pydift_conf_path, "w") as f:
                        yaml.dump(current_conf, f)
                    input("\n"+blue("Press Enter to continue..."))
                elif chosen_conf_index == "Recursive":
                    current_settings = current_conf.get("recursive", "Not set!")
                    print(blue(f"\nCurrent value: {current_settings}"))
                    recursive_options = ["Back", "True", "False"]
                    chosen_recursive = inquirer.select(
                        message="Diff all files in directory and subdirectories by default:",
                        choices=recursive_options
                    ).execute()
                    if chosen_recursive == "Back":
                        continue
                    with open(pydift_conf_path, "r") as f:
                        current_conf = yaml.safe_load(f)
                        current_conf["recursive"] = chosen_recursive == "True"
                    with open(pydift_conf_path, "w") as f:
                        yaml.dump(current_conf, f)
                    input("\n"+blue("Press Enter to continue..."))
            continue
        chosen_diff = diffs[chosen_idx - 2]

        action = inquirer.select(
            message="Choose an action:",
            choices=["Show diff", "Reconstruct code", "Cancel"]
        ).execute()

        if action == "Show diff":
            clear_screen()
            print("\n--- Summary ---")
            print(chosen_diff.get("diff_summary", "No summary available."))
            print("\n--- Diff ---")
            diff_text = chosen_diff.get("diff_full", "No diff available.")
            diff_text = diff_text.split("\n")
            for line in diff_text:
                if line.startswith("+"):
                    print(green(line))
                elif line.startswith("-"):
                    print(red(line))
                else:
                    print(line)
            input("\n"+blue("Press Enter to continue..."))

        elif action == "Reconstruct code":
            clear_screen()
            print("Not yet implemented.")
            input("\n"+blue("Press Enter to continue..."))
            # reconstruct_code(chosen_diff, ppath)