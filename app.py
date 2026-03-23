import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- CORE APIs ---
@st.cache_data(show_spinner=False) # Caches the data so it doesn't reload on every click
def get_vep_annotation(chrom, pos, alt_allele):
    server = "https://grch37.rest.ensembl.org"
    endpoint = f"/vep/human/region/{chrom}:{pos}-{pos}:1/{alt_allele}"
    try:
        response = requests.get(server + endpoint, headers={"Content-Type": "application/json"}, timeout=10)
        if response.ok:
            data = response.json()[0]
            cons = data.get('most_severe_consequence', 'Unknown').replace('_', ' ').upper()
            trans = data.get('transcript_consequences', [{}])[0]
            return cons, trans.get('gene_symbol', 'Unknown'), trans.get('amino_acids', 'N/A'), trans.get('protein_start', 'N/A')
        return "API Error", "Unknown", "N/A", "N/A"
    except:
        return "Offline", "Unknown", "N/A", "N/A"

@st.cache_data(show_spinner=False)
def predict_binding(allele, gene, aa_change):
    if aa_change == 'N/A' or '/' not in aa_change: return 9999.0
    mutant_aa = aa_change.split('/')[-1]
    
    valid_aa = "ACDEFGHIKLMNPQRSTVWY"
    if mutant_aa not in valid_aa: mutant_aa = 'A'
        
    peptide = (mutant_aa + "SIYRYYGL")[:9]
    url = "http://tools-cluster-interface.iedb.org/tools_api/mhci/"
    payload = {"method": "smm", "sequence_text": peptide, "allele": allele, "length": "9"}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.post(url, data=payload, headers=headers, timeout=15)
        if res.ok:
            lines = res.text.strip().split('\n')
            if len(lines) > 1:
                col_headers = lines[0].split('\t')
                vals = lines[1].split('\t')
                if 'ic50' in col_headers:
                    return round(float(vals[col_headers.index('ic50')]), 2)
        return 9999.0
    except:
        return 9999.0

# --- G.U.L.B.I.A. FULL DASHBOARD UI ---
st.set_page_config(page_title="G.U.L.B.I.A. Clinical Suite", layout="wide", page_icon="🧬")

# Sidebar Controls
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50) # Generic DNA icon
    st.title("Control Panel")
    hla = st.selectbox("Target HLA-Allele", ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02"])
    batch_size = st.slider("Variants to Analyze (Batch Size)", min_value=1, max_value=20, value=5, help="Keep under 20 to prevent IEDB API timeouts.")
    st.markdown("---")
    st.caption("G.U.L.B.I.A. Engine v2.0 | Liver Core")

st.title("🧬 G.U.L.B.I.A. Clinical Dashboard")
st.markdown("Analyze raw patient genomic data to identify high-affinity neoantigen vaccine targets.")

vcf_file = st.file_uploader("Upload Patient Sequence (VCF/MAF)", type=["vcf", "maf"])

if vcf_file:
    # 1. Parsing Phase
    is_maf = vcf_file.name.endswith(".maf")
    df_raw = pd.read_csv(vcf_file, sep="\t", comment="#", low_memory=False)
    
    if is_maf and 'Variant_Classification' in df_raw.columns:
        df_clean = df_raw[df_raw['Variant_Classification'] == 'Missense_Mutation']
    else:
        df_clean = df_raw
        
    variants = df_clean.head(batch_size) 
    
    if variants.empty:
        st.error("No valid protein-altering mutations found.")
    else:
        # UI Metrics Layout
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Mutations Detected", f"{len(df_raw):,}")
        col2.metric("Filtered Missense Targets", f"{len(df_clean):,}")
        col3.metric("Current Batch Processing", len(variants))
        
        # 2. Analysis Phase
        results = []
        progress_text = "Pinging Ensembl & IEDB Neural Nets..."
        my_bar = st.progress(0, text=progress_text)
        
        for count, (i, row) in enumerate(variants.iterrows()):
            my_bar.progress((count + 1) / len(variants), text=f"Processing Target {count+1}/{len(variants)}...")
            
            chrom = str(row.get('Chromosome', '')) if is_maf else str(row.iloc[0])
            pos = str(row.get('Start_Position', '')) if is_maf else str(row.iloc[1])
            alt = str(row.get('Tumor_Seq_Allele2', '')) if is_maf else str(row.iloc[4]).split(',')[0]
            
            cons, gene, aa, p_pos = get_vep_annotation(chrom.replace('chr',''), pos, alt)
            score = predict_binding(hla, gene, aa)
            results.append({"Target Gene": gene, "Consequence": cons, "Amino Acid Change": f"{aa}@{p_pos}", "IC50 (nM)": score})

        my_bar.empty() # Clear progress bar when done
        
        # 3. Data Formatting
        final_df = pd.DataFrame(results).sort_values("IC50 (nM)")
        
        st.subheader("📋 Ranked Clinical Targets")
        st.dataframe(final_df, use_container_width=True)
        
        # 4. Data Visualization (Plotly)
        st.subheader("📊 Immunogenicity Landscape")
        # Filter out 9999 errors for a clean graph
        graph_df = final_df[final_df["IC50 (nM)"] < 9999.0]
        
        if not graph_df.empty:
            fig = px.bar(graph_df, x="Target Gene", y="IC50 (nM)", 
                         color="IC50 (nM)", color_continuous_scale="Viridis_r",
                         title="Binding Affinity by Gene (Lower IC50 = Stronger Vaccine Target)")
            fig.add_hline(y=500, line_dash="dash", line_color="red", annotation_text="Strong Binder Threshold (<500nM)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No valid binding scores retrieved to generate graph.")
            
        # 5. Export Engine
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Liver Vaccine Blueprint (CSV)",
            data=csv,
            file_name='gulbia_patient_blueprint.csv',
            mime='text/csv',
        )