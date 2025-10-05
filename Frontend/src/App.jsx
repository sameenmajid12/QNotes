import { useState, useEffect, useRef } from "react"; // 👈 Import useRef
import { supabase } from "./supabaseClient";
import "./index.css";

// Separate component for the main landing page content
function LandingPage({ onLoginClick, onSignupClick }) {
  const fileInputRef = useRef(null);
  
  // SEC Search states
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState('cik'); // 'name' or 'cik'
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  const handleUploadButtonClick = () => {
    fileInputRef.current.click();
  };

  // 👈 3. Function to handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Selected file:", file.name);
      alert(`File selected: ${file.name}. Ready to upload!`);
      // Add actual file upload logic here
    }
  };

  const searchCompany = async () => {
    if (!searchTerm.trim()) {
      setError('Please enter a company name, ticker, or CIK');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);
    setSearched(true);

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
        
        // Fetch company info to verify CIK exists
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

      // Search by name/ticker
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
      
      // Convert to array and search
      const companies = Object.values(data);
      const searchLower = searchTerm.toLowerCase();
      
      const matches = companies.filter(company => 
        company.title.toLowerCase().includes(searchLower) ||
        company.ticker?.toLowerCase().includes(searchLower)
      );

      if (matches.length === 0) {
        setError('No companies found matching your search');
      } else {
        // Add padded CIK to results
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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchCompany();
    }
  };

  return (
    <div className="landing-page">
      <header className="header">
        <div className="logo-placeholder">Q Notes</div>
        <div className="auth-buttons">
          <button className="primary-btn login-btn" onClick={onLoginClick}>
            Login
          </button>
          <button className="secondary-btn signup-btn" onClick={onSignupClick}>
            Sign Up
          </button>
        </div>
      </header>

      <main className="hero-section">
        {/* Left Column: Text and Search */}
        <div className="hero-left">
          <h1 className="main-title">
            Learn Finance Through <span className="highlight-text">Real Reports</span>
          </h1>
          <p className="subtitle-text">
            Search for a company or upload a 10-Q file, and we'll turn it into simple
            summaries, charts, and explanations you can understand with definitions
            for any financial terms you don't know.
          </p>
          <div className="p-6 max-w-3xl mx-auto">

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            searchType === 'name'
              ? 'Enter company name or ticker'
              : 'Enter CIK number'
          }
          className="flex-1 px-3 py-2 border border-gray-300 rounded"
        />
        <button
          onClick={searchCompany}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-300 rounded text-red-700">
          {error}
        </div>
      )}

      {searched && !loading && results.length > 0 && (
        <div>
          <p className="mb-3 font-semibold">
            Found {results.length} {results.length === 1 ? 'company' : 'companies'}
          </p>
          
          {results.map((company, idx) => (
            <div key={idx} className="mb-3 p-4 border border-gray-300 rounded">
              <div className="mb-2">
                <div className="font-bold">{company.title}</div>
                <div className="text-sm text-gray-600">
                  Ticker: {company.ticker || 'N/A'} | CIK: {company.cik_padded}
                </div>
              </div>
              
              <a
                href={company.edgarUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                View SEC Filings →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
        </div>

        

        {/* Right Column: Upload Card */}
        <div className="hero-right">
          <div className="upload-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#6d5dfc" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="file-icon">
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
            {/* 👈 4. The actual hidden file input */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden-file-input"
                accept=".txt,.pdf,.doc,.docx" // Optional: specify acceptable file types
            />
            {/* 👈 5. The visible button to trigger the hidden input */}
            <button className="primary-btn upload-btn" onClick={handleUploadButtonClick}>
              Upload File
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="upload-icon">
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

// ... rest of App.jsx (AuthView and App components) remains the same as your previous working version ...
function AuthView({ onLogin, onSignup, onToggleAuth, showSignup }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = showSignup ? onSignup : onLogin;
    
    return (
        <div className="container auth-view">
            <div className="card">
                <h1 className="title">Q Notes</h1>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit(email, password);
                }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit" className="primary-btn">
                        {showSignup ? "Sign Up" : "Login"}
                    </button>
                </form>
                <p className="toggle-text">
                    {showSignup ? "Already have an account?" : "Don't have an account?"}{" "}
                    <button
                        type="button"
                        className="link-btn"
                        onClick={onToggleAuth}
                    >
                        {showSignup ? "Login" : "Sign Up"}
                    </button>
                </p>
            </div>
        </div>
    );
}

function App() {
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState(null); // 'login', 'signup', or null for landing page
  // The email/password states are no longer needed here as they are managed in AuthView
  // const [email, setEmail] = useState(""); 

  useEffect(() => {
    // Initial session check
    supabase.auth.getSession().then(({ data }) => {
      if (data.session) setUser(data.session.user);
    });

    // Listener for auth state changes
    const { data: subscription } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription?.subscription?.unsubscribe();
  }, []);

  const handleAuth = async (isSignup, currentEmail, currentPassword) => {
    const method = isSignup 
        ? supabase.auth.signUp 
        : supabase.auth.signInWithPassword;

    const { data, error } = await method({
        email: currentEmail,
        password: currentPassword,
    });

    if (error) {
        alert(error.message);
    } else if (isSignup) {
        alert("Signup successful! Check your email for confirmation.");
        setAuthMode(null); // Go back to landing page
    } else {
        setUser(data.user);
        setAuthMode(null); // Go to logged-in view
    }
  };

  // const handleLogin and handleSignup are simplified for brevity, 
  // but the logic remains to call handleAuth
  
  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };
  
  // Decide which view to render
  if (user) {
    // Logged-in view
    return (
      <div className="container logged-in-container">
        <div className="card logged-in">
          <h1>Welcome, {user.email}</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    );
  }

  if (authMode) {
    // Login/Signup Modal/View
    return (
        <div className="gradient-bg">
            <AuthView 
                onLogin={(email, password) => handleAuth(false, email, password)}
                onSignup={(email, password) => handleAuth(true, email, password)}
                onToggleAuth={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}
                showSignup={authMode === 'signup'}
            />
        </div>
    )
  }

  // Landing Page View
  return (
    <LandingPage
        onLoginClick={() => setAuthMode('login')}
        onSignupClick={() => setAuthMode('signup')}
    />
  );
}

export default App;