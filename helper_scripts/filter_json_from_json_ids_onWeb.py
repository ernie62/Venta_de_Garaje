import json
import os # Import the os module to check for file existence

def filter_json_by_ids(json_file_path, ids_to_exclude_file_path, output_file_path):
    """
    Reads a JSON file, filters out items whose IDs are in a given text file,
    and writes the remaining items to a new JSON file.

    Args:
        json_file_path (str): Path to the input JSON file (data_n_images copy.json).
        ids_to_exclude_file_path (str): Path to the text file containing IDs to exclude (json_ids_onWeb.txt).
        output_file_path (str): Path for the output JSON file.
    """
    # 1. Read IDs to exclude from the text file
    excluded_ids = set()
    if not os.path.exists(ids_to_exclude_file_path):
        print(f"Error: Excluded IDs file not found at '{ids_to_exclude_file_path}'. Please ensure it exists.")
        return

    try:
        with open(ids_to_exclude_file_path, 'r') as f:
            for line in f:
                # Remove leading/trailing whitespace and quotes
                excluded_ids.add(line.strip().replace('"', ''))
        print(f"**Successfully loaded IDs to exclude from '{ids_to_exclude_file_path}':**")
        print(f"  {excluded_ids}")
    except Exception as e:
        print(f"Error reading excluded IDs file '{ids_to_exclude_file_path}': {e}")
        return

    # 2. Read the main JSON data
    if not os.path.exists(json_file_path):
        print(f"Error: Input JSON file not found at '{json_file_path}'. Please ensure it exists.")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"**Successfully loaded main JSON data from '{json_file_path}'.**")
        print(f"  Total items in original JSON: {len(data)}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{json_file_path}': {e}")
        return
    except Exception as e:
        print(f"Error reading main JSON file '{json_file_path}': {e}")
        return

    # 3. Filter the JSON data
    filtered_data = []
    items_filtered_out = 0
    for item in data:
        if "id" in item:
            if item["id"] not in excluded_ids:
                filtered_data.append(item)
            else:
                items_filtered_out += 1
        else:
            # Optionally, you can add items without an 'id' or log them
            # For this request, we'll assume all relevant items have an 'id'
            filtered_data.append(item)
            print(f"Warning: Item without 'id' found and included: {item.get('descripcion', 'No description')}")

    print(f"**Filtering complete.**")
    print(f"  Number of items excluded: {items_filtered_out}")
    print(f"  Number of items remaining: {len(filtered_data)}")

    # 4. Write the filtered data to a new JSON file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        print(f"**Filtered data successfully written to '{output_file_path}'.**")
    except Exception as e:
        print(f"Error writing output JSON file '{output_file_path}': {e}")

if __name__ == "__main__":
    # Define your actual file paths here
    ids_file_name = "json_ids_onWeb.txt"
    input_json_file_name = "data_n_images copy.json"
    output_json_file_name = "missing_items_on_web_base_of_xl.json"

    print("--- Starting JSON Filtering Process ---")

    # Call the filtering function with your specified file names
    filter_json_by_ids(input_json_file_name, ids_file_name, output_json_file_name)

    print("--- Process Finished ---")