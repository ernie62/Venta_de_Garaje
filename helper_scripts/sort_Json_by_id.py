import json
import os

def sort_json_by_id(input_json_path, output_json_path):
    """
    Reads a JSON file containing a list of objects, sorts them lexicographically
    by their 'id' field in ascending order, and saves the sorted data to a new JSON file.

    Args:
        input_json_path (str): Path to the input JSON file (e.g., 'data_n_images copy.json').
        output_json_path (str): Path for the output sorted JSON file (e.g., 'data_n_images_orderd.json').
    """
    # 1. Check if the input file exists
    if not os.path.exists(input_json_path):
        print(f"Error: Input JSON file not found at '{input_json_path}'. Please ensure it exists.")
        return

    # 2. Read the main JSON data
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"**Successfully loaded JSON data from '{input_json_path}'.**")
        print(f"  Total items loaded: {len(data)}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{input_json_path}': {e}")
        return
    except Exception as e:
        print(f"Error reading input JSON file '{input_json_path}': {e}")
        return

    # 3. Sort the JSON data by 'id'
    # We'll use a custom key for sorting: lambda item: item.get('id', '')
    # .get('id', '') handles cases where an item might not have an 'id'
    # by defaulting to an empty string, preventing a KeyError during sorting.
    try:
        # Filter out items that explicitly do not have an 'id' before sorting,
        # or handle them based on your desired behavior.
        # For simple lexicographical sort, all items should ideally have an 'id'.
        # If an item doesn't have an 'id', .get('id', '') will put it at the beginning.
        sorted_data = sorted(data, key=lambda item: item.get('id', ''))
        print(f"**Data successfully sorted by 'id' in ascending lexicographical order.**")
    except TypeError as e:
        print(f"Error during sorting (possibly inconsistent 'id' types): {e}")
        print("Please ensure all 'id' values are comparable (e.g., all strings).")
        return
    except Exception as e:
        print(f"An unexpected error occurred during sorting: {e}")
        return

    # 4. Write the sorted data to a new JSON file
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, indent=2, ensure_ascii=False)
        print(f"**Sorted data successfully written to '{output_json_path}'.**")
    except Exception as e:
        print(f"Error writing output JSON file '{output_json_path}': {e}")

if __name__ == "__main__":
    # Define your input and output file names
    input_file = "../data_n_images.json" # Your original JSON file
    output_file = "data_n_images_orderd.json" # The new sorted JSON file

    print("--- Starting JSON Sorting Process ---")

    # Call the sorting function
    sort_json_by_id(input_file, output_file)

    print("--- Process Finished ---")