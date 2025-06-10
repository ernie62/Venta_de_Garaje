import json
import unicodedata
import re
import os

def slugify_description(description):
    """
    Takes a description, extracts the first 3 words/numbers, removes accents,
    replaces spaces with hyphens, and converts to lowercase to create a slug.

    Args:
        description (str): The input description string.

    Returns:
        str: The slugified string from the first 3 tokens, suitable for a filename.
             (e.g., "Mueble de madera de 2 puertas" -> "mueble-de-madera")
             (e.g., "2 Mesas de noche" -> "2-mesas-de")
    """
    # Split the description into words/numbers (tokens)
    words = description.split()
    
    # Take only the first 3 tokens, or fewer if the description is shorter
    tokens_for_slug = " ".join(words[:3]) 
    
    # Normalize unicode characters to remove accents (NFD form)
    normalized_text = unicodedata.normalize('NFD', tokens_for_slug)
    
    # Encode to ASCII, ignoring non-ASCII characters (which removes accents), then decode back to utf-8
    slug = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    
    # Replace any non-alphanumeric characters (except spaces and hyphens) with nothing.
    # This helps clean up the string before hyphenating.
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace any sequence of whitespace characters with a single hyphen
    # and convert the entire string to lowercase
    slug = re.sub(r'\s+', '-', slug).lower()
    
    # Remove any leading or trailing hyphens that might result from extra spaces/chars
    slug = slug.strip('-')

    return slug

def update_image_paths_in_json(input_filepath, output_filepath=None):
    """
    Reads a JSON file, modifies the first image path for each item
    based on the 'descripcion' field, and saves the updated JSON.

    Args:
        input_filepath (str): The path to the input JSON file.
        output_filepath (str, optional): The path to save the modified JSON file.
                                         If None, the original file will be overwritten.
    """
    print(f"Attempting to load data from: {input_filepath}")
    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' does not exist.")
        return

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("JSON data loaded successfully.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_filepath}'. Please check the file's format.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    # Ensure data is a list; if it's a single object, wrap it in a list
    if not isinstance(data, list):
        data = [data]
        print("JSON data was a single object, converted to a list for processing.")

    updated_count = 0
    for item in data:
        # Check if the required keys exist and 'fotos' list is not empty
        if "descripcion" in item and "fotos" in item and isinstance(item["fotos"], list) and item["fotos"]:
            description = item["descripcion"]
            
            # Generate the new slug from the first 3 tokens of the description
            new_slug = slugify_description(description)
            
            # Construct the new image path
            new_image_path = f"./images/{new_slug}.jpg"
            
            # Update the first photo URL in the 'fotos' list
            item["fotos"][0] = new_image_path
            updated_count += 1
        else:
            print(f"Warning: Item {item.get('id', 'unknown')} is missing 'descripcion' or 'fotos' field, 'fotos' is not a list, or 'fotos' is empty. Skipping this item.")

    # Determine the output file path
    if output_filepath is None:
        final_output_path = input_filepath
    else:
        final_output_path = output_filepath

    try:
        with open(final_output_path, 'w', encoding='utf-8') as f:
            # Use indent for pretty-printing, ensure_ascii=False for non-ASCII characters
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully updated {updated_count} image paths and saved to '{final_output_path}'.")
    except IOError as e:
        print(f"Error: Could not write to file '{final_output_path}'. {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing the file: {e}")


# --- HOW TO USE THIS SCRIPT ---
if __name__ == "__main__":
    # Define your input JSON file name
    # Make sure this file is in the same directory as this script, or provide the full path.
    input_json_file = 'data.json' 
    
    # Define your output JSON file name.
    # If you want to OVERWRITE the original file, set output_json_file = None
    output_json_file = 'data_n_images.json' 

    # --- OPTIONAL: Code to create a dummy JSON file for testing ---
    # You can uncomment this section to generate a test file if you don't have one ready.
    # Make sure to comment it out or delete the generated file before running with your actual data.
    
    # dummy_data_for_testing = [
    #     {
    #         "id": "item-003",
    #         "descripcion": "Cama doble en Cedro con su respectivo colchón",
    #         "descripcionIngles": "Cedar double bed with mattress.",
    #         "categoria": "Muebles",
    #         "precio": "$800.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     {
    #         "id": "item-004",
    #         "descripcion": "Mueble de madera de 2 puertas con 15 entrepaños de 1.97 alto por 90 cm ancho y 27 de fondo",
    #         "descripcionIngles": "Wooden cabinet, 2 doors, 15 shelves. 1.97m H x 90cm W x 27cm D.",
    #         "categoria": "Muebles",
    #         "precio": "$700.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     {
    #         "id": "item-005",
    #         "descripcion": "2 Mesas de noche con sus lámparas",
    #         "descripcionIngles": "2 nightstands with lamps.",
    #         "categoria": "Muebles",
    #         "precio": "$350.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     {
    #         "id": "item-022",
    #         "descripcion": "Parrilla eléctrica para asar",
    #         "descripcionIngles": "Electric grilling pan.",
    #         "categoria": "Electrodomesticos",
    #         "precio": "$250.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     {
    #         "id": "item-026",
    #         "descripcion": "Sólo una palabra",
    #         "descripcionIngles": "Only one word.",
    #         "categoria": "Misceláneos",
    #         "precio": "$5.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     { # New test case for 3 words
    #         "id": "item-027",
    #         "descripcion": "Lámpara de pie moderna",
    #         "descripcionIngles": "Modern floor lamp.",
    #         "categoria": "Decoración",
    #         "precio": "$120.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     },
    #     { # New test case for number-word-word
    #         "id": "item-028",
    #         "descripcion": "10 Botellas de vidrio",
    #         "descripcionIngles": "10 glass bottles.",
    #         "categoria": "Cocina",
    #         "precio": "$50.000 COP",
    #         "disponibilidad": "si",
    #         "fotos": [
    #             "./images/ ----- .jpg",
    #             "./images/ ----- .jpg"
    #         ]
    #     }
    # ]

    # # Set the input file name for the dummy data
    # input_json_file = 'dummy_items_for_testing.json'
    # print(f"Creating dummy data in '{input_json_file}' for testing purposes...")
    # with open(input_json_file, 'w', encoding='utf-8') as f:
    #     json.dump(dummy_data_for_testing, f, indent=4, ensure_ascii=False)
    # print("Dummy data created.")

    # --- End of OPTIONAL dummy data creation section ---


    # Call the main function to update image paths
    update_image_paths_in_json(input_json_file, output_json_file)