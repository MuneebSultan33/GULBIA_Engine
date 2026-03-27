import React from 'react';

const UserProfile = () => {
  return (
    <div className="Profile-Container Inter-Font Fade-In">
      
      {/* 1. Top Hero Section (Inline Background Image is Safe) */}
      <div className="Profile-Hero" style={{ backgroundImage: "url('/profile-bg.jpg')" }}>
        <div className="Profile-Hero-Overlay"></div>
        
        <h1 className="Profile-Hero-Text Instrument-Font">
          Lead Architect &<br/>Computational<br/>Biotechnologist
        </h1>
        
        <div className="Profile-Image-Wrapper">
          <img src="/muneeb-profile.jpg" alt="Muhammad Muneeb Sultan" />
        </div>
      </div>

      {/* 2. Middle Biography Section */}
      <div className="Profile-Bio-Block">
        <h2 className="Instrument-Font">Biography:</h2>
        <p>
          Muhammad Muneeb Sultan is a biotechnology researcher specializing in structural bioinformatics, computational virology, and AI-driven vaccine design. Currently an undergraduate at the University of Veterinary and Animal Sciences (UVAS) in Lahore Pakistan, his work bridges the gap between raw genomic data and clinical immunology.
        </p>
        <p>
          His core research focuses on leveraging dry-lab techniques, including Whole Genome Sequence (WGS) analysis, molecular docking, and Python scripting to process complex biological datasets for precision medicine. He is the lead author of an upcoming review on Artificial Intelligence-based mRNA vaccine solutions for the CCHF Virus, building on advanced certifications in Vaccinology and Immunology from Imperial College London. The GULBIA Engine represents the culmination of his focus on automating and optimizing the neoantigen discovery pipeline.
        </p>
      </div>

      {/* 3. Bottom Competencies Section */}
      <div className="Profile-Comp-Block">
        <h2 className="Instrument-Font">Core<br/>Competencies:</h2>
        
        <ul className="Profile-Comp-List">
          <li><strong>Genomics & Sequence Analysis:</strong> Whole Genome Sequence (WGS) assembly, annotation, and phylogenetic mapping (NCBI BLAST, MEGA-X).</li>
          <li><strong>Structural Bioinformatics:</strong> Protein tertiary structure prediction, complex molecular docking (AutoDock Vina, ClusPro), and 3D interaction visualization (PyMol).</li>
          <li><strong>Computational Engineering:</strong> Python scripting for biological data processing, algorithm design, and pipeline automation.</li>
          <li><strong>Wet-Lab Fundamentals:</strong> DNA/RNA extraction, primary cell culturing, and strict aseptic techniques.</li>
        </ul>
      </div>

    </div>
  );
};

export default UserProfile;