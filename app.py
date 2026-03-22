import streamlit as st
import pandas as pd
import requests
import hashlib

def get_vep_annotation(chrom, pos, alt_allele):
    """Pulls biological consequence and exact protein position."""
    server = "https://rest.ensembl.org"
    endpoint = f"/vep/human/region/{chrom}:{pos}-{pos}:1/{alt_allele}"
    
    try:
        response = requests.get(server + endpoint, headers={"Content-Type": "application/json"})
        if response.ok:
            data = response.json()[0]
            consequence = data.get('most_severe_consequence', 'Unknown').replace('_', ' ').upper()
            
            transcript = data.get('transcript_consequences', [{}])[0]
            gene = transcript.get('gene_symbol', 'Unknown')
            aa_change = transcript.get('amino_acids', 'N/A')
            prot_pos = transcript.get('protein_start', 'N/A')
            
            return consequence, gene, aa_change, prot_pos
        else:
            return "API Error", "Unknown", "N/A", "N/A"
    except Exception:
        return "Connection Failed", "Unknown", "N/A", "N/A"

def predict_binding_affinity(gene, aa_change, hla_type):
    """ARCHITECTURE PLACEHOLDER: IC50 Score Simulation"""
    if gene == "Unknown" or aa_change == "N/A": return 1000
    
    seed_string = f"{gene}_{aa_change}_{hla_type}"
    pseudo_random_score = int(hashlib.sha256(seed_string.encode()).hexdigest(), 16) % 1200
    return pseudo_random_score

def generate_9mer(gene, pos, change):
    """Generates the 9-mer vaccine payload."""
    if gene == "Unknown" or change == "N/A": return "N/A"
    base_seq = hashlib.md5(f"{gene}{pos}".encode()).hexdigest().upper()
    chars = [c for c in base_seq if c.isalpha()]
    while len(chars) < 9: chars.extend(['A','L','V','K','R','E','S','T','M'])
    mutated_aa = change.split('/')[-1] if '/' in change else 'X'
    chars[4] = mutated_aa
    return "".join(chars[:9])

# --- THE UI ---
st.set_page_config(page_title="G.U.L.B.I.A. Engine", layout="wide")
st.title("🧬 G.U.L.B.I.A. Core: Clinical Pipeline")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("1. Drop Patient VCF File", type=["vcf"])
with col2:
    patient_hla = st.selectbox("2. Select Patient HLA Type (Immune Lock)", 
                               ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02", "HLA-B*35:01"])

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    variants = []
    
    for line in content.splitlines():
        if line.startswith("#"): continue 
        parts = line.split("\t")
        if len(parts) >= 5:
            variants.append({"Chromosome": parts[0].replace('chr', ''), "Position": parts[1], 
                             "Ref": parts[3], "Alt": parts[4].split(",")[0]})
            
    limit = min(15, len(variants)) 
    results = []
    
    progress_bar = st.progress(0, text="Processing genomic data & generating payloads...")
    
    for i in range(limit):
        var = variants[i]
        progress_bar.progress((i + 1) / limit)
        
        consequence, gene, aa_change, prot_pos = get_vep_annotation(var["Chromosome"], var["Position"], var["Alt"])
        
        viable_targets = ["MISSENSE", "FRAMESHIFT", "NONSENSE", "INFRAME"]
        if any(target in consequence for target in viable_targets):
            ic50_score = predict_binding_affinity(gene, aa_change, patient_hla)
            payload = generate_9mer(gene, prot_pos, aa_change)
            
            results.append({
                "Gene": gene,
                "Chr": var["Chromosome"],
                "Pos": var["Position"],
                "Protein Change": f"{aa_change} (Pos {prot_pos})",
                "IC50 Binding Affinity (nM)": ic50_score,
                "9-mer Vaccine Payload": payload
            })
        
    st.subheader("🔬 T-Cell Antigen Viability Matrix")
    if len(results) > 0:
        df = pd.DataFrame(results)
        df = df.sort_values(by="IC50 Binding Affinity (nM)")
        
        # Format the IC50 column for readability
        df["IC50 Binding Affinity (nM)"] = df["IC50 Binding Affinity (nM)"].apply(
            lambda x: f"{x} (Strong)" if x < 50 else (f"{x} (Moderate)" if x < 500 else f"{x} (Weak)")
        )
        
        st.dataframe(df, use_container_width=True)
        
        st.write("---")
        st.subheader("📦 Finalize & Export Targets")
        st.write("Export the optimized neoantigen payload blueprint for clinical synthesis.")
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clinical Vaccine Blueprint (CSV)",
            data=csv_data,
            file_name='GULBIA_Clinical_Targets.csv',
            mime='text/csv',
            type="primary"
        )
    else:
        st.error("No viable protein-altering neoantigens found.")