import json

def get_value_from_path(data, path):
    """Helper function to get value from a nested path"""
    if not path:  # If path is empty, return the data itself
        return data
        
    current = data
    parts = path.replace('[i]', '').split('.')
    
    try:
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                results = []
                for item in current:
                    if isinstance(item, dict):
                        results.append(item.get(part))
                current = results
            if current is None:
                return None
    except (KeyError, TypeError, AttributeError):
        return None
    
    return current

def get_json_data_by_address(data, filter_address, addresses, conditions=None):
    """Main function to get data based on filter address, desired addresses, and optional conditions"""
    results = {}
    
    # If filter_address is empty, use the root data
    filtered_section = data if not filter_address else get_value_from_path(data, filter_address)
    if filtered_section is None:
        return results

    # If filtered_section is not a list, wrap it in a list for consistent processing
    if not isinstance(filtered_section, list):
        filtered_section = [filtered_section]

    # Apply conditions if they exist
    if conditions:
        filtered_items = []
        for item in filtered_section:
            if all(get_value_from_path(item, cond_key) == cond_value for cond_key, cond_value in conditions.items()):
                filtered_items.append(item)
        filtered_section = filtered_items
    
    # For each address, get the values
    for address in addresses:
        values = []
        for item in filtered_section:
            value = get_value_from_path(item, address)
            if value is not None:
                values.append(value)
        
        if values:
            results[address] = values if len(values) > 1 or '[i]' in address else values[0]

    return results

def main():
    # Load your JSON data
    with open('sample.json', 'r') as json_file:
        json_data = json.load(json_file)

    # Define the filter address and the addresses to retrieve
    filter_address = 'additionalDetails'  # Empty string for root level
    addresses = ['items[i].price.currency', 'items[i].price.value', 'orderId']
    
    # Test without conditions
    result_without_conditions = get_json_data_by_address(json_data, filter_address, addresses)
    print("Results without conditions:")
    print(json.dumps(result_without_conditions, indent=4))


    # Test with conditions
    # conditions = {'name': 'Product A'}
    # result_with_conditions = get_json_data_by_address(json_data, filter_address, addresses, conditions)
    # print("\nResults with conditions:")
    # print(json.dumps(result_with_conditions, indent=4))

if __name__ == "__main__":
    main()