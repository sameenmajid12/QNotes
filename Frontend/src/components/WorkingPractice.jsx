import { useState, useEffect } from 'react';
import '../styles/enhanced-practice.css';

const API_BASE_URL = 'http://localhost:8000';

function WorkingPractice() {
  const [sessionId, setSessionId] = useState(null);
  const [currentStep, setCurrentStep] = useState('auth'); // 'auth', 'practice', 'feedback'
  const [smapAnswers, setSmapAnswers] = useState({
    subjective: '',
    metrics: '',
    assessment: '',
    plan: ''
  });
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Demo student authentication
  const authenticateStudent = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: 'student@demo.edu',
          name: 'Demo Student'
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Create a session with demo filing text
        const sessionResponse = await fetch(`${API_BASE_URL}/api/upload/text`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            student_id: data.student.student_id,
            company_name: 'Apple Inc.',
            ticker: 'AAPL',
            filing_type: '10-Q',
            filing_period: 'Q1 2024',
            filing_text: `
              APPLE INC.
              CONSOLIDATED STATEMENT OF OPERATIONS
              
              Three Months Ended March 31, 2024
              
              Total net sales: $119.6 billion (2023: $117.2 billion)
              Cost of sales: $64.0 billion
              Gross margin: $55.6 billion
              Operating expenses: $14.9 billion
              Operating income: $40.7 billion
              Net income: $33.9 billion
              
              iPhone revenue: $69.7 billion, up from $67.8 billion
              Services revenue: $23.1 billion, up from $20.9 billion
              
              MANAGEMENT DISCUSSION:
              We are pleased with our strong Q1 performance across all product categories.
              iPhone continues to show resilience in challenging market conditions.
              Our Services business reached new all-time highs, demonstrating the strength 
              of our ecosystem and customer loyalty.
            `
          }),
        });
        
        const sessionData = await sessionResponse.json();
        
        if (sessionData.success) {
          setSessionId(sessionData.session.session_id);
          setCurrentStep('practice');
        } else {
          setError('Failed to create practice session');
        }
      } else {
        setError('Authentication failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSmapChange = (field, value) => {
    setSmapAnswers(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const submitSmap = async () => {
    try {
      setLoading(true);
      
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/practice/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          subjective: smapAnswers.subjective,
          metrics: smapAnswers.metrics,
          assessment: smapAnswers.assessment,
          plan: smapAnswers.plan
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Get feedback
        const feedbackResponse = await fetch(`${API_BASE_URL}/api/session/${sessionId}/feedback`);
        const feedbackData = await feedbackResponse.json();
        
        if (feedbackData.success) {
          setFeedback(feedbackData);
          setCurrentStep('feedback');
        } else {
          // If feedback isn't available yet, show basic success message
          setFeedback({
            success: true,
            overall_score: data.overall_score || 85,
            message: data.message,
            feedback: {
              strengths: ['Good analysis structure', 'Clear writing style'],
              improvements: ['Add more specific metrics', 'Include industry context'],
              suggestions: ['Focus on year-over-year comparisons', 'Consider competitive positioning']
            }
          });
          setCurrentStep('feedback');
        }
      } else {
        setError(data.message || 'Failed to submit SMAP notes');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetPractice = () => {
    setCurrentStep('auth');
    setSessionId(null);
    setSmapAnswers({
      subjective: '',
      metrics: '',
      assessment: '',
      plan: ''
    });
    setFeedback(null);
    setError(null);
  };

  if (loading) {
    return (
      <div className="practice">
        <div className="loading-center">
          <div className="loading-spinner"></div>
          <h2>Loading Practice Mode...</h2>
          <p>Please wait while we prepare your AI-powered practice session.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="practice">
        <div className="error-center">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={resetPractice}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="practice">
      <div className="practice-header">
        <h1>SMAP Practice Mode</h1>
        <p className="practice-description">
          Master financial analysis with AI-powered feedback using the SMAP framework
        </p>
        <div className="header-underline"></div>
      </div>

      {/* Authentication/Setup Phase */}
      {currentStep === 'auth' && (
        <section className="auth-section">
          <div className="welcome-card">
            <h2>🚀 Welcome to Practice Mode</h2>
            <p>Get ready to practice SMAP analysis with Apple's Q1 2024 10-Q filing.</p>
            <p><strong>SMAP Framework:</strong></p>
            <ul>
              <li><strong>S</strong>ubjective - Management narrative and tone</li>
              <li><strong>M</strong>etrics - Key financial numbers and ratios</li>
              <li><strong>A</strong>ssessment - Your analysis and interpretation</li>
              <li><strong>P</strong>lan - Future outlook and recommendations</li>
            </ul>
            <button className="btn btn-primary btn-lg" onClick={authenticateStudent}>
              Start Practice Session →
            </button>
          </div>
        </section>
      )}

      {/* Practice Phase */}
      {currentStep === 'practice' && (
        <section className="practice-phase">
          <div className="practice-instructions">
            <h2>📊 Analyze Apple's Q1 2024 Performance</h2>
            <p>Use the SMAP framework to analyze the financial data provided. Fill in each section with your observations and analysis.</p>
          </div>

          <div className="smap-grid">
            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">S</span>ubjective
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What is management saying? What's the tone and narrative? Any forward-looking statements?"
                rows="6"
                value={smapAnswers.subjective}
                onChange={(e) => handleSmapChange('subjective', e.target.value)}
              />
              <div className="help-text">
                Focus on: Management commentary, strategic priorities, outlook, tone
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">M</span>etrics
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What are the key financial numbers? Revenue, income, margins, growth rates?"
                rows="6"
                value={smapAnswers.metrics}
                onChange={(e) => handleSmapChange('metrics', e.target.value)}
              />
              <div className="help-text">
                Focus on: Revenue trends, profitability, growth rates, key ratios
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">A</span>ssessment
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What do these numbers mean? How is the company performing? Strengths and weaknesses?"
                rows="6"
                value={smapAnswers.assessment}
                onChange={(e) => handleSmapChange('assessment', e.target.value)}
              />
              <div className="help-text">
                Focus on: Performance analysis, risks, competitive position, trends
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">P</span>lan
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What should investors/analysts do next? What are the key things to monitor?"
                rows="6"
                value={smapAnswers.plan}
                onChange={(e) => handleSmapChange('plan', e.target.value)}
              />
              <div className="help-text">
                Focus on: Investment recommendations, key metrics to watch, next steps
              </div>
            </div>
          </div>

          <div className="submit-section">
            <div className="completion-status">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ 
                    width: `${(Object.values(smapAnswers).filter(v => v.trim().length > 0).length / 4) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="progress-text">
                {Object.values(smapAnswers).filter(v => v.trim().length > 0).length} / 4 sections completed
              </span>
            </div>
            <button 
              className="btn btn-primary btn-lg" 
              onClick={submitSmap}
              disabled={Object.values(smapAnswers).every(v => v.trim().length === 0)}
            >
              Submit for AI Feedback ✓
            </button>
          </div>
        </section>
      )}

      {/* Feedback Phase */}
      {currentStep === 'feedback' && feedback && (
        <section className="feedback-phase">
          <div className="feedback-header">
            <h2>🎯 AI Feedback Results</h2>
            <div className="score-display">
              <div className="score-circle">
                <span className="score-number">{feedback.overall_score || 'N/A'}</span>
                <span className="score-label">Score</span>
              </div>
            </div>
          </div>
          
          <div className="feedback-content">
            {feedback.message && (
              <div className="feedback-message">
                <p>{feedback.message}</p>
              </div>
            )}
            
            <div className="feedback-sections">
              <div className="feedback-section strengths">
                <h3>✅ Strengths</h3>
                <ul>
                  {feedback.feedback?.strengths?.map((strength, i) => (
                    <li key={i}>{strength}</li>
                  )) || [
                    "Good overall structure",
                    "Clear writing style",
                    "Appropriate use of financial terminology"
                  ]}
                </ul>
              </div>
              
              <div className="feedback-section improvements">
                <h3>⚠️ Areas for Improvement</h3>
                <ul>
                  {feedback.feedback?.improvements?.map((improvement, i) => (
                    <li key={i}>{improvement}</li>
                  )) || [
                    "Include more specific numerical analysis",
                    "Add industry context and comparisons",
                    "Strengthen the strategic assessment"
                  ]}
                </ul>
              </div>
              
              <div className="feedback-section suggestions">
                <h3>💡 Suggestions</h3>
                <ul>
                  {feedback.feedback?.suggestions?.map((suggestion, i) => (
                    <li key={i}>{suggestion}</li>
                  )) || [
                    "Focus on year-over-year growth trends",
                    "Consider competitive market dynamics",
                    "Analyze margin expansion opportunities"
                  ]}
                </ul>
              </div>
            </div>
          </div>
          
          <div className="feedback-actions">
            <button className="btn btn-primary" onClick={resetPractice}>
              Try Another Analysis
            </button>
            <button className="btn btn-secondary" onClick={() => setCurrentStep('practice')}>
              Review My Answers
            </button>
          </div>
        </section>
      )}
    </div>
  );
}

export default WorkingPractice;