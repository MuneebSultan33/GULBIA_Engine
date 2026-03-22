import requests
import sys

server = "https://rest.ensembl.org"
# The VEP API endpoint. Format: /region/chromosome:start-end:strand/mutated_allele
# This simulates a VCF line: Chr 7, Position 140753336, mutating to 'T'
endpoint = "/vep/human/region/7:140753336-140753336:1/T"

print("🧬 Transmitting raw VCF coordinate to Ensembl VEP...")

response = requests.get(server + endpoint, headers={"Content-Type": "application/json"})

if response.ok:
    data = response.json()[0]
    print("\n✅ VEP Translation Complete.")
    print("-" * 45)
    print(f"📍 VCF Location:    Chromosome {data['seq_region_name']}, Pos {data['start']}")
    print(f"⚠️  Consequence:     {data['most_severe_consequence'].replace('_', ' ').upper()}")
    
    # We dig into the transcript data to find the exact amino acid change
    transcript = data['transcript_consequences'][0]
    if 'amino_acids' in transcript:
        print(f"🎯 Protein Target:  Gene {transcript.get('gene_symbol', 'Unknown')}")
        print(f"🧩 Amino Acid Hit:  {transcript['amino_acids']} (Codon Position {transcript.get('protein_start', 'N/A')})")
    print("-" * 45)
else:
    print(f"\n❌ VEP Engine Failed. Error Code: {response.status_code}")
    sys.exit()