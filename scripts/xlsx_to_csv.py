import pandas as pd
import argparse
import sys

def convert_xlsx_to_csv(input_file, output_file):
    try:
        print(f"Reading {input_file}...")
        # Read the Excel file
        df = pd.read_excel(input_file)
        
        print(f"Writing to {output_file}...")
        # Write to CSV, excluding the row indices
        df.to_csv(output_file, index=False)
        
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an XLSX file to a CSV file using pandas.")
    parser.add_argument("input_file", help="Path to the input .xlsx file")
    parser.add_argument("output_file", help="Path to the output .csv file")
    
    args = parser.parse_args()
    
    convert_xlsx_to_csv(args.input_file, args.output_file)
