import requests
import sys

# The Ensembl REST API endpoint for human gene lookups
server = "https://rest.ensembl.org"
endpoint = "/lookup/symbol/human/TP53?expand=1"

print("📡 Pinging Ensembl Genomic Database...")

# Sending the request to the server
response = requests.get(server + endpoint, headers={"Content-Type": "application/json"})

if response.ok:
    data = response.json()
    print("\n✅ Success! Database Handshake Established.")
    print("-" * 30)
    print(f"🧬 Target Gene:   {data['display_name']}")
    print(f"🆔 Ensembl ID:    {data['id']}")
    print(f"📍 Location:      Chromosome {data['seq_region_name']}")
    print(f"📏 Coordinates:   {data['start']} to {data['end']}")
    print(f"🔬 Biotype:       {data['biotype']}")
    print("-" * 30)
else:
    print(f"\n❌ Connection Failed. Error Code: {response.status_code}")
    sys.exit()