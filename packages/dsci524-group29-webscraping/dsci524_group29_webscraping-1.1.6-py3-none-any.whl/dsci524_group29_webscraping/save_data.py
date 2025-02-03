# save_data.py
# author: Hui Tang
# date: 2025-01-16

import os
import json
import csv

def save_data(data, format='csv', destination='output.csv'):
    """
    Saves the extracted data into a file in the specified format at the given destination.

    Parameters:
        data (list or dict): The data to be saved.
            - For 'csv', it must be a list of dictionaries where each dictionary represents a row.
            - For 'json', it can be either a list or a dictionary.
        format (str, optional): The file format to save the data. Supported formats are:
            - 'csv': Saves the data as a CSV file.
            - 'json': Saves the data as a JSON file.
            Default is 'csv'.
        destination (str, optional): The file path where the data will be saved. 
            Default is 'output.csv'.

    Returns:
        str: The absolute path to the saved file.

    Raises:
        ValueError: If the specified format is unsupported or the data structure is incompatible with the format.
        FileNotFoundError: If the directory specified in the destination path does not exist.
        Exception: If an unexpected error occurs during the file writing process.

    Examples:
        # Save data as a CSV file
        save_data([{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}], format='csv', destination='data.csv')

        # Save data as a JSON file
        save_data({"name": "Alice", "age": 25}, format='json', destination='data.json')

    Notes:
        - For 'csv', the input data must be a list of dictionaries where each dictionary represents a row in the CSV.
        - For 'json', the input data can be a dictionary or a list.
        - If the specified directory in the destination does not exist, a FileNotFoundError will be raised.
    """
    # Validate the destination directory
    dir_path = os.path.dirname(destination)
    if dir_path and not os.path.exists(dir_path):
        # Ensure the directory exists before attempting to save
        raise FileNotFoundError(f"The directory {dir_path} does not exist.")

    # Save data in CSV format
    if format == 'csv':
        # Ensure the input data is a list of dictionaries
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("For CSV, data must be a list of dictionaries.")
        try:
            with open(destination, mode='w', newline='') as file:
                # Write the data to the CSV file
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()  # Write the header row
                writer.writerows(data)  # Write the data rows
        except Exception as e:
            # Handle unexpected issues when saving the CSV file
            raise Exception(f"Failed to save CSV data: {e}")

    # Save data in JSON format
    elif format == 'json':
        # Ensure the input data is either a list or a dictionary
        if not isinstance(data, (list, dict)):
            raise ValueError("For JSON, data must be a list or a dictionary.")
        try:
            with open(destination, mode='w') as file:
                # Write the JSON data to the file with indentation for readability
                json.dump(data, file, indent=4)
        except Exception as e:
            # Handle unexpected issues when saving the JSON file
            raise Exception(f"Failed to save JSON data: {e}")

    else:
        # Raise an error for unsupported formats
        raise ValueError("Unsupported format. Use 'csv' or 'json'.")

    # Return the absolute path to the saved file
    return os.path.abspath(destination)