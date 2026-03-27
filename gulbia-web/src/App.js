import React, { useState, useEffect } from 'react';
import './App.css';

import Methodology from './Methodology';
import Documentation from './Documentation';
import UserProfile from './UserProfile';
import Contact from './Contact';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState(null);
  const [vaccineData, setVaccineData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const [patientId] = useState("HC-9912");
  const [hlaAllele, setHlaAllele] = useState("HLA-A*02:01");
  const [activePage, setActivePage] = useState('Home');

  useEffect(() => {
    const handlePopState = (event) => {
      if (!event.state || !event.state.onDashboard) {
        setActivePage('Home');
        setResults(null); 
        setVaccineData(null);
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const handleEnterWorkspace = () => {
    window.history.pushState({ onDashboard: true }, '');
    setActivePage('Workspace'); 
    window.scrollTo(0, 0); 
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return alert("Please select a valid clinical file first.");
    setIsLoading(true);
    setResults(null); 
    setVaccineData(null); 
    
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("hla_allele", hlaAllele);
    formData.append("batch_size", 50000); 

    try {
      const response = await fetch("http://localhost:8000/analyze/", { 
        method: "POST", 
        body: formData 
      });
      const data = await response.json();
      
      setResults(data.analysis_results);
      setVaccineData(data.vaccine_construct); 
      
    } catch (error) {
      alert("SYSTEM OFFLINE: Make sure your Python (Uvicorn) backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!results) return;
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Target Gene,Mutation Variant,Peptide Sequence,HLA Allele,IC50 Affinity (nM)\n";
    results.forEach(row => {
      csvContent += `${row.target_gene},${row.amino_acid_change || 'N/A'},${row.peptide_sequence},${hlaAllele},${row.ic50_score}\n`;
    });
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `GULBIA_Clinical_Report_${patientId}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const TopNav = () => (
    <nav className="Top-Nav Clinical-Serif">
      <div className="Nav-Logo Ahsing-Font" onClick={() => setActivePage('Home')}>M</div>
      <div className="Nav-Links Inter-Font">
        <span className={activePage === 'Workspace' ? 'Active-Link' : ''} onClick={handleEnterWorkspace}>Clinical Workspace</span>
        <span className={activePage === 'Methodology' ? 'Active-Link' : ''} onClick={() => setActivePage('Methodology')}>Methodology</span>
        <span className={activePage === 'Documentation' ? 'Active-Link' : ''} onClick={() => setActivePage('Documentation')}>Documentation & API</span>
        <span className={activePage === 'Contact' ? 'Active-Link' : ''} onClick={() => setActivePage('Contact')}>Contact</span>
        <span className={activePage === 'Profile' ? 'Active-Link' : ''} onClick={() => setActivePage('Profile')}>User Profile</span>
      </div>
    </nav>
  );

  const LandingPage = () => (
    <div className="Landing-Page Fade-In">
      <header className="Hero-Section">
        <div className="Hero-Text-Container">
          <h1 className="Huge-Title Instrument-Font">GULBIA</h1>
          <h2 className="Hero-Subtitle Inter-Font">Genomic Utility for Liver Biomarker and Immunotherapy Analysis</h2>
        </div>
        <div className="Hero-Btn-Container">
          <button className="Hero-Btn Inter-Font" onClick={handleEnterWorkspace}>Get Started &rarr;</button>
        </div>
        <img className="Hero-BG" src="/dna-bg.jpg" alt="Dark DNA Structure" />
      </header>

      <section className="Design-Section-Light">
        <div className="Section-Container">
          <div className="Pill-Header"><h2>Precision Neoantigen<br/>Discovery for Hepatocellular<br/>Carcinoma</h2></div>
          <div className="Text-Content Inter-Font"><p>GULBIA bridges the critical gap between raw tumor sequencing and personalized immunotherapy. Designed specifically for liver biomarker analysis, the engine ingests patient-specific somatic mutation data (VCF/MAF) and automatically translates non-synonymous variants into 9-mer mutant peptide sequences. We isolate the specific genomic anomalies driving the cancer, providing the foundational targets required for customized mRNA or peptide-based vaccine development.</p></div>
        </div>
      </section>

      <section className="Design-Section-Dark">
        <div className="Section-Container">
          <div className="Dark-Section-Header"><h2>Neural-Backed MHC-I<br/>Binding Prediction</h2></div>
          <div className="Text-Content Inter-Font"><p>Identifying a mutation is not enough; the immune system must be able to see it. Not all mutant proteins are immunogenic. GULBIA interfaces with advanced neural network models to predict the binding affinity of translated peptides against specific patient HLA alleles. By calculating precise IC50 scores, the engine filters out passenger mutations and isolates the 'Goldilocks' targets—those with an affinity score under 500nM—ensuring only the strongest binders are prioritized for clinical use.</p></div>
        </div>
      </section>

      <section className="Design-Section-Light">
        <div className="Section-Container">
          <div className="Pill-Header"><h2>Aseptic Reporting for<br/>Vaccine Pipelines</h2></div>
          <div className="Text-Content Inter-Font"><p>A computational tool is only as valuable as its output. GULBIA translates thousands of rows of complex genomic noise into a clean, actionable clinical hierarchy. The system automatically formats the highest-affinity neoantigen targets, alongside their variant consequences and precise peptide payloads, into standardized CSV reports. This allows clinicians and biotech manufacturers to immediately export validated data directly into their downstream synthesis and production pipelines.</p></div>
        </div>
      </section>

      <footer className="Design-Footer Inter-Font">
        <div className="Footer-Divider"></div>
        <div className="Footer-Grid">
          <div className="Footer-Logo-Box"><span className="Ahsing-Font">M</span></div>
          <div className="Footer-Info">
            <h4>CONTACT</h4>
            <p>Muhammad Muneeb Sultan<br/>muneebkayt369@gmail.com</p>
          </div>
        </div>
      </footer>
    </div>
  );

  const WorkspacePage = () => (
    <div className="Dashboard Inter-Font Fade-In">
      <nav className="Sidebar">
        <div className="Sidebar-Header">
          <h2 className="Instrument-Font">GULBIA ENGINE</h2>
          <div className="Status-Indicator"><span className="Pulse-Dot"></span> SYSTEM ONLINE</div>
        </div>
        <div className="Divider" />
        <div className="Meta-Box">
          <label>PATIENT ID</label>
          <div className="Val mono">{patientId}</div>
          <label>SOURCE</label>
          <div className="Val">Liver Tissue</div>
        </div>
        <div className="Divider" />
        <div className="Param-Box">
          <label>HLA ALLELE (MHC-I)</label>
          <select value={hlaAllele} onChange={(e) => setHlaAllele(e.target.value)}>
            <option>HLA-A*02:01</option>
            <option>HLA-A*01:01</option>
          </select>
          <p style={{fontSize: '0.7rem', color: '#555', marginTop: '10px', lineHeight: '1.4'}}>
            *Algorithm locked to high-throughput uncapped batch processing.
          </p>
        </div>
        <button className="Exit-Btn" onClick={() => { setActivePage('Home'); setResults(null); setVaccineData(null); }}>Terminate Session</button>
      </nav>

      <main className="Workspace">
        <header className="W-Header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div>
            <h1 className="Instrument-Font">Clinical Workspace</h1>
            <p style={{margin: '5px 0 0 0', color: '#666', fontFamily: 'monospace'}}>Aseptic Environment // Ready for Genomic Payload</p>
          </div>
          {results && (
            <button onClick={downloadCSV} className="Run-Btn" style={{ background: 'transparent', color: '#ff4d4d', border: '1px solid #ff4d4d' }}>📥 Export Full CSV ({results.length} targets)</button>
          )}
        </header>
        
        <div className="Upload-Dropzone">
          <label className="Custom-File-Upload">
            <input type="file" onChange={handleFileChange} style={{display: 'none'}} />
            <div className="File-Name-Display">
              {selectedFile ? `📄 ${selectedFile.name}` : "📁 CLICK TO SELECT CLINICAL DATA (.MAF / .VCF)"}
            </div>
          </label>
          <button onClick={handleAnalyze} className="Run-Btn" disabled={isLoading || !selectedFile}>
            {isLoading ? "ANALYZING MUTATIONS..." : "EXECUTE PROTOCOL"}
          </button>
        </div>

        {/* BRUTE-FORCE RENDERING: It is physically impossible for CSS to hide this now */}
        {vaccineData && vaccineData.full_sequence ? (
          <div className="Vaccine-Blueprint-Box Fade-In" style={{ minHeight: '200px', display: 'block', overflow: 'visible' }}>
            <h2 className="Blueprint-Title Instrument-Font" style={{marginBottom: '10px'}}>Vaccine Construct Blueprint</h2>
            <p className="Blueprint-Subtitle" style={{color: '#ff4d4d', marginBottom: '20px'}}>Proposed Multi-Epitope mRNA Sequence (Top Targets)</p>
            
            <div className="Final-Sequence-Display" style={{color: '#00ff00', backgroundColor: '#111', padding: '20px', fontFamily: 'monospace', wordBreak: 'break-all', border: '1px solid #333', borderRadius: '5px'}}>
              {vaccineData.full_sequence}
            </div>
            
            <div style={{display: 'flex', gap: '40px', fontSize: '0.85rem', color: '#888', marginTop: '20px', fontFamily: 'monospace'}}>
               <div><strong style={{color: '#fff'}}>LENGTH:</strong> {vaccineData.length} AA</div>
               <div><strong style={{color: '#fff'}}>WEIGHT:</strong> {vaccineData.molecular_weight}</div>
               <div><strong style={{color: '#fff'}}>pI:</strong> {vaccineData.isoelectric_point}</div>
            </div>
          </div>
        ) : null}

        {results && (
          <div className="Table-Container Fade-In">
            <div style={{color: '#888', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '10px', display: 'flex', justifyContent: 'space-between'}}>
               <span>Displaying Top 100 Candidates</span>
               <span>{results.length} Total Targets Processed</span>
            </div>
            <table className="Clinical-Table">
              <thead>
                <tr>
                  <th>Target Gene</th>
                  <th>Mutant Peptide (9-mer)</th>
                  <th>IC50 Binding Affinity</th>
                </tr>
              </thead>
              <tbody>
                {results.slice(0, 100).map((r, i) => (
                  <tr key={i}>
                    <td>{r.target_gene}</td>
                    <td className="mono" style={{color: '#ff8e8e'}}>{r.peptide_sequence}</td>
                    <td className={r.ic50_score < 500 ? "clinical-serif Green" : "clinical-serif"} style={r.ic50_score < 500 ? {color: '#00ff00', fontWeight: 'bold'} : {}}>
                      {r.ic50_score} nM
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );

  return (
    <div className="App Inter-Font">
      <TopNav />
      {activePage === 'Workspace' && <WorkspacePage />}
      {activePage === 'Methodology' && <Methodology />}
      {activePage === 'Documentation' && <Documentation />}
      {activePage === 'Profile' && <UserProfile />}
      {activePage === 'Contact' && <Contact />}
      {activePage === 'Home' && <LandingPage />}
    </div>
  );
}

export default App;