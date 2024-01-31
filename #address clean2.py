#address clean
import pandas as pd
import difflib 
import usaddress

def normalize_address(address, designation_mapping):
    for key, value in designation_mapping.items():
        address = address.replace(value, key)
    return address

def to_ups_format(parsed_address):
    # Assuming UPS format includes "UPS" as a prefix
    return f"UPS {parsed_address}"

def convert_to_ups_format_with_designation(input_file, output_file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file)

    # Define street designation mapping
    designation_mapping = {"St": "Street", "Ln": "Lane", "Rd": "Road"}

    # Create a new column for UPS-formattel addresses
    df['UPS_Format'] = df['Address'].apply(lambda x: to_ups_format(normalize_address(str(x), designation_mapping)))

    # Create a new column for missing street designations
    df['Missing_Designation'] = df['Address'].apply(lambda x: find_missing_designation(str(x), designation_mapping))
    

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_file, index=False)

def find_missing_designation(address, designation_mapping):
    # Parse the address using usaddress library
    parsed_address, address_type = usaddress.tag(address)
    
    # Check if the parsed address contains a street designation
    if 'StreetNamePostType' not in parsed_address and 'StreetNamePostType' not in address_type:
        # If missing, find a matching street designation
        for key, value in designation_mapping.items():
            if difflib.SequenceMatcher(None, key, parsed_address['StreetName']).ratio() > 0.8:
                return value
    
    return ''

if __name__ == "__main__":
    input_excel_file = "/Users/devin/Documents/RAW_ADDRESSES.xlsx"  # Update with your input file path
    output_excel_file = "/Users/devin/Documents/UPSRAW.xlsx"  # Update with your desired output file path

    convert_to_ups_format_with_designation(input_excel_file, output_excel_file)