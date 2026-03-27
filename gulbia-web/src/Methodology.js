import React from 'react';

const Methodology = () => {
  return (
    <div className="Meth-Container Inter-Font Fade-In">
      
      {/* Block 1: Dark Red Hero */}
      <div className="Meth-Hero">
        <h1 className="Meth-Hero-Text Inter-Font">The GULBIA<br/>Pipeline: From<br/>Tumor to Therapy</h1>
      </div>

      {/* Block 2: Deep Red (Core Concept) */}
      <div className="Meth-Block Meth-Red">
        <h2 className="Inter-Font">Core Concept:</h2>
        <p>GULBIA operates on a deterministic, four-stage bioinformatics pipeline designed to isolate immunogenic neoantigens from Hepatocellular Carcinoma (HCC) somatic mutation data.</p>
      </div>

      {/* Block 3: Dark Grey (Phase 1) */}
      <div className="Meth-Block Meth-Dark">
        <h2 className="Inter-Font">Phase 1: Genomic Parsing &<br/>Translation</h2>
        <p>The engine ingests standard clinical variant files (MAF/VCF). It isolates non-synonymous passenger mutations and performs *in silico* translation to generate mutated 9-mer peptide sequences representing the tumor's unique proteomic signature.</p>
      </div>

      {/* Block 4: Salmon Pink (Phase 2) */}
      <div className="Meth-Block Meth-Pink">
        <h2 className="Inter-Font">Phase 2: Neural MHC-I<br/>Binding Prediction</h2>
        <p>Not all mutations are visible to the immune system. GULBIA utilizes predictive algorithms to calculate the binding affinity (IC50 scores) of these peptides against specific patient Human Leukocyte Antigen (HLA) alleles (e.g., HLA-A*02:01).</p>
        
        {/* Indented Text to match Canva layout */}
        <p className="Align-Right-Text">
          Selection Threshold: Only peptides demonstrating strong binding affinity (&lt; 500 nM) are classified as viable targets.
        </p>
      </div>

      {/* Block 5: Deep Red (Phase 3) */}
      <div className="Meth-Block Meth-Red">
        <h2 className="Inter-Font">Phase 3: Multi-Epitope<br/>Construct Assembly</h2>
        <p>The highest-ranking neoantigens are automatically aggregated into a continuous mRNA/peptide vaccine blueprint.</p>
        
        {/* Indented Text to match Canva layout */}
        <p className="Align-Right-Text" style={{color: '#fff'}}>
          Molecular Engineering: The system inserts rigid (EAAAK) and flexible (GPGPG) linkers to ensure proper protein folding and attaches a beta-defensin adjuvant sequence to stimulate toll-like receptors and boost immune response.
        </p>
      </div>

    </div>
  );
};

export default Methodology;