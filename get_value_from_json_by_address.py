import csv
import json
import os

def flatten_json(data, prefix=''):
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{prefix}.{k}" if prefix else k
            items.extend(flatten_json(v, new_key))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{prefix}[{i}]"
            items.extend(flatten_json(item, new_key))
    else:
        items.append((prefix, data))
    return items

def get_value_from_json(data, path):
    keys = path.replace('[', '.').replace(']', '').split('.')
    value = data
    for key in keys:
        if key.isdigit():
            key = int(key)
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and isinstance(key, int) and key < len(value):
            value = value[key]
        else:
            return None
    return value

def main():
    # Read the JSON file
    with open('sample1.json', 'r') as json_file:
        json_data = json.load(json_file)

    # Read the CSV file with address paths
    with open('json_template.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        address_paths = [row[0] for row in csv_reader]

    # Prepare data for the new CSV
    output_data = {}
    for path in address_paths:
        if '[i]' in path:
            base_path = path.split('[i]')[0]
            array_value = get_value_from_json(json_data, base_path)
            if isinstance(array_value, list):
                flattened = flatten_json(array_value, base_path)
                output_data.update({item[0]: item[1] for item in flattened})
        else:
            value = get_value_from_json(json_data, path)
            if isinstance(value, (dict, list)):
                flattened = flatten_json(value, path)
                output_data.update({item[0]: item[1] for item in flattened})
            else:
                output_data[path] = value

    # Write to a new CSV file
    with open('address_values.csv', 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['Address Path', 'Value'])  # Header
        for path, value in output_data.items():
            writer.writerow([path, value])

    print(f"CSV file 'address_values.csv' has been created in {os.getcwd()}")

if __name__ == "__main__":
    main()