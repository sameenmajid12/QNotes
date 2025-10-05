import { useState, useEffect } from 'react';
import '../styles/simple-voice-agent.css';

const API_BASE_URL = 'http://localhost:8000';

function SimpleVoiceAgent() {
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
        // Fallback: Create a mock ConvAI agent for demo
        console.log('ConvAI API failed, using fallback mode');
        setConvaiAgent({
          agent_id: 'agent_2001k6r67ejzejx930t22kwwaw5j',
          name: 'Financial Advisor',
          description: 'AI-powered financial advisor for earnings calls and analysis',
          widget_code: '<div style="background: #f8f9fa; padding: 2rem; border-radius: 12px; text-align: center;"><h3>🎤 ConvAI Widget</h3><p>ElevenLabs ConvAI integration would appear here</p><p><strong>Agent ID:</strong> agent_2001k6r67ejzejx930t22kwwaw5j</p><p><em>Demo mode - Full ConvAI functionality available with proper API setup</em></p></div>'
        });
      }
    } catch (err) {
      console.log('Network error, using fallback mode:', err.message);
      // Fallback: Create a mock ConvAI agent for demo
      setConvaiAgent({
        agent_id: 'agent_2001k6r67ejzejx930t22kwwaw5j',
        name: 'Financial Advisor',
        description: 'AI-powered financial advisor for earnings calls and analysis',
        widget_code: '<div style="background: #f8f9fa; padding: 2rem; border-radius: 12px; text-align: center;"><h3>🎤 ConvAI Widget</h3><p>ElevenLabs ConvAI integration would appear here</p><p><strong>Agent ID:</strong> agent_2001k6r67ejzejx930t22kwwaw5j</p><p><em>Demo mode - Full ConvAI functionality available with proper API setup</em></p></div>'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="simple-voice-agent">
      <div className="voice-agent-header">
        <h1>🎤 AI Voice Agent</h1>
        <p>Chat with our AI financial advisor powered by ElevenLabs ConvAI</p>
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

      {convaiAgent && isWidgetLoaded && (
        <div className="convai-container">
          <div className="agent-info">
            <h2>🤖 Financial Advisor Agent</h2>
            <p>Status: <span className="status-active">Active</span></p>
            <p>Capabilities: Earnings calls, financial analysis, investment advice, market discussion</p>
          </div>

          {/* ElevenLabs ConvAI Widget */}
          <div className="convai-widget-container">
            <h3>💬 Chat with AI Advisor</h3>
            <div 
              className="convai-widget"
              dangerouslySetInnerHTML={{ 
                __html: convaiAgent.widget_code || 
                `<elevenlabs-convai agent-id="${convaiAgent.agent_id}"></elevenlabs-convai>`
              }}
            />
          </div>
        </div>
      )}

      {!isWidgetLoaded && !error && (
        <div className="widget-loading">
          <p>Loading interactive chat widget...</p>
        </div>
      )}
    </div>
  );
}

export default SimpleVoiceAgent;
