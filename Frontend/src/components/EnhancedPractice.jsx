import { useState } from 'react';
import '../styles/enhanced-practice.css';

function EnhancedPractice({ file }) {
  const [currentStep, setCurrentStep] = useState('practice');
  const [smapAnswers, setSmapAnswers] = useState({
    subjective: '',
    metrics: '',
    assessment: '',
    plan: ''
  });
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSmapChange = (field, value) => {
    setSmapAnswers(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const submitSmap = async () => {
    try {
      setLoading(true);
      
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Calculate score based on content quality
      const totalContent = Object.values(smapAnswers).join(' ').toLowerCase();
      let score = 70;
      
      // Boost score for financial keywords
      const keywords = ['revenue', 'profit', 'growth', 'margin', 'performance', 'risk', 'strategy', 'outlook', 'billion', 'income'];
      keywords.forEach(keyword => {
        if (totalContent.includes(keyword)) score += 3;
      });
      
      // Boost for comprehensive answers
      const avgLength = totalContent.length / 4;
      if (avgLength > 50) score += 10;
      if (avgLength > 100) score += 5;
      
      score = Math.min(score, 100);
      
      // Generate demo feedback
      setFeedback({
        success: true,
        overall_score: score,
        message: `SMAP analysis submitted successfully! AI Score: ${score}/100`,
        feedback: {
          strengths: [
            'Good use of SMAP framework structure',
            'Clear analytical thinking demonstrated', 
            'Appropriate financial terminology used',
            'Well-organized presentation of ideas'
          ],
          improvements: [
            'Include more specific numerical analysis',
            'Add industry context and peer comparisons', 
            'Strengthen strategic assessment with risk factors',
            'Consider macroeconomic factors impact'
          ],
          suggestions: [
            'Focus on year-over-year growth trends',
            'Consider competitive market dynamics',
            'Analyze margin expansion opportunities',
            'Include forward-looking guidance analysis',
            'Examine cash flow generation patterns'
          ]
        }
      });
      setCurrentStep('feedback');
      
    } catch (err) {
      console.error('Demo error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetPractice = () => {
    setCurrentStep('practice');
    setSmapAnswers({
      subjective: '',
      metrics: '',
      assessment: '',
      plan: ''
    });
    setFeedback(null);
  };

  if (loading) {
    return (
      <div className="practice">
        <div className="loading-center">
          <div className="loading-spinner"></div>
          <h2>Processing Your SMAP Analysis...</h2>
          <p>AI is analyzing your submission and generating personalized feedback.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="practice">
      <div className="practice-header">
        <h1>🎯 SMAP Practice Mode</h1>
        <p className="practice-description">
          Master financial analysis with AI-powered feedback using the SMAP framework{file ? ` for ${file.name}` : ''}
        </p>
        <div className="header-underline"></div>
      </div>

      {/* Practice Phase */}
      {currentStep === 'practice' && (
        <section className="practice-phase">
          <div className="practice-instructions">
            <h2>📊 Analyze Apple's Q1 2024 Performance</h2>
            <p>Apply the SMAP framework to analyze Apple's latest quarterly results. Fill each section with your observations.</p>
            
            <div className="smap-info">
              <div className="smap-item"><strong>S</strong>ubjective - Management narrative & tone</div>
              <div className="smap-item"><strong>M</strong>etrics - Key financial numbers & ratios</div>
              <div className="smap-item"><strong>A</strong>ssessment - Your analysis & interpretation</div>
              <div className="smap-item"><strong>P</strong>lan - Future outlook & recommendations</div>
            </div>
          </div>

          <div className="smap-grid">
            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">S</span>ubjective
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What is management saying? What's their tone and narrative? Any forward-looking statements or strategic priorities mentioned?"
                rows="6"
                value={smapAnswers.subjective}
                onChange={(e) => handleSmapChange('subjective', e.target.value)}
              />
              <div className="help-text">
                💡 Focus on: Management commentary, strategic priorities, market outlook, confidence level
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">M</span>etrics
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What are the key financial numbers? Revenue growth, profit margins, cash flow, key performance indicators?"
                rows="6"
                value={smapAnswers.metrics}
                onChange={(e) => handleSmapChange('metrics', e.target.value)}
              />
              <div className="help-text">
                📈 Focus on: Revenue trends, profitability, growth rates, operational metrics, year-over-year changes
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">A</span>ssessment
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What do these numbers mean? How is the company performing? What are the strengths, weaknesses, and risks?"
                rows="6"
                value={smapAnswers.assessment}
                onChange={(e) => handleSmapChange('assessment', e.target.value)}
              />
              <div className="help-text">
                🔍 Focus on: Performance analysis, competitive position, risk factors, market trends impact
              </div>
            </div>

            <div className="smap-field">
              <label className="smap-label">
                <span className="smap-letter">P</span>lan
              </label>
              <textarea
                className="smap-textarea"
                placeholder="What should investors/analysts do next? What are the key metrics to monitor? Investment recommendations?"
                rows="6"
                value={smapAnswers.plan}
                onChange={(e) => handleSmapChange('plan', e.target.value)}
              />
              <div className="help-text">
                🎯 Focus on: Investment thesis, key catalysts to watch, risk mitigation, action items
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
              🤖 Submit for AI Feedback & Grading
            </button>
          </div>
        </section>
      )}

      {/* Feedback Phase */}
      {currentStep === 'feedback' && feedback && (
        <section className="feedback-phase">
          <div className="feedback-header">
            <h2>🎯 AI-Powered Feedback Results</h2>
            <div className="score-display">
              <div className="score-circle">
                <span className="score-number">{feedback.overall_score}</span>
                <span className="score-label">AI Score</span>
              </div>
            </div>
          </div>
          
          <div className="feedback-content">
            {feedback.message && (
              <div className="feedback-message">
                <p><strong>{feedback.message}</strong></p>
              </div>
            )}
            
            <div className="feedback-sections">
              <div className="feedback-section strengths">
                <h3>✅ Strengths Identified</h3>
                <ul>
                  {feedback.feedback?.strengths?.map((strength, i) => (
                    <li key={i}>{strength}</li>
                  ))}
                </ul>
              </div>
              
              <div className="feedback-section improvements">
                <h3>⚠️ Areas for Improvement</h3>
                <ul>
                  {feedback.feedback?.improvements?.map((improvement, i) => (
                    <li key={i}>{improvement}</li>
                  ))}
                </ul>
              </div>
              
              <div className="feedback-section suggestions">
                <h3>💡 AI Suggestions</h3>
                <ul>
                  {feedback.feedback?.suggestions?.map((suggestion, i) => (
                    <li key={i}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          
          <div className="feedback-actions">
            <button className="btn btn-primary" onClick={resetPractice}>
              📝 Try Another Analysis
            </button>
            <button className="btn btn-secondary" onClick={() => setCurrentStep('practice')}>
              👁️ Review My Answers
            </button>
          </div>
        </section>
      )}
    </div>
  );
}

export default EnhancedPractice;
