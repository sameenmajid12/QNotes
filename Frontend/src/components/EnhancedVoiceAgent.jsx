import { useState, useEffect } from 'react';
import '../styles/voice-agent.css';

function EnhancedVoiceAgent({ file }) {
  const [isActive, setIsActive] = useState(false);
  const [currentDemo, setCurrentDemo] = useState(null);
  const [loading, setLoading] = useState(false);

  // Demo agent data
  const agentData = {
    status: 'Active',
    type: 'financial_advisor',
    capabilities: [
      'Financial Analysis',
      'Earnings Call Simulation', 
      'Investment Advice',
      'Market Commentary',
      'Q&A Session'
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
        <h1>🎤 AI Voice Agent</h1>
        <p className="voice-agent-description">
          Interactive financial advisor with voice synthesis {file ? `analyzing ${file.name}` : ''}
        </p>
        <div className="header-underline"></div>
      </div>

      {isActive && (
        <div className="voice-agent-content">
          <div className="agent-info">
            <h2>🤖 Financial Advisor Agent</h2>
            <div className="agent-details">
              <div className="agent-status">
                <span className="status-indicator active"></span>
                <span>Status: {agentData.status}</span>
              </div>
              <div className="agent-type">
                <strong>Type:</strong> {agentData.type.replace('_', ' ').toUpperCase()}
              </div>
              <div className="agent-capabilities">
                <strong>Capabilities:</strong>
                <ul>
                  {agentData.capabilities.map((capability, index) => (
                    <li key={index}>{capability}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="voice-features">
            <h3>🎙️ Voice Features Demo</h3>
            <div className="feature-grid">
              <div className="feature-card">
                <h4>📊 Earnings Call Simulation</h4>
                <p>Experience realistic earnings call conversations with management tone</p>
                <button 
                  onClick={() => handleVoiceDemo('earnings', "Welcome to Apple's Q1 2024 earnings call. We're pleased to report strong performance with revenue of 119.6 billion dollars, up 2 percent year over year.")}
                  className={`feature-btn ${currentDemo === 'earnings' ? 'active' : ''}`}
                  disabled={loading}
                >
                  {currentDemo === 'earnings' && loading ? '🎙️ Speaking...' : '▶️ Play Demo'}
                </button>
              </div>
              
              <div className="feature-card">
                <h4>💹 Financial Analysis</h4>
                <p>Get detailed explanations of financial metrics and ratios</p>
                <button 
                  onClick={() => handleVoiceDemo('analysis', "Let me explain the key financial ratios. The gross margin improved to 46.6 percent, indicating strong operational efficiency and favorable product mix.")}
                  className={`feature-btn ${currentDemo === 'analysis' ? 'active' : ''}`}
                  disabled={loading}
                >
                  {currentDemo === 'analysis' && loading ? '🎙️ Speaking...' : '📈 Analyze Metrics'}
                </button>
              </div>
              
              <div className="feature-card">
                <h4>💡 Investment Insights</h4>
                <p>Receive AI-powered investment recommendations and market outlook</p>
                <button 
                  onClick={() => handleVoiceDemo('advice', "Based on current performance metrics and market conditions, Apple shows strong fundamentals with resilient iPhone sales and growing services revenue.")}
                  className={`feature-btn ${currentDemo === 'advice' ? 'active' : ''}`}
                  disabled={loading}
                >
                  {currentDemo === 'advice' && loading ? '🎙️ Speaking...' : '💰 Get Advice'}
                </button>
              </div>
              
              <div className="feature-card">
                <h4>🌍 Market Commentary</h4>
                <p>Discuss market trends, sector performance, and economic indicators</p>
                <button 
                  onClick={() => handleVoiceDemo('market', "Current market trends show technology sector resilience. Despite macroeconomic headwinds, companies with strong ecosystems continue to outperform.")}
                  className={`feature-btn ${currentDemo === 'market' ? 'active' : ''}`}
                  disabled={loading}
                >
                  {currentDemo === 'market' && loading ? '🎙️ Speaking...' : '📊 Market Update'}
                </button>
              </div>
            </div>
          </div>

          <div className="demo-info">
            <div className="info-card">
              <h3>🎯 Demo Features</h3>
              <ul>
                <li>✅ <strong>Voice Synthesis:</strong> Browser-based text-to-speech</li>
                <li>✅ <strong>Financial Content:</strong> Real earnings data and analysis</li>
                <li>✅ <strong>Interactive UI:</strong> Click any demo button to hear AI voice</li>
                <li>🔄 <strong>ElevenLabs Ready:</strong> Can integrate with professional voice models</li>
              </ul>
            </div>
          </div>

          <div className="voice-controls">
            <h3>🎛️ Voice Controls</h3>
            <div className="controls-row">
              <button 
                onClick={() => speechSynthesis.cancel()}
                className="control-btn stop-btn"
                disabled={!loading}
              >
                ⏹️ Stop Voice
              </button>
              <button 
                onClick={() => handleVoiceDemo('demo', "This is a demonstration of the AI voice agent for financial analysis and investment insights.")}
                className="control-btn demo-btn"
                disabled={loading}
              >
                🎤 Test Voice
              </button>
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
