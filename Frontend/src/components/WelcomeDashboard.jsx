import { useState, useRef } from 'react';
import '../styles/welcome-dashboard.css';
import { LoadingSpinner, EmptyState } from './LoadingStates';

function WelcomeDashboard({ onSelectFile, user }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState([]);
  const [searchType, setSearchType] = useState('company');
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
                'User-Agent': 'QNotes Financial Learning Platform'
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
            'User-Agent': 'QNotes Financial Learning Platform'
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
      ).slice(0, 10); // Limit to 10 results

      if (matches.length === 0) {
        setError('No companies found matching your search');
      } else {
        const formattedResults = matches.map(company => ({
          ...company,
          cik_padded: String(company.cik_str).padStart(10, '0'),
          edgarUrl: `https://www.sec.gov/edgar/browse/?CIK=${String(company.cik_str).padStart(10, '0')}&owner=exclude`
        }));
        setResults(formattedResults);
      }
    } catch (err) {
      setError('Error fetching data from SEC. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['.txt', '.pdf', '.doc', '.docx'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!validTypes.includes(fileExtension)) {
        setError('Please upload a valid document file (.txt, .pdf, .doc, .docx)');
        return;
      }

      console.log("Selected file:", file.name);
      onSelectFile(file.name);
    }
  };

  const selectCompany = (company) => {
    // In a real app, this would fetch the 10-Q data
    console.log("Selected company:", company);
    onSelectFile(`${company.title} (${company.ticker}) - Latest 10-Q`);
  };

  return (
    <div className="welcome-dashboard">
      <div className="dashboard-header">
        <div className="welcome-content">
          <h1 className="welcome-title">
            Welcome back, <span className="user-name">{user?.email?.split('@')[0] || 'Student'}</span>!
          </h1>
          <p className="welcome-subtitle">
            Ready to dive into financial learning? Choose a company to analyze or upload your own 10-Q document.
          </p>
        </div>
        
        <div className="dashboard-stats">
          <div className="stat-item">
            <div className="stat-icon">📚</div>
            <div className="stat-content">
              <div className="stat-number">0</div>
              <div className="stat-label">Documents Analyzed</div>
            </div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">🎯</div>
            <div className="stat-content">
              <div className="stat-number">0</div>
              <div className="stat-label">Practice Sessions</div>
            </div>
          </div>
          <div className="stat-item">
            <div className="stat-icon">⏱️</div>
            <div className="stat-content">
              <div className="stat-number">0h</div>
              <div className="stat-label">Learning Time</div>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="action-section">
          <div className="search-section">
            <div className="section-header">
              <h2 className="section-title">Find a Company</h2>
              <p className="section-description">
                Search for any public company to analyze their latest 10-Q filing
              </p>
            </div>
            
            <div className="search-controls">
              <div className="search-type-toggle">
                <button 
                  className={`toggle-btn ${searchType === 'company' ? 'active' : ''}`}
                  onClick={() => setSearchType('company')}
                >
                  By Name/Ticker
                </button>
                <button 
                  className={`toggle-btn ${searchType === 'cik' ? 'active' : ''}`}
                  onClick={() => setSearchType('cik')}
                >
                  By CIK Number
                </button>
              </div>

              <form className="company-search-form" onSubmit={searchCompany}>
                <div className="search-input-container">
                  <input
                    type="text"
                    placeholder={searchType === 'company' 
                      ? "Enter company name or ticker (e.g., Apple, AAPL)" 
                      : "Enter CIK number (e.g., 320193)"
                    }
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                    required
                  />
                  <button type="submit" className="search-submit-btn" disabled={loading}>
                    {loading ? (
                      <LoadingSpinner size="sm" color="white" />
                    ) : (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                      </svg>
                    )}
                  </button>
                </div>
              </form>

              {error && (
                <div className="error-message">
                  <span className="error-icon">⚠️</span>
                  {error}
                </div>
              )}

              {results.length > 0 && (
                <div className="search-results">
                  <h3 className="results-title">Search Results</h3>
                  <div className="results-list">
                    {results.map((company, index) => (
                      <div 
                        key={index} 
                        className="result-item hover-lift"
                        onClick={() => selectCompany(company)}
                      >
                        <div className="result-content">
                          <div className="company-name">{company.title}</div>
                          <div className="company-details">
                            <span className="ticker">{company.ticker}</span>
                            <span className="cik">CIK: {company.cik_str}</span>
                          </div>
                        </div>
                        <div className="result-action">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polyline points="9 18 15 12 9 6"></polyline>
                          </svg>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="upload-section">
            <div className="section-header">
              <h2 className="section-title">Upload Document</h2>
              <p className="section-description">
                Have your own 10-Q document? Upload it for AI-powered analysis
              </p>
            </div>
            
            <div className="upload-area" onClick={handleUploadButtonClick}>
              <div className="upload-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-15"></path>
                  <polyline points="7 10 12 5 17 10"></polyline>
                  <line x1="12" y1="5" x2="12" y2="15"></line>
                </svg>
              </div>
              <div className="upload-content">
                <h3 className="upload-title">Click to upload or drag and drop</h3>
                <p className="upload-description">Support for PDF, DOC, DOCX, and TXT files</p>
                <div className="upload-formats">
                  <span className="format-tag">PDF</span>
                  <span className="format-tag">DOC</span>
                  <span className="format-tag">TXT</span>
                </div>
              </div>
            </div>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
              accept=".txt,.pdf,.doc,.docx"
            />
          </div>
        </div>

        <div className="recent-activity">
          <div className="section-header">
            <h2 className="section-title">Recent Activity</h2>
            <p className="section-description">Pick up where you left off</p>
          </div>
          
          <EmptyState
            icon="📋"
            title="No recent activity"
            description="Start analyzing your first document to see your activity here."
            action={
              <button className="btn btn-primary" onClick={handleUploadButtonClick}>
                Upload Document
              </button>
            }
          />
        </div>
      </div>
    </div>
  );
}

export default WelcomeDashboard;