import { useState } from 'react';
import '../styles/voiceagent.css';

function VoiceAgent() {
  const [isListening, setIsListening] = useState(false);

  return (
    <div className="voice-agent">
      <div className="voice-agent-header">
        <h1>Voice Agent</h1>
        <p className="voice-agent-description">
          Ask our AI anything about the company's 10-Q, from definitions to deeper financial insights.
          <br />
          Learn through conversation and get clear, plain-English explanations.
        </p>
        <div className="header-underline"></div>
      </div>

      <div className="voice-agent-content">
        <div className="voice-visualizer">
          <div className={`voice-circle ${isListening ? 'active' : ''}`}>
            <svg viewBox="0 0 200 200" className="voice-pattern">
              <defs>
                <pattern id="circuit" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M0 20 L10 20 L10 10 L30 10 L30 30 L20 30" stroke="#1a8fff" strokeWidth="2" fill="none" opacity="0.3"/>
                  <circle cx="10" cy="20" r="2" fill="#1a8fff" opacity="0.5"/>
                  <circle cx="30" cy="10" r="2" fill="#1a8fff" opacity="0.5"/>
                </pattern>
                <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#0ea5e9" />
                  <stop offset="50%" stopColor="#2754f5" />
                  <stop offset="100%" stopColor="#1e40af" />
                </linearGradient>
              </defs>
              <circle cx="100" cy="100" r="95" fill="url(#blueGradient)" />
              <rect x="0" y="0" width="200" height="200" fill="url(#circuit)" />
            </svg>
          </div>
        </div>

        <div className="voice-controls">
          <button
            className={`control-btn mic-btn ${isListening ? 'active' : ''}`}
            onClick={() => setIsListening(!isListening)}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 14C13.66 14 15 12.66 15 11V5C15 3.34 13.66 2 12 2C10.34 2 9 3.34 9 5V11C9 12.66 10.34 14 12 14Z" fill="white"/>
              <path d="M17 11C17 13.76 14.76 16 12 16C9.24 16 7 13.76 7 11H5C5 14.53 7.61 17.43 11 17.92V21H13V17.92C16.39 17.43 19 14.53 19 11H17Z" fill="white"/>
            </svg>
          </button>
          <button className="control-btn close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6L18 18" stroke="#888" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>

        <div className="suggestions">
          <p className="suggestions-title">Try asking:</p>
          <p className="suggestion-item">What does net income mean?</p>
          <p className="suggestion-item">Why did revenue drop this quarter?</p>
          <p className="suggestion-item">Explain this company's debt ratio.</p>
        </div>
      </div>
    </div>
  );
}

export default VoiceAgent;
