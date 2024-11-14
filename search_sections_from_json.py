import json

def get_value_from_path(data, path):
    """Helper function to get value from a nested path"""
    if not path:
        return data

    current = data
    parts = path.split('.')

    try:
        for part in parts:
            if '[' in part:
                # Handle array indexing
                array_name = part.split('[')[0]
                index = part.split('[')[1].split(']')[0]
                current = current[array_name]
                if index != 'i':  # If specific index
                    current = current[int(index)]
            elif isinstance(current, dict):
                current = current.get(part)
            if current is None:
                return None
    except (KeyError, TypeError, AttributeError, IndexError):
        return None
    
    return current

def extract_values(data, path):
    """Extract values from a path that may contain [i]"""
    if '[i]' not in path:
        return get_value_from_path(data, path)

    parts = path.split('.')
    current = data
    items_found = False

    for part in parts:
        if '[i]' in part:
            array_name = part.split('[')[0]
            if isinstance(current, dict) and array_name in current:
                current = current[array_name]
                items_found = True
                continue
        if items_found:
            # We're past the [i] part, collect values from each item
            results = []
            for item in current:
                value = get_value_from_path(item, '.'.join(parts[parts.index(part):]))
                if value is not None:
                    results.append(value)
            return results
        current = get_value_from_path(current, part)
        if current is None:
            return None
    return current

def get_json_data_by_address(data, filter_address, addresses, conditions=None):
    """Main function to get data based on filter address, desired addresses, and optional conditions"""
    results = {}
    
    # Get the filtered section based on filter_address
    filtered_data = get_value_from_path(data, filter_address)
    if filtered_data is None:
        return results

    # Handle conditions
    if conditions and isinstance(filtered_data, dict) and 'items' in filtered_data:
        filtered_items = []
        for item in filtered_data['items']:
            matches_all = True
            for cond_key, cond_value in conditions.items():
                clean_key = cond_key.replace('additionalDetails.items[i].', '')
                if get_value_from_path(item, clean_key) != cond_value:
                    matches_all = False
                    break
            if matches_all:
                filtered_items.append(item)
        filtered_data['items'] = filtered_items

    # Process each address
    for address in addresses:
        if '[i]' in address:
            # Handle array iteration
            values = extract_values(data, address)
            if values:
                results[address] = values
        else:
            # Handle direct addressing
            value = get_value_from_path(data, address)
            if value is not None:
                results[address] = value

    return results

def main():
    # Load your JSON data
    with open('sample.json', 'r') as json_file:
        json_data = json.load(json_file)

    # Test Case 1: filter_address = 'additionalDetails'
    filter_address = 'additionalDetails'
    addresses = ['additionalDetails.items[i].price.currency', 'additionalDetails.items[i].price.value','referenceNumber']
    
    print("Test Case 1 - filter_address = 'additionalDetails'")
    # Without conditions
    result = get_json_data_by_address(json_data, filter_address, addresses)
    print("\nResults without conditions:")
    print(json.dumps(result, indent=4))
    
    # With conditions
    conditions = {'additionalDetails.items[i].name': 'Product A'}
    result = get_json_data_by_address(json_data, filter_address, addresses, conditions)
    print("\nResults with conditions:")
    print(json.dumps(result, indent=4))

    # Test Case 2: filter_address = 'additionalDetails.items[0]'
    filter_address = 'additionalDetails.items[0]'
    print("\nTest Case 2 - filter_address = 'additionalDetails.items[0]'")
    # Without conditions
    result = get_json_data_by_address(json_data, filter_address, addresses)
    print("\nResults without conditions:")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()