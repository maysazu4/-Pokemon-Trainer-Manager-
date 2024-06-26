import json


def read_data_json(file_path):
    """
    Read JSON data from a file.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    (list of dict): The data read from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_data_json(file_path, data):
    """
    Write JSON data to a file.

    Parameters:
    file_path (str): The path to the JSON file.
    data (list of dict): The data to write to the JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
