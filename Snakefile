# Load configuration
configfile: "config.yaml"

rule all:
    input:
        config["output_file"]

rule process_data:
    input:
        config["input_file"]
    output:
        config["output_file"]
    script:
        "scripts/assign_sample_ids.py"