import { useState, useEffect } from 'react';
import '../styles/voice-agent.css';

const API_BASE_URL = 'http://localhost:8000';

function EnhancedVoiceAgent() {
  const [convaiAgent, setConvaiAgent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isWidgetLoaded, setIsWidgetLoaded] = useState(false);
  const sessionId = 'demo123';

  useEffect(() => {
    initializeConvAI();
    loadConvAIScript();
  }, []);

  const loadConvAIScript = () => {
    // Load ElevenLabs ConvAI widget script
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/@elevenlabs/convai-widget-embed';
    script.async = true;
    script.onload = () => {
      setIsWidgetLoaded(true);
      console.log('ElevenLabs ConvAI script loaded');
    };
    script.onerror = () => {
      console.error('Failed to load ElevenLabs ConvAI script');
    };
    document.head.appendChild(script);
  };

  const initializeConvAI = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/convai`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'Hello, initialize the financial advisor agent' }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setConvaiAgent(data.convai_agent);
      } else {
        setError('Failed to initialize ConvAI agent');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceSynthesis = async (text, voiceType = 'professional') => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/voice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, voice_type: voiceType }),
      });
      
      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
      }
    } catch (err) {
      console.error('Voice synthesis error:', err);
    }
  };

  return (
    <div className="voice-agent-container">
      <div className="voice-agent-header">
        <h1>🎤 AI Voice Agent</h1>
        <p className="voice-agent-description">
          Interactive financial advisor powered by ElevenLabs ConvAI
        </p>
        <div className="header-underline"></div>
      </div>

      {loading && (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Initializing AI Voice Agent...</p>
        </div>
      )}

      {error && (
        <div className="error-state">
          <h3>⚠️ Error</h3>
          <p>{error}</p>
          <button onClick={initializeConvAI} className="retry-btn">
            Retry
          </button>
        </div>
      )}

      {convaiAgent && (
        <div className="voice-agent-content">
          <div className="agent-info">
            <h2>🤖 Financial Advisor Agent</h2>
            <div className="agent-details">
              <div className="agent-status">
                <span className="status-indicator active"></span>
                <span>Status: {convaiAgent.status}</span>
              </div>
              <div className="agent-type">
                <strong>Type:</strong> {convaiAgent.type.replace('_', ' ').toUpperCase()}
              </div>
              <div className="agent-capabilities">
                <strong>Capabilities:</strong>
                <ul>
                  {convaiAgent.capabilities.map((capability, index) => (
                    <li key={index}>{capability.replace('_', ' ')}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="voice-features">
            <h3>🎙️ Voice Features</h3>
            <div className="feature-grid">
              <div className="feature-card">
                <h4>Earnings Call Simulation</h4>
                <p>Experience realistic earnings call conversations</p>
                <button 
                  onClick={() => handleVoiceSynthesis("Welcome to our Q1 2024 earnings call. We're pleased to report strong performance across all segments.")}
                  className="feature-btn"
                >
                  Play Demo
                </button>
              </div>
              
              <div className="feature-card">
                <h4>Financial Analysis Q&A</h4>
                <p>Ask questions about financial statements and metrics</p>
                <button 
                  onClick={() => handleVoiceSynthesis("Let me explain the key financial ratios and what they mean for investors.")}
                  className="feature-btn"
                >
                  Ask Question
                </button>
              </div>
              
              <div className="feature-card">
                <h4>Investment Advice</h4>
                <p>Get AI-powered investment insights and recommendations</p>
                <button 
                  onClick={() => handleVoiceSynthesis("Based on current market conditions, here are my investment recommendations.")}
                  className="feature-btn"
                >
                  Get Advice
                </button>
              </div>
              
              <div className="feature-card">
                <h4>Market Discussion</h4>
                <p>Discuss market trends and economic outlook</p>
                <button 
                  onClick={() => handleVoiceSynthesis("Let's discuss the current market trends and economic indicators.")}
                  className="feature-btn"
                >
                  Discuss Market
                </button>
              </div>
            </div>
          </div>

          {/* ElevenLabs ConvAI Widget */}
          {isWidgetLoaded && convaiAgent.agent_id && (
            <div className="convai-widget-container">
              <h3>💬 Interactive Chat</h3>
              <p>Chat directly with the AI financial advisor</p>
              <div 
                className="convai-widget"
                dangerouslySetInnerHTML={{ 
                  __html: convaiAgent.widget_code || 
                  `<elevenlabs-convai agent-id="${convaiAgent.agent_id}"></elevenlabs-convai>`
                }}
              />
            </div>
          )}

          {!isWidgetLoaded && (
            <div className="widget-loading">
              <p>Loading interactive chat widget...</p>
            </div>
          )}
        </div>
      )}

      <div className="voice-agent-footer">
        <p>Powered by ElevenLabs ConvAI Technology</p>
      </div>
    </div>
  );
}

export default EnhancedVoiceAgent;
