import streamlit as st
import pandas as pd
import requests

# 1. ENSEMBL VEP CORE (GRCh37)
def get_vep_annotation(chrom, pos, alt_allele):
    server = "https://grch37.rest.ensembl.org"
    endpoint = f"/vep/human/region/{chrom}:{pos}-{pos}:1/{alt_allele}"
    try:
        response = requests.get(server + endpoint, headers={"Content-Type": "application/json"})
        if response.ok:
            data = response.json()[0]
            cons = data.get('most_severe_consequence', 'Unknown').replace('_', ' ').upper()
            trans = data.get('transcript_consequences', [{}])[0]
            return cons, trans.get('gene_symbol', 'Unknown'), trans.get('amino_acids', 'N/A'), trans.get('protein_start', 'N/A')
        return "API Error", "Unknown", "N/A", "N/A"
    except:
        return "Offline", "Unknown", "N/A", "N/A"

# 2. PRO BINDING PREDICTOR (9-mer Construction)
def predict_binding(allele, gene, aa_change):
    if aa_change == 'N/A' or '/' not in aa_change: return 9999.0
    
    # Extract the mutant amino acid (e.g., 'K' from 'E/K')
    mutant_aa = aa_change.split('/')[-1]
    
    # Construct a valid 9-mer peptide window (Placeholder logic for demo)
    # In a full clinical tool, we'd fetch the actual protein context here
    placeholder_backbone = "SIYRYYGL" # A common high-binder scaffold
    peptide = (mutant_aa + placeholder_backbone)[:9]
    
    url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/"
    payload = {"method": "netmhcpan", "sequence_text": peptide, "allele": allele, "length": "9"}
    try:
        res = requests.post(url, data=payload, timeout=10)
        if res.ok:
            # Extract IC50 from the IEDB response table
            return round(float(res.text.strip().split('\n')[1].split('\t')[7]), 2)
        return 9999.0
    except:
        return 9999.0

# --- G.U.L.B.I.A. UI ---
st.set_page_config(page_title="G.U.L.B.I.A. Liver Core", layout="wide")
st.title("🧬 G.U.L.B.I.A. Engine")
st.subheader("Clinical Liver Biomarker Analysis (VCF/MAF Hybrid)")

vcf_file = st.file_uploader("Upload Patient Data (VCF or MAF)", type=["vcf", "maf"])
hla = st.selectbox("HLA-Allele", ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02"])

if vcf_file:
    is_maf = vcf_file.name.endswith(".maf")
    df_raw = pd.read_csv(vcf_file, sep="\t", comment="#", low_memory=False)
    
    if is_maf and 'Variant_Classification' in df_raw.columns:
        df_clean = df_raw[df_raw['Variant_Classification'] == 'Missense_Mutation']
    else:
        df_clean = df_raw
        
    results = []
    variants = df_clean.head(5) 
    
    if not variants.empty:
        progress = st.progress(0, "Analyzing Clinical Targets...")
        for count, (i, row) in enumerate(variants.iterrows()):
            progress.progress((count + 1) / len(variants))
            
            chrom = str(row.get('Chromosome', '')) if is_maf else str(row.iloc[0])
            pos = str(row.get('Start_Position', '')) if is_maf else str(row.iloc[1])
            alt = str(row.get('Tumor_Seq_Allele2', '')) if is_maf else str(row.iloc[4]).split(',')[0]
            
            cons, gene, aa, p_pos = get_vep_annotation(chrom.replace('chr',''), pos, alt)
            score = predict_binding(hla, gene, aa)
            results.append({"Target": gene, "Type": cons, "Change": f"{aa}@{p_pos}", "IC50 (nM)": score})

        st.table(pd.DataFrame(results).sort_values("IC50 (nM)"))