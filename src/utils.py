import json

def read_json(path: str) -> dict:
    """
    Helper function that reads a json file into a python dict.
    
    Params:
        path (str): the path that contains the json file.
    Returns:
        dict: a python dictionary containing all the key-value pairs from the json file.
    """
    try:
        with open(path) as json_file:
            data = json.load(json_file)
            return data
    except Exception:
        raise Exception(f"Could not open/read file:, {path}")

