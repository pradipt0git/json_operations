import json
import csv
import os

def extract_address_paths(data, prefix=''):
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                paths.extend(extract_address_paths(value, current_path))
            else:
                paths.append(current_path)
    elif isinstance(data, list):
        # For lists, we use [i] to indicate any index
        if prefix:  # If there is a prefix, we append [i] to it
            current_path = f"{prefix}[i]"
        else:  # If there is no prefix, we just use [i]
            current_path = '[i]'
        paths.append(current_path)  # Add the generic list path
        if data:  # Only process the first item of the list to avoid duplicates
            paths.extend(extract_address_paths(data[0], current_path))
    return paths

def main():
    # Read the JSON file
    with open('sample.json', 'r') as file:
        data = json.load(file)

    # Extract all address paths
    all_paths = extract_address_paths(data)

    # Write to CSV file
    with open('json_template.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address Path'])  # Header
        for path in all_paths:
            writer.writerow([path])

    print(f"CSV file 'json_template.csv' has been created in {os.getcwd()}")

if __name__ == "__main__":
    main()