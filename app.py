import streamlit as st
import pandas as pd
import requests

# 1. ENSEMBL VEP CORE (Unified for VCF & MAF)
def get_vep_annotation(chrom, pos, alt_allele):
    server = "https://rest.ensembl.org"
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

# 2. BINDING PREDICTOR (IEDB API)
def predict_binding(allele, gene, change):
    mut_aa = change.split('/')[-1] if '/' in change else 'A'
    peptide = (f"{gene}{mut_aa}YLQCGE"[:9]).ljust(9, 'A')
    url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/"
    payload = {"method": "netmhcpan", "sequence_text": peptide, "allele": allele, "length": "9"}
    try:
        res = requests.post(url, data=payload, timeout=10)
        return round(float(res.text.strip().split('\n')[1].split('\t')[7]), 2) if res.ok else 9999.0
    except:
        return 9999.0

# --- G.U.L.B.I.A. HYBRID UI ---
st.set_page_config(page_title="G.U.L.B.I.A. Liver Core", layout="wide")
st.title("🧬 G.U.L.B.I.A. Engine")
st.subheader("Clinical Liver Biomarker Analysis (VCF/MAF Hybrid)")

vcf_file = st.file_uploader("Upload Patient Data (VCF or MAF)", type=["vcf", "maf"])
hla = st.selectbox("HLA-Allele", ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02"])

if vcf_file:
    # Detect File Type
    is_maf = vcf_file.name.endswith(".maf")
    df_raw = pd.read_csv(vcf_file, sep="\t", comment="#", low_memory=False)
    
    results = []
    # Process top 5 variants to keep the API from timing out during testing
    variants = df_raw.head(5)
    progress = st.progress(0, "Analyzing Clinical Targets...")

    for i, row in variants.iterrows():
        progress.progress((i+1)/5)
        
        # Dynamic Mapping: MAF vs VCF
        if is_maf:
            chrom = str(row.get('Chromosome', ''))
            pos = str(row.get('Start_Position', ''))
            alt = str(row.get('Tumor_Seq_Allele2', ''))
        else:
            chrom = str(row.iloc[0])
            pos = str(row.iloc[1])
            alt = str(row.iloc[4]).split(',')[0]
        
        cons, gene, aa, p_pos = get_vep_annotation(chrom.replace('chr',''), pos, alt)
        score = predict_binding(hla, gene, aa)
        
        results.append({"Target": gene, "Type": cons, "Change": f"{aa}@{p_pos}", "IC50": score})

    st.table(pd.DataFrame(results))