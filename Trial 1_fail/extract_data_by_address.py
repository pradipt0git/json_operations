import csv
import json

def extract_data_by_address(json_data, address):
    """Extracts data from a JSON object using a dot-separated address.

    Args:
        json_data: The JSON data as a Python object.
        address: The dot-separated address to the desired data.

    Returns:
        The extracted data, or None if the address is not found.
    """

    parts = address.split('.')
    data = json_data

    for part in parts:
        if isinstance(data, dict):
            if part in data:
                data = data[part]
            else:
                pass
                #return None  # Handle missing keys
        elif isinstance(data, list):
            try:
                index = int(part)
                data = data[index]
            except (ValueError, IndexError):
                pass
                #return None  # Handle invalid index or out-of-bounds access
        else:
            return data  # Return the value if it's not a dict or list

    return data

# Load the JSON data
with open('sample.json', 'r') as f:
    json_data = json.load(f)

# Open the addresses CSV file for reading and the output CSV for writing
with open('output.csv', 'r') as addresses_file, open('address_wise_csv.csv', 'w', newline='') as output_file:
    reader = csv.reader(addresses_file)
    writer = csv.writer(output_file)

    # Write the header row to the output CSV
    writer.writerow(['Address', 'Value'])

    # Extract data and write to the output CSV
    for row in reader:
        address = row[0]  # Assuming the first column contains the address
        value = extract_data_by_address(json_data, address)
        writer.writerow([address, value])