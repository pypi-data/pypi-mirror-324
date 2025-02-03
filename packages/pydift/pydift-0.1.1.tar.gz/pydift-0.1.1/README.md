# pydift

pydift is a simple version-tracking tool for research code development. It allows you to track changes in your code, generate diffs, and even reconstruct code at specific points in time. Additionally, it can summarize diffs using various language models.

![pydift TUI](figures/demo.gif)

Current version: 0.1.1

## Features

- Track changes in your Python scripts.
- Generate diffs between code runs.
- Summarize diffs using language models.
- Reconstruct code at specific points in time.
- Interactive Text User Interface (TUI) for managing diffs and configurations.

## Installation

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## Usage
### Command Line Interface (CLI)
You can use pydift from the command line to track and run your scripts. Here are some examples:
```sh
# Track and run a script
pydift script.py
pydift -p script.py
pydift --path script.py

# Track and run a script, and generate a summary of the diff
pydift -s script.py
pydift --summary script.py

# Track all files in the current directory
pydift -w script.py
pydift --wide script.py

# Track all files in the current directory and subdirectories
pydift -r script.py
pydift --recursive script.py

# Launch the pydift TUI
pydift
pydift -t
pydift --tui
pydift path/to/folder
```

### Text User Interface (TUI)
pydift also provides an interactive TUI for managing diffs and configurations. To launch the TUI, run:
```sh
pydift --tui
pydift -t
```

In the TUI, you can:

- Scroll between diffs of code runs.
- Select a diff to view or reconstruct the code at that point in time.
- Configure pydift settings such as the language model, summary generation, and file tracking options.

## Configuration

pydift uses a configuration file located at `~/.pydift/pydift_conf.yaml`. The default configuration is:
```yaml
model: "Meta Llama 3.3"
summary: False
wide: False
recursive: False
```
You can modify these settings directly in the configuration file or through the TUI.

### Adding models

By default, pydift is configured with the following models:
- OpenAI GPT-4o
- Meta Llama 3.3
- Google Gemini 2.0 Flash (Exp)

You can add new models to be used by pydift (and then configure appropriately through the TUI), by adding the details of the cURL request to `model_conf.yaml` (in `~/.pydift`).
For example,
```yaml
OpenAI GPT-4o:
    url: "https://api.openai.com/v1/chat/completions"
    headers:
      Content-Type: "application/json"
      Authorization:  "Bearer $API_KEY"
    data:
      model: "gpt-4o"
      messages:
        - role: "user"
          content: none
      max_completion_tokens: 256
      temperature: 0.7
    api_key_env: "OPENAI_API_KEY"
    api_key_path: "headers.Authorization"
    response_path: "choices.0.message.content"
    input_path: "messages.0.content"
```

Note the following sections:
- The name of the entry (e.g `OpenAI GPT-4o`) will appear in the TUI selection screen.
- The URL is the target of the API call.
- The headers (typically the same for all models)
- The data (this differs substantially between models)
- api_key_path: This indicates in which part of the (entire) request JSON the API key will be inserted (indicated by the placeholder `$API_KEY`)
- api_key_env: The name of the environment variable holding the API key.
- api_key: alternatively, possible to directly give the api_key in the yaml (will be superceded by api_key_env)
- response_path: Given a successful call to the model's API, assuming the response returns a JSON, this indicates the list of keys, to be accessed in succession, to get the actual text output of the model.
- input_path: This indicates in which part of the data portion of the request JSON, the prompt will be inserted (in the above example, in data["messages"][0]["content"])

## Example
Here is an example of how to use pydift:

1. Create a Python script example.py:
```python
print("Hello, world!")
```

2. Track the script using pydift:
```python
pydift example.py
```

3. Modify the script to print a different message:
```python
print("Goodbye, world!")
```

4. Track the script again:
```python
pydift example.py
```

5. Launch the pydift TUI:
```python
pydift --tui
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
