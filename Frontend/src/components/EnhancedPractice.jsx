import { useState, useEffect } from 'react';
import '../styles/enhanced-practice.css';

const API_BASE_URL = 'http://localhost:8000';

function EnhancedPractice() {
  const [currentStep, setCurrentStep] = useState('sections'); // 'sections', 'teaching', 'practice', 'grading', 'insights'
  const [sections, setSections] = useState([]);
  const [currentSection, setCurrentSection] = useState(null);
  const [teaching, setTeaching] = useState(null);
  const [smapAnswers, setSmapAnswers] = useState({
    subjective: '',
    metrics: '',
    assessment: '',
    plan: ''
  });
  const [grading, setGrading] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Demo session ID
  const sessionId = 'demo123';

  useEffect(() => {
    loadSections();
  }, []);

  const loadSections = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/practice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'get_sections' }),
      });
      const data = await response.json();
      
      if (data.success) {
        setSections(data.sections.sections || []);
      } else {
        setError('Failed to load sections');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const startSection = async (section) => {
    try {
      setLoading(true);
      setCurrentSection(section);
      
      // Get SMAP teaching for this section
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/practice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'teach_smap', section: section }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setTeaching(data.teaching);
        setCurrentStep('teaching');
      } else {
        setError('Failed to load teaching content');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const startPractice = () => {
    setCurrentStep('practice');
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
      
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/practice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'grade_submission',
          student_submission: `SUBJECTIVE: ${smapAnswers.subjective}\n\nMETRICS: ${smapAnswers.metrics}\n\nASSESSMENT: ${smapAnswers.assessment}\n\nPLAN: ${smapAnswers.plan}`,
          section_id: currentSection?.id || 'financial_statements'
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setGrading(data.grading);
        setCurrentStep('grading');
      } else {
        setError('Failed to submit SMAP notes');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getInsights = async () => {
    try {
      setLoading(true);
      
      const response = await fetch(`${API_BASE_URL}/api/session/${sessionId}/practice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'get_insights' }),
      });
      const data = await response.json();
      
      if (data.success) {
        setInsights(data.insights);
        setCurrentStep('insights');
      } else {
        setError('Failed to get insights');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetPractice = () => {
    setCurrentStep('sections');
    setCurrentSection(null);
    setTeaching(null);
    setGrading(null);
    setInsights(null);
    setSmapAnswers({
      subjective: '',
      metrics: '',
      assessment: '',
      plan: ''
    });
  };

  if (loading) {
    return (
      <div className="practice">
        <div className="loading">
          <h2>Loading...</h2>
          <p>Please wait while we prepare your practice session.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="practice">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="practice">
      <div className="practice-header">
        <h1>Enhanced Practice Mode</h1>
        <p className="practice-description">
          Interactive SMAP learning with AI-powered feedback and grading
        </p>
        <div className="header-underline"></div>
      </div>

      {/* Sections Selection */}
      {currentStep === 'sections' && (
        <section className="sections-selection">
          <h2 className="section-title">Choose a Section to Practice</h2>
          <div className="sections-grid">
            {sections.map((section, index) => (
              <div key={section.id} className="section-card" onClick={() => startSection(section)}>
                <h3>{section.title}</h3>
                <p className="section-description">{section.description}</p>
                <div className="section-meta">
                  <span className={`difficulty ${section.difficulty}`}>{section.difficulty}</span>
                  <span className="part">{section.part}</span>
                </div>
                <div className="section-objectives">
                  <strong>Learning Objectives:</strong>
                  <ul>
                    {section.learning_objectives?.map((obj, i) => (
                      <li key={i}>{obj}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Teaching Phase */}
      {currentStep === 'teaching' && teaching && (
        <section className="teaching-phase">
          <div className="teaching-header">
            <h2>SMAP Framework Teaching</h2>
            <h3>{currentSection?.title}</h3>
            <button className="start-practice-btn" onClick={startPractice}>
              Start Practice
            </button>
          </div>
          
          <div className="teaching-content">
            <div className="teaching-text" dangerouslySetInnerHTML={{ __html: teaching.teaching_content.replace(/\n/g, '<br>') }} />
            
            <div className="section-info">
              <div className="info-item">
                <strong>Difficulty:</strong> {teaching.difficulty}
              </div>
              <div className="info-item">
                <strong>SMAP Focus:</strong> {teaching.smap_focus}
              </div>
              <div className="info-item">
                <strong>Learning Objectives:</strong>
                <ul>
                  {teaching.learning_objectives?.map((obj, i) => (
                    <li key={i}>{obj}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Practice Phase */}
      {currentStep === 'practice' && (
        <section className="practice-phase">
          <div className="practice-header">
            <h2>Practice SMAP Analysis</h2>
            <h3>{currentSection?.title}</h3>
          </div>

          <div className="smap-grid">
            <div className="smap-field">
              <label className="smap-label">Subjective (S)</label>
              <textarea
                className="smap-textarea"
                placeholder="Management's narrative, tone, forward-looking statements, strategic priorities"
                rows="6"
                value={smapAnswers.subjective}
                onChange={(e) => handleSmapChange('subjective', e.target.value)}
              />
            </div>

            <div className="smap-field">
              <label className="smap-label">Metrics (M)</label>
              <textarea
                className="smap-textarea"
                placeholder="Key financial numbers, ratios, trends, quantitative data"
                rows="6"
                value={smapAnswers.metrics}
                onChange={(e) => handleSmapChange('metrics', e.target.value)}
              />
            </div>

            <div className="smap-field">
              <label className="smap-label">Assessment (A)</label>
              <textarea
                className="smap-textarea"
                placeholder="Analysis of performance, risks, strengths/weaknesses, what the numbers mean"
                rows="6"
                value={smapAnswers.assessment}
                onChange={(e) => handleSmapChange('assessment', e.target.value)}
              />
            </div>

            <div className="smap-field">
              <label className="smap-label">Plan (P)</label>
              <textarea
                className="smap-textarea"
                placeholder="Future outlook, strategic initiatives, management's next steps"
                rows="6"
                value={smapAnswers.plan}
                onChange={(e) => handleSmapChange('plan', e.target.value)}
              />
            </div>
          </div>

          <div className="submit-section">
            <button className="submit-btn" onClick={submitSmap}>
              Submit for AI Grading
            </button>
          </div>
        </section>
      )}

      {/* Grading Phase */}
      {currentStep === 'grading' && grading && (
        <section className="grading-phase">
          <div className="grading-header">
            <h2>AI Feedback & Grading</h2>
            <div className="score-display">
              <div className="overall-score">
                <span className="score-number">{grading.overall_score}</span>
                <span className="score-label">/100</span>
                <span className={`grade ${grading.letter_grade}`}>{grading.letter_grade}</span>
              </div>
            </div>
          </div>

          <div className="component-scores">
            <h3>Component Scores</h3>
            <div className="score-grid">
              <div className="score-item">
                <span className="score-label">Subjective</span>
                <span className="score-value">{grading.component_scores?.subjective || 0}/100</span>
              </div>
              <div className="score-item">
                <span className="score-label">Metrics</span>
                <span className="score-value">{grading.component_scores?.metrics || 0}/100</span>
              </div>
              <div className="score-item">
                <span className="score-label">Assessment</span>
                <span className="score-value">{grading.component_scores?.assessment || 0}/100</span>
              </div>
              <div className="score-item">
                <span className="score-label">Plan</span>
                <span className="score-value">{grading.component_scores?.plan || 0}/100</span>
              </div>
            </div>
          </div>

          <div className="detailed-feedback">
            <h3>Detailed Feedback</h3>
            <div className="feedback-content" dangerouslySetInnerHTML={{ __html: grading.detailed_feedback.replace(/\n/g, '<br>') }} />
          </div>

          <div className="grading-actions">
            <button className="insights-btn" onClick={getInsights}>
              Get Progress Insights
            </button>
            <button className="reset-btn" onClick={resetPractice}>
              Try Another Section
            </button>
          </div>
        </section>
      )}

      {/* Insights Phase */}
      {currentStep === 'insights' && insights && (
        <section className="insights-phase">
          <div className="insights-header">
            <h2>Learning Progress Insights</h2>
          </div>

          <div className="insights-content">
            <div className="progress-stats">
              <div className="stat-item">
                <span className="stat-label">Average Score</span>
                <span className="stat-value">{insights.average_score?.toFixed(1) || 0}/100</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Sections Completed</span>
                <span className="stat-value">{insights.sections_completed || 0}</span>
              </div>
            </div>

            <div className="insights-text" dangerouslySetInnerHTML={{ __html: insights.insights.replace(/\n/g, '<br>') }} />
          </div>

          <div className="insights-actions">
            <button className="reset-btn" onClick={resetPractice}>
              Practice More Sections
            </button>
          </div>
        </section>
      )}
    </div>
  );
}

export default EnhancedPractice;
