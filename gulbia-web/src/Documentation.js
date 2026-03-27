import React from 'react';

const Documentation = () => {
  return (
    <div className="Doc-Container Inter-Font Fade-In">
      
      {/* Hero Section */}
      <div className="Doc-Hero">
        <div className="Doc-Hero-Text">
          <h1 className="Instrument-Font">System<br/>Architecture &<br/>Integration</h1>
          <p>
            The GULBIA engine is built for high-throughput clinical environments, 
            utilizing a decoupled React.js frontend and an asynchronous Python/FastAPI backend.
          </p>
        </div>
        {/* Make sure to add this green DNA image to your public folder later */}
        <img src="/dna-green.png" alt="Green DNA Helix" className="Doc-Hero-Image" />
      </div>

      {/* The Green Block */}
      <div className="Doc-Block Doc-Green">
        <h2 className="Instrument-Font">The Async Brain<br/>(Concurrency<br/>Model):</h2>
        <p>
          To process thousands of genomic rows without rate-limiting external databases, 
          the backend employs a Semaphore-controlled asynchronous loop (asyncio). It 
          processes batches of up to 10,000 rows concurrently, reducing analysis time 
          from hours to seconds.
        </p>
      </div>

      {/* The Dark API Endpoint Block */}
      <div className="Doc-Block Doc-Dark">
        <h2 className="Instrument-Font">API Endpoint<br/>Details:</h2>
        
        <div className="Doc-List">
          {/* Item 1 - Left Aligned */}
          <div className="Doc-List-Item">
            <span className="Doc-List-Num">1</span>
            <p className="Doc-List-Text">Endpoint: POST /analyze/</p>
          </div>

          {/* Item 2 - Indented Right (The Zig-Zag) */}
          <div className="Doc-List-Item Offset-Right-Doc" style={{marginTop: '20px', marginBottom: '20px'}}>
            <span className="Doc-List-Num">2</span>
            <p className="Doc-List-Text">
              Payload Requirements: Requires a .maf or .vcf multipart file, a target 
              hla_allele string, and an integer batch_size.
            </p>
          </div>

          {/* Item 3 - Left Aligned */}
          <div className="Doc-List-Item">
            <span className="Doc-List-Num">3</span>
            <p className="Doc-List-Text">
              Output: Returns a structured JSON payload containing the sorted array of 
              analysis_results (Gene, Variant, Peptide, Affinity) and the vaccine_construct 
              blueprint (Sequence, Length, Weight, pI).
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};

export default Documentation;