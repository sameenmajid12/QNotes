import { useState, useEffect } from 'react';
import '../styles/voice-agent.css';

function EnhancedVoiceAgent({ file }) {
  const [isActive, setIsActive] = useState(false);
  const [currentDemo, setCurrentDemo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(true);

  // Demo agent data
  const agentData = {
    status: 'Active',
    type: 'AI Financial Advisor',
    capabilities: [
      '📊 Real-time Financial Analysis',
      '🎙️ Earnings Call Simulation', 
      '💡 Intelligent Investment Advice',
      '📈 Market Commentary & Trends',
      '❓ Interactive Q&A Sessions'
    ]
  };

  const handleVoiceDemo = async (demoType, text) => {
    setLoading(true);
    setCurrentDemo(demoType);
    
    // Simulate voice processing
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Create a simple text-to-speech if available
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.voice = speechSynthesis.getVoices().find(voice => 
        voice.name.includes('Alex') || voice.name.includes('Daniel') || voice.default
      );
      speechSynthesis.speak(utterance);
    }
    
    setLoading(false);
    setCurrentDemo(null);
  };

  useEffect(() => {
    setIsActive(true);
  }, []);

  return (
    <div className="voice-agent-container">
      <div className="voice-agent-header">
        <div className="header-icon">🎤</div>
        <h1>AI Voice Financial Advisor</h1>
        <p className="voice-agent-description">
          Experience intelligent financial conversations with advanced AI voice synthesis
          {file ? ` • Currently analyzing: ${file.name}` : ''}
        </p>
        <div className="header-underline"></div>
      </div>

      {isActive && (
        <div className="voice-agent-content">
          <div className="agent-info">
            <div className="agent-status-bar">
              <div className="status-item">
                <span className="status-indicator active"></span>
                <span className="status-text">{agentData.status}</span>
              </div>
              <div className="agent-type">
                <span className="type-label">Agent Type:</span>
                <span className="type-value">{agentData.type}</span>
              </div>
            </div>
            
            <div className="capabilities-section">
              <h3 className="capabilities-title">🧠 AI Capabilities</h3>
              <div className="capabilities-grid">
                {agentData.capabilities.map((capability, index) => (
                  <div key={index} className="capability-item">
                    {capability}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="voice-features">
            <h3 className="section-title">🎙️ Interactive Voice Demos</h3>
            <p className="section-subtitle">Click any demo below to hear the AI voice in action</p>
            
            <div className="feature-grid">
              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h4>Earnings Call Simulation</h4>
                <p>Experience realistic executive presentations with professional tone and delivery</p>
                <button 
                  onClick={() => handleVoiceDemo('earnings', "Welcome to Apple's Q1 2024 earnings call. We're pleased to report strong performance with revenue of 119.6 billion dollars, representing 2 percent year-over-year growth.")}
                  className={`feature-btn ${currentDemo === 'earnings' && loading ? 'speaking' : ''}`}
                  disabled={loading && currentDemo !== 'earnings'}
                >
                  {currentDemo === 'earnings' && loading ? (
                    <>🔊 Speaking...</>
                  ) : (
                    <>▶️ Play Earnings Call</>
                  )}
                </button>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">💹</div>
                <h4>Financial Analysis</h4>
                <p>Get detailed explanations of key metrics, ratios, and performance indicators</p>
                <button 
                  onClick={() => handleVoiceDemo('analysis', "Let me break down the key financial metrics. The gross margin improved to 46.6 percent, indicating strong operational efficiency and favorable product mix across all segments.")}
                  className={`feature-btn ${currentDemo === 'analysis' && loading ? 'speaking' : ''}`}
                  disabled={loading && currentDemo !== 'analysis'}
                >
                  {currentDemo === 'analysis' && loading ? (
                    <>🔊 Analyzing...</>
                  ) : (
                    <>📈 Analyze Metrics</>
                  )}
                </button>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">💡</div>
                <h4>Investment Insights</h4>
                <p>Receive AI-powered recommendations and strategic market outlook analysis</p>
                <button 
                  onClick={() => handleVoiceDemo('advice', "Based on comprehensive analysis of current performance metrics and market conditions, Apple demonstrates strong fundamentals with resilient iPhone sales and accelerating services growth.")}
                  className={`feature-btn ${currentDemo === 'advice' && loading ? 'speaking' : ''}`}
                  disabled={loading && currentDemo !== 'advice'}
                >
                  {currentDemo === 'advice' && loading ? (
                    <>🔊 Advising...</>
                  ) : (
                    <>💰 Investment Advice</>
                  )}
                </button>
              </div>
              
              <div className="feature-card">
                <div className="feature-icon">🌍</div>
                <h4>Market Commentary</h4>
                <p>Explore market trends, sector performance, and macroeconomic indicators</p>
                <button 
                  onClick={() => handleVoiceDemo('market', "Current market dynamics reveal technology sector resilience. Despite macroeconomic headwinds, companies with strong ecosystem moats continue to demonstrate superior performance.")}
                  className={`feature-btn ${currentDemo === 'market' && loading ? 'speaking' : ''}`}
                  disabled={loading && currentDemo !== 'market'}
                >
                  {currentDemo === 'market' && loading ? (
                    <>🔊 Commenting...</>
                  ) : (
                    <>📀 Market Update</>
                  )}
                </button>
              </div>
            </div>
          </div>

          <div className="voice-controls">
            <h3 className="section-title">🎛️ Voice Controls</h3>
            <div className="controls-section">
              <div className="control-item">
                <button 
                  onClick={() => speechSynthesis.cancel()}
                  className="control-btn stop-btn"
                  disabled={!loading}
                  title="Stop current voice playback"
                >
                  ⏹️ Stop Audio
                </button>
              </div>
              
              <div className="control-item">
                <button 
                  onClick={() => handleVoiceDemo('demo', "Welcome to QNotes AI Voice Agent. This advanced financial advisor uses cutting-edge voice synthesis to provide intelligent market analysis and investment insights.")}
                  className="control-btn test-btn"
                  disabled={loading}
                  title="Test the voice synthesis system"
                >
                  {currentDemo === 'demo' && loading ? (
                    <>🔊 Testing...</>
                  ) : (
                    <>🎤 Test Voice System</>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* ElevenLabs ConvAI Widget */}
          <div className="convai-widget-section">
            <h3>💬 Interactive AI Chat</h3>
            <p>Chat directly with the ElevenLabs AI financial advisor</p>
            <div className="widget-container">
              <elevenlabs-convai agent-id="agent_2001k6r67ejzejx930t22kwwaw5j"></elevenlabs-convai>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default EnhancedVoiceAgent;
