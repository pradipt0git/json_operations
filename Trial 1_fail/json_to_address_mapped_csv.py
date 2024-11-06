import pandas as pd
import json

def extract_data(data, parent_path=''):
    df = pd.DataFrame()
    for key, value in data.items():
        if isinstance(value, dict):
            df = pd.concat([df, extract_data(value, parent_path + '.' + key)])
        elif isinstance(value, list):
            for i, item in enumerate(value):
                df = pd.concat([df, extract_data(item, parent_path + '.' + key + '[' + str(i) + ']')])
        else:
            df[parent_path + '.' + key] = value
    return df

# Load the JSON data
with open('sample.json', 'r') as f:
    data = json.load(f)

# Extract data and transpose the DataFrame
df = extract_data(data).T

# Export the DataFrame to a CSV file
df.to_csv('output.csv')