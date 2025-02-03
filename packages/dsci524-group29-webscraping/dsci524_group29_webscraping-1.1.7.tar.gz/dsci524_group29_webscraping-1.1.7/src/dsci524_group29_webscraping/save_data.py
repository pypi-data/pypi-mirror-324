# save_data.py
# author: Hui Tang
# date: 2025-01-16

import os
import json
import csv

def save_data(data, format='csv', destination='output.csv'):
    """
    Saves the extracted data into a file.

    Parameters:
        data (list or dict): The data to be saved.
            - For 'csv', it must be a list of dictionaries where each dictionary represents a row.
            - For 'json', it can be either a list or a dictionary.
        format (str, optional): The format in which to save the data. Options are:
            - 'csv': Saves the data as a CSV file. Each key in the dictionaries becomes a column header.
            - 'json': Saves the data as a JSON file. The data is serialized with indentation for readability.
            Default is 'csv'.
        destination (str, optional): The file path to save the data. Can specify:
            - A file name (e.g., 'output.csv').
            - A full path (e.g., '/path/to/output.csv').
            Default is 'output.csv'.

    Returns:
        str: The absolute path to the saved file.

    Raises:
        ValueError: If the format is unsupported or if the data structure is incompatible with the format.
        FileNotFoundError: If the directory specified in the destination path does not exist.
        Exception: If an unexpected error occurs during the file-writing process.

    Examples:
        # Save data as a CSV file
        save_data([{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}], format='csv', destination='data.csv')

        # Save data as a JSON file
        save_data({"name": "Alice", "age": 25}, format='json', destination='data.json')

    Notes:
        - The directory specified in the destination path must exist; otherwise, a FileNotFoundError is raised.
        - For 'csv', the first dictionary in the list determines the column headers.
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