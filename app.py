import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- G.U.L.B.I.A. CUSTOM MAROON THEME & ANIMATIONS ---
st.set_page_config(page_title="G.U.L.B.I.A. Clinical Suite", layout="wide", page_icon="🧬")

custom_css = """
<style>
    /* Deep Maroon Backgrounds */
    .stApp {
        background-color: #1a0505;
        color: #f5f5f5;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2b0000;
        border-right: 1px solid #4a0000;
    }

    /* Smooth Fade-In Animation for the main container */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .main .block-container {
        animation: fadeInUp 0.8s ease-out;
    }

    /* Animated Buttons */
    div.stButton > button {
        background-color: #800000 !important;
        color: white !important;
        border: 1px solid #ff4d4d !important;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background-color: #b30000 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 77, 77, 0.2);
    }
    
    /* Progress Bar Maroon Override */
    .stProgress > div > div > div > div {
        background-color: #cc0000;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CORE APIs ---
@st.cache_data(show_spinner=False)
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

# --- UI LAYOUT ---
with st.sidebar:
    st.title("🩸 Control Panel")
    hla = st.selectbox("Target HLA-Allele", ["HLA-A*02:01", "HLA-A*24:02", "HLA-B*07:02"])
    batch_size = st.slider("Variants to Analyze (Batch Size)", min_value=1, max_value=20, value=5)
    st.markdown("---")
    st.caption("G.U.L.B.I.A. Engine v3.0 | Pro Edition")

st.title("🧬 G.U.L.B.I.A. Clinical Dashboard")
st.markdown("### Next-Generation Liver Neoantigen Discovery")

vcf_file = st.file_uploader("Upload Patient Sequence (VCF/MAF)", type=["vcf", "maf"])

if vcf_file:
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
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Mutations", f"{len(df_raw):,}")
        col2.metric("Missense Targets", f"{len(df_clean):,}")
        col3.metric("Batch Processing", len(variants))
        
        results = []
        my_bar = st.progress(0, text="Pinging Neural Nets...")
        
        for count, (i, row) in enumerate(variants.iterrows()):
            my_bar.progress((count + 1) / len(variants), text=f"Processing Target {count+1}/{len(variants)}...")
            chrom = str(row.get('Chromosome', '')) if is_maf else str(row.iloc[0])
            pos = str(row.get('Start_Position', '')) if is_maf else str(row.iloc[1])
            alt = str(row.get('Tumor_Seq_Allele2', '')) if is_maf else str(row.iloc[4]).split(',')[0]
            
            cons, gene, aa, p_pos = get_vep_annotation(chrom.replace('chr',''), pos, alt)
            score = predict_binding(hla, gene, aa)
            results.append({"Target Gene": gene, "Consequence": cons, "Amino Acid Change": f"{aa}@{p_pos}", "IC50 (nM)": score})

        my_bar.empty() 
        final_df = pd.DataFrame(results).sort_values("IC50 (nM)")
        
        st.subheader("📋 Ranked Clinical Targets")
        st.dataframe(final_df, use_container_width=True)
        
        st.subheader("📊 Immunogenicity Landscape")
        graph_df = final_df[final_df["IC50 (nM)"] < 9999.0]
        
        if not graph_df.empty:
            # Customized the Plotly graph to match the maroon theme
            fig = px.bar(graph_df, x="Target Gene", y="IC50 (nM)", 
                         color="IC50 (nM)", color_continuous_scale="Reds_r",
                         title="Binding Affinity by Gene")
            fig.update_layout(plot_bgcolor='#1a0505', paper_bgcolor='#1a0505', font_color='#f5f5f5')
            fig.add_hline(y=500, line_dash="dash", line_color="#ff4d4d", annotation_text="Strong Binder (<500nM)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Fire a success toast animation
            st.toast('Analysis Complete! Targets acquired.', icon='🎯')
        else:
            st.warning("No valid binding scores retrieved to generate graph.")
            
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Vaccine Blueprint",
            data=csv,
            file_name='gulbia_blueprint.csv',
            mime='text/csv',
        )