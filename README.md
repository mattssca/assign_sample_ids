# Snakemake Workflow for Assigning Sample IDs

This Snakemake workflow assigns unique sample IDs to a data frame of samples based on personal identification numbers, dates, and lab IDs. It adds suffixes to sample IDs for multiple tumor samples and duplicated samples.

## Directory Structure

```
assign_sample_ids/
├── Snakefile
├── config.yaml
├── data
│   └── (optional) input_data.txt
├── output
├── scripts
│   └── assign_sample_ids.py
```

## Setup

1. **Install Conda**: If you don't have Conda installed, you can download and install it from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

2. **Create a Conda Environment**: Create a new Conda environment with the required packages.

   ```sh
   conda create -n assign_sample_ids_env python=3.10 snakemake pandas numpy pyyaml
   conda activate assign_sample_ids_env
   ```

3. **Clone the Repository**: Clone this repository to your local machine.

   ```sh
   git clone https://github.com/mattssca/assign_sample_ids.git
   cd assign_sample_ids
   ```

4. **Edit the Configuration File**: Edit the `config.yaml` file to specify the input and output file paths.

   ```yaml
   input_file: "path/to/your/input_data.txt"
   output_file: "output/processed_data.txt"
   ```

## Running the Workflow

1. **Run Snakemake**: Navigate to the directory containing the `Snakefile` and run Snakemake with the specified number of cores.

   ```sh
   snakemake --cores all
   ```

   Alternatively, you can specify the number of cores to use (e.g., 4 cores):

   ```sh
   snakemake --cores 4
   ```

2. **Check the Output**: The processed data will be saved to the output file specified in the `config.yaml` file.

## Files

- `Snakefile`: The Snakemake workflow definition.
- `config.yaml`: Configuration file specifying input and output file paths.
- `data/input_data.txt`: Example input data file (optional).
- `scripts/assign_sample_ids.py`: Python script for processing the data.

## Example Usage

```sh
# Create and activate the Conda environment
conda create -n snakemake_env python=3.10 snakemake pandas numpy pyyaml
conda activate snakemake_env

# Clone the repository and navigate to the directory
git clone <repository_url>
cd assign_sample_ids

# Edit the configuration file to specify your own input file
nano config.yaml

# Run the Snakemake workflow
snakemake --cores all
```

## License

This project is licensed under the MIT License.