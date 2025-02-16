import pandas as pd
import numpy as np
import yaml
import sys

def assign_sample_id(samples_data, lab_id_col="lab_id", personal_id_col="personal_id", date_col="date", verbose=True):
    # Check if the specified columns exist in the incoming data frame
    required_cols = [lab_id_col, personal_id_col, date_col]
    if not all(col in samples_data.columns for col in required_cols):
        raise ValueError(f"The data frame must contain the specified columns: {', '.join(required_cols)}")
    
    if verbose:
        print("Converting date column to Date type...")
    # Convert date column to Date type if it's not already
    samples_data[date_col] = pd.to_datetime(samples_data[date_col])
    
    # Define helper functions
    # Step 1 - Add sample IDs based on personal identification numbers
    def add_sample_id(incoming_data):
        if verbose:
            print("Assigning unique sample IDs based on personal identification numbers...")
        
        # Create a unique identifier for each unique personal_id
        unique_ids = incoming_data[[personal_id_col]].drop_duplicates().reset_index(drop=True)
        unique_ids['sample_id'] = ["USQ_{:05d}".format(i + 1) for i in range(len(unique_ids))]
        
        # Join the unique sample IDs back to the original data
        incoming_data = incoming_data.merge(unique_ids, on=personal_id_col, how='left')
        
        return incoming_data
    
    # Step 2 - Add suffix for multiple tumor samples
    def add_tumor_suffix(incoming_data):
        if verbose:
            print("Adding suffixes for multiple tumor samples with different dates...")
        
        # Add suffixes for samples with the same sample_id but different dates
        incoming_data = incoming_data.sort_values(by=[lab_id_col, date_col])
        incoming_data['suffix'] = incoming_data.groupby('sample_id').cumcount().apply(lambda x: "" if x == 0 else chr(65 + x))
        incoming_data['sample_id'] = incoming_data.apply(lambda row: row['sample_id'] + row['suffix'], axis=1)
        incoming_data.drop(columns=['suffix'], inplace=True)
        
        return incoming_data
    
    # Step 3 - Add suffix for duplicated samples
    def add_repl_suffix(incoming_data):
        if verbose:
            print("Adding suffixes for duplicated samples with the same personal ID and date...")
        
        # Add suffixes for samples with the same personal_id and date
        incoming_data = incoming_data.sort_values(by=[lab_id_col])
        incoming_data['suffix'] = incoming_data.groupby([personal_id_col, date_col]).cumcount().apply(lambda x: "" if x == 0 else f"_{x}")
        incoming_data['sample_id'] = incoming_data.apply(lambda row: row['sample_id'] + row['suffix'], axis=1)
        incoming_data.drop(columns=['suffix'], inplace=True)
        
        return incoming_data
    
    # Run helpers
    sample_ids = add_sample_id(samples_data)
    sample_ids_tumor = add_tumor_suffix(sample_ids)
    sample_ids_tumour_repl = add_repl_suffix(sample_ids_tumor)
    
    if verbose:
        print("Sample ID assignment complete.")
    
    return sample_ids_tumour_repl

if __name__ == "__main__":
    # Load configuration
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    
    input_file = config["input_file"]
    output_file = config["output_file"]

    # Read the data from the input file
    samples_data = pd.read_csv(input_file, sep="\t")

    # Process the data
    result = assign_sample_id(samples_data)

    # Write the resulting DataFrame to the output file
    result.to_csv(output_file, sep="\t", index=False)
    