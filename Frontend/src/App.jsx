import { useState, useEffect, useRef } from "react"; // 👈 Import useRef
import { supabase } from "./supabaseClient";
import "./index.css";

// Separate component for the main landing page content
function LandingPage({ onLoginClick, onSignupClick }) {
  const [searchQuery, setSearchQuery] = useState("");
  // 👈 1. Create a ref for the file input
  const fileInputRef = useRef(null); 

  const handleSearch = (e) => {
    e.preventDefault();
    console.log("Searching for:", searchQuery);
    // Add logic for search here
  };

  // 👈 2. Function to trigger the hidden file input
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
            summaries, charts, and explanations you can understand — with definitions
            for any financial terms you don't know.
          </p>
          <form className="search-box" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Search company (eg. Apple, Google...)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              required
            />
            <button type="submit" className="search-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-search">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </form>
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