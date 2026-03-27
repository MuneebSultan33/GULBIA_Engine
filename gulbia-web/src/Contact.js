import React from 'react';

const Contact = () => {
  return (
    <div className="Contact-Container Inter-Font Fade-In">
      
      {/* 1. Hero with safe inline background image */}
      <div className="Contact-Hero" style={{ backgroundImage: "url('/contact-bg.jpg')" }}>
        <div className="Contact-Hero-Overlay"></div>
        <h1 className="Contact-Hero-Text Instrument-Font">Initiate<br/>Collaboration</h1>
      </div>

      <div className="Contact-Middle-Block">
        <p className="Contact-Middle-Text Inter-Font">
          The GULBIA clinical pipeline is under active development. For clinical inquiries, access to the source code, or collaboration on bioinformatics and computational virology research, please reach out through the channels below.
        </p>
      </div>

      <div className="Contact-Bottom-Block">
        <div className="Contact-Divider-Line"></div>
        <div className="Contact-Details-Grid">
          <h2 className="Contact-Details-Title Instrument-Font">Contact Details:</h2>
          <div className="Contact-List-Container">
            <ul className="Contact-List Inter-Font">
              <li>Lead Developer: Muhammad Muneeb Sultan</li>
              <li>Email: muneebkayt369@gmail.com</li>
              <li>Phone: +92-3214856171</li>
              <li>LinkedIn: <a href="https://www.linkedin.com/in/muhammad-muneeb-sultan-878975352" target="_blank" rel="noreferrer">linkedin.com/in/muhammad-muneeb-sultan-878975352</a></li>
              <li>Location: Lahore, Pakistan</li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  );
};

export default Contact;