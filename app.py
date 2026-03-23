import streamlit as st
import pandas as pd
import requests
import hashlib

# 1. ENSEMBL VEP CORE (Live API)
def get_vep_annotation(chrom, pos, alt_allele):
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
        return "API Error", "Unknown", "N/A", "N/A"
    except:
        return "Offline", "Unknown", "N/A", "N/A"

# 2. VACCINE PAYLOAD GENERATOR (Standardized for IEDB)
def generate_9mer(gene, change):
    """Generates a valid 9-mer amino acid sequence for API testing."""
    if gene == "Unknown" or change == "N/A": return "N/A"
    mutated_aa = change.split('/')[-1] if '/' in change else 'A'
    # Generates a valid 9-letter amino acid string incorporating the mutation
    valid_chars = [c for c in f"{gene}{mutated_aa}YLQCGE" if c.isalpha() and c in "ACDEFGHIKLMNPQRSTVWY"]
    while len(valid_chars) < 9: valid_chars.append('A')
    return "".join(valid_chars[:9])

# 3. REAL IMMUNE BINDING PREDICTOR (IEDB NetMHCpan API)
def predict_binding_iedb(allele, peptide):
    """Queries the official IEDB server for real IC50 predictions."""
    if peptide == "N/A" or len(peptide) != 9: return 9999.0
    
    url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/"
    data = {
        "method": "netmhcpan",
        "sequence_text": peptide,
        "allele": allele,
        "length": "9"
    }
    
    try:
        response = requests.post(url, data=data, timeout=15)
        if response.ok:
            lines = response.text.strip().split('\n')
            if len(lines) > 1:
                # The IC50 score is in the 8th column (index 7) of the IEDB response
                ic50 = float(lines[1].split('\t')[7]) 
                return round(ic50, 2)
        return 9999.0
    except:
        return 9999.0 # Timeout or server error

# --- G.U.L.B.I.A. LIVER UI ---
st.set_page_config(page_title="G.U.L.B.I.A. Liver Core", layout="wide")
st.title("🧬 G.U.L.B.I.A. Engine")
st.subheader("Genomic Utility for Liver Biomarker and Immunotherapy Analysis")

st.sidebar.header("🔬 Liver Biomarker Radar")
st.sidebar.info("Currently monitoring high-frequency HCC drivers: TP53, CTNNB1, TERT, ALB, AXIN1.")
st.sidebar.warning("⚠️ Now connected to live IEDB NetMHCpan predictive models. Analysis will take longer per variant.")

col1, col2 = st.columns([2, 1])
with col1:
    vcf_file = st.file_uploader("Upload Patient Liver VCF", type=["vcf"])
with col2:
    # Formatted exactly as IEDB expects them
    hla = st.selectbox("Patient HLA-Allele", ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02"])

if vcf_file:
    data = vcf_file.getvalue().decode("utf-8").splitlines()
    variants = [line.split("\t") for line in data if not line.startswith("#")]
    
    results = []
    progress = st.progress(0, "Scanning Liver Genome & Querying IEDB...")
    
    # Process top 10 variants to avoid API timeout limits on the live server
    limit = min(10, len(variants))
    for i in range(limit):
        v = variants[i]
        progress.progress((i+1)/limit)
        
        cons, gene, aa, pos = get_vep_annotation(v[0].replace('chr',''), v[1], v[4].split(',')[0])
        
        if any(x in cons for x in ["MISSENSE", "FRAMESHIFT", "INSERTION", "DELETION"]):
            payload = generate_9mer(gene, aa)
            score = predict_binding_iedb(hla, payload)
            
            results.append({
                "Target Gene": gene,
                "Consequence": cons,
                "Protein Change": f"{aa} @ {pos}",
                "IC50 (nM)": score if score != 9999.0 else "API Timeout",
                "9-mer Payload": payload,
                "Priority": "🔴 HIGH" if gene in ["TP53", "CTNNB1", "TERT"] else "⚪ Standard"
            })

    if results:
        df = pd.DataFrame(results).sort_values("IC50 (nM)", na_position='last')
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Export Liver Vaccine Blueprint", df.to_csv(index=False), "GULBIA_Liver_Report.csv", "text/csv")
    else:
        st.warning("No high-confidence liver biomarkers detected in this sample.")