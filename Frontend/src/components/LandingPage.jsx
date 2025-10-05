import { useState, useRef } from "react";
import "../styles/landingpage.css";
function LandingPage({ setFile }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState("");
  const [error, setError] = useState('');
   const[result, setResults] = useState([]);
  const fileInputRef = useRef(null);
   const searchCompany = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) {
      setError('Please enter a company name, ticker, or CIK');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      // If searching by CIK, directly create the result
      if (searchType === 'cik') {
        const cikNumber = searchTerm.replace(/\D/g, ''); // Remove non-digits
        
        if (!cikNumber) {
          setError('Please enter a valid CIK number');
          setLoading(false);
          return;
        }

        const cikPadded = cikNumber.padStart(10, '0');
        
        try {
          const response = await fetch(
            `https://data.sec.gov/submissions/CIK${cikPadded}.json`,
            {
              headers: {
                'User-Agent': 'Company Search Tool'
              }
            }
          );

          if (!response.ok) {
            throw new Error('CIK not found');
          }

          const companyInfo = await response.json();
          
          setResults([{
            title: companyInfo.name,
            ticker: companyInfo.tickers?.[0] || 'N/A',
            cik_str: parseInt(cikNumber),
            cik_padded: cikPadded,
            edgarUrl: `https://www.sec.gov/edgar/browse/?CIK=${cikPadded}&owner=exclude`
          }]);
        } catch (err) {
          setError('CIK number not found in SEC database');
        }
        
        setLoading(false);
        return;
      }

      const response = await fetch(
        'https://www.sec.gov/files/company_tickers.json',
        {
          headers: {
            'User-Agent': 'Company Search Tool'
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch company data');
      }

      const data = await response.json();
      
      const companies = Object.values(data);
      const searchLower = searchTerm.toLowerCase();
      
      const matches = companies.filter(company => 
        company.title.toLowerCase().includes(searchLower) ||
        company.ticker?.toLowerCase().includes(searchLower)
      );

      if (matches.length === 0) {
        setError('No companies found matching your search');
      } else {
        const formattedResults = matches.map(company => ({
          ...company,
          cik_padded: String(company.cik_str).padStart(10, '0'),
          edgarUrl: `https://www.sec.gov/edgar/browse/?CIK=${String(company.cik_str).padStart(10, '0')}&owner=exclude`
        }));
        console.log(formattedResults);
        setResults(formattedResults);
      }
    } catch (err) {
      setError('Error fetching data from SEC. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  const handleSearch = (e) => {
    e.preventDefault();
    console.log("Searching for:", searchTerm);
  };

  const handleUploadButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Selected file:", file.name);
      setFile(file.name)
      alert(`File selected: ${file.name}. Ready to upload!`);
    }
  };

  return (
    <div className="landing-page">
      <main className="hero-section">
        <div className="hero-left">
          <div>
            <h1 className="main-title">
              Learn Finance Through{" "}
              <span className="highlight-text">Real Reports</span>
            </h1>
            <p className="subtitle-text">
              Search for a company or upload a 10-Q file, and we'll turn it into
              simple summaries, charts, and explanations you can understand —
              with definitions for any financial terms you don't know.
            </p>
          </div>

          <span className="seperator-line"></span>
          <form className="search-box" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Search company (eg. Apple, Google...)"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              required
            />
            <button type="submit" onClick={searchCompany} className="search-btn">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="feather feather-search"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </form>
        </div>

        <div className="hero-right">
          <div className="upload-card">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="100"
              height="100"
              viewBox="0 0 24 24"
              fill="none"
              stroke="var(--color-primary)"
              strokeWidth="1"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="file-icon"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <p className="upload-prompt">
              Upload your 10Q file here for
              <br />
              us to analyze and simplify it
              <br />
              for you!
            </p>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden-file-input"
              accept=".txt,.pdf,.doc,.docx"
            />
            <button
              className="primary-btn upload-btn"
              onClick={handleUploadButtonClick}
            >
              Upload File
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="upload-icon"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default LandingPage;
