import { useState } from "react";
import '../styles/enhanced-auth.css';

function EnhancedAuthView({ onLogin, onSignup, onToggleAuth, showSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    // Basic validation
    const newErrors = {};
    if (!email) newErrors.email = "Email is required";
    if (!password) newErrors.password = "Password is required";
    if (showSignup && !name) newErrors.name = "Name is required";
    if (email && !email.includes('.edu')) newErrors.email = "Please use a .edu email address";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setLoading(false);
      return;
    }

    try {
      if (showSignup) {
        await onSignup(email, password);
      } else {
        await onLogin(email, password);
      }
    } catch (error) {
      setErrors({ general: "Authentication failed. Please try again." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-background">
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
        </div>
      </div>
      
      <div className="auth-content">
        <div className="auth-card">
          <div className="auth-header">
            <div className="logo-container">
              <div className="logo-icon">📊</div>
              <h1 className="logo-text">QNotes AI</h1>
            </div>
            <p className="auth-subtitle">
              {showSignup 
                ? "Join the future of financial education" 
                : "Welcome back to your learning journey"
              }
            </p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            {showSignup && (
              <div className="input-group">
                <label htmlFor="name">Full Name</label>
                <input
                  id="name"
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className={errors.name ? 'error' : ''}
                  disabled={loading}
                />
                {errors.name && <span className="error-text">{errors.name}</span>}
              </div>
            )}

            <div className="input-group">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                placeholder="your.email@university.edu"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={errors.email ? 'error' : ''}
                disabled={loading}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={errors.password ? 'error' : ''}
                disabled={loading}
              />
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            {errors.general && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {errors.general}
              </div>
            )}

            <button 
              type="submit" 
              className={`auth-button ${loading ? 'loading' : ''}`}
              disabled={loading}
            >
              {loading ? (
                <div className="button-loading">
                  <div className="spinner"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                showSignup ? "Create Account" : "Sign In"
              )}
            </button>
          </form>

          <div className="auth-footer">
            <p className="toggle-text">
              {showSignup ? "Already have an account?" : "Don't have an account?"}
              <button
                type="button"
                className="toggle-link"
                onClick={onToggleAuth}
                disabled={loading}
              >
                {showSignup ? "Sign In" : "Create Account"}
              </button>
            </p>
          </div>

          <div className="auth-features">
            <div className="feature-item">
              <span className="feature-icon">🎓</span>
              <span>Student-focused learning</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🤖</span>
              <span>AI-powered feedback</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📈</span>
              <span>Real financial data</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EnhancedAuthView;
