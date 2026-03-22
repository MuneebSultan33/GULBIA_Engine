import pandas as pd
import os

def get_vcf_data(filepath):
    # This loop finds exactly which line the data starts on (the one starting with #CHROM)
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('#CHROM'):
                return i
    return 0

print("--- GULBIA Stress-Test Engine ---")
target_file = "data_samples/HCC_Sample_Large.vcf"

if os.path.exists(target_file):
    header_index = get_vcf_data(target_file)
    print(f"Header found at line {header_index}. Processing...")
    
    # Now we load the data using the automatically discovered header line
    df = pd.read_csv(target_file, sep='\t', skiprows=header_index)
    
    # Let's see the full table of mutations
    print(df[['#CHROM', 'POS', 'REF', 'ALT', 'INFO']])
else:
    print("File not found.")