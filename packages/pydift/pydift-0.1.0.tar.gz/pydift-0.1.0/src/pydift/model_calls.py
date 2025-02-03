import requests, json, os, yaml
from copy import deepcopy

global available_calls
global model_confs

model_conf_path = os.path.join(os.path.expanduser("~"), ".pydift/model_conf.yaml")
with open(model_conf_path, "r") as f:
    model_confs = yaml.safe_load(f)
available_calls = list(model_confs.keys())

def generic_call(prompt, model_name):
    """
    Generic call to a language model API.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The model to call.

    Returns:
        str: Model response
    """
    model_conf = deepcopy(model_confs[model_name])
    if "api_key_env" in model_conf:
        model_conf["api_key"] = os.environ.get(model_conf["api_key_env"])
    api_key = model_conf["api_key"]
    api_key_path = model_conf["api_key_path"].split('.')
    response_path = model_conf["response_path"].split('.')
    input_path = model_conf["input_path"].split('.')
    input_data = model_conf["data"]
    for i, key in enumerate(input_path):
        # check if key is num
        if key.isdigit():
            key = int(key)
        if i < len(input_path) - 1:
            input_data = input_data[key]
        elif i == len(input_path) - 1:
            input_data[key] = prompt
    
    api_data = model_conf
    for i, key in enumerate(api_key_path):
        # check if key is num
        if key.isdigit():
            key = int(key)
        if i < len(api_key_path) - 1:
            api_data = api_data[key]
        elif i == len(api_key_path) - 1:
            api_data[key] = api_data[key].replace("$API_KEY", api_key)
    url = model_conf["url"]
    headers = model_conf["headers"]
    data = model_conf["data"]
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = response.json()
    for key in response_path:
        if key.isdigit():
            key = int(key)
        response = response[key]
    return response