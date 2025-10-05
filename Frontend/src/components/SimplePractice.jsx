import { useState } from 'react';
import '../styles/simple-practice.css';

function SimplePractice() {
  const [currentSection, setCurrentSection] = useState(null);
  const [smapAnswers, setSmapAnswers] = useState({
    subjective: '',
    metrics: '',
    assessment: '',
    plan: ''
  });
  const [grading, setGrading] = useState(null);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // All 9 sections for demo
  const sections = [
    {
      id: "financial_statements",
      title: "Financial Statements",
      description: "Company's balance sheet, income statement, and cash flow",
      difficulty: "Beginner",
      content: "The company reported strong Q1 performance with revenue of $42.5 billion (+6.8% YoY), net income of $13.4 billion, and operating cash flow of $15.2 billion. Key metrics include ROE of 17.8%, CET1 ratio of 15.9%, and book value per share of $95.35.",
      part: "Part I",
      learning_objectives: "Understand financial statements and key metrics",
      smap_focus: "Financial performance analysis"
    },
    {
      id: "md_a",
      title: "Management's Discussion & Analysis",
      description: "Management's explanation of financial results",
      difficulty: "Intermediate",
      content: "Management expressed strong confidence in Q1 performance, highlighting robust revenue growth driven by digital transformation initiatives. The fortress balance sheet strategy provides flexibility for economic volatility while maintaining strong profitability metrics.",
      part: "Part I",
      learning_objectives: "Analyze management commentary and strategic direction",
      smap_focus: "Management narrative and tone analysis"
    },
    {
      id: "market_risk",
      title: "Market Risk Disclosures",
      description: "Company's exposure to market risks",
      difficulty: "Advanced",
      content: "The company faces market risks including interest rate sensitivity, foreign exchange exposure, and credit risk. Interest rate risk is managed through asset-liability matching, with a net interest margin of 2.74%.",
      part: "Part I",
      learning_objectives: "Understand risk factors and mitigation strategies",
      smap_focus: "Risk assessment and management"
    },
    {
      id: "controls_procedures",
      title: "Controls and Procedures",
      description: "Internal controls for financial reporting",
      difficulty: "Intermediate",
      content: "Management maintains a comprehensive system of internal controls designed to ensure reliable financial reporting. No material weaknesses were identified during the quarter.",
      part: "Part I",
      learning_objectives: "Understand internal control systems",
      smap_focus: "Control environment assessment"
    },
    {
      id: "legal_proceedings",
      title: "Legal Proceedings",
      description: "Material legal matters",
      difficulty: "Beginner",
      content: "The company is involved in various legal proceedings, including regulatory investigations and civil litigation. Management believes these matters will not have a material adverse effect on the company's financial condition.",
      part: "Part II",
      learning_objectives: "Assess legal and regulatory risks",
      smap_focus: "Legal risk evaluation"
    },
    {
      id: "risk_factors",
      title: "Risk Factors",
      description: "Significant business risks",
      difficulty: "Intermediate",
      content: "Key risk factors include economic uncertainty, regulatory changes, competitive pressures, credit quality deterioration, interest rate volatility, cybersecurity threats, and operational risks.",
      part: "Part II",
      learning_objectives: "Identify and analyze business risks",
      smap_focus: "Risk factor analysis"
    },
    {
      id: "unregistered_securities",
      title: "Unregistered Securities Sales",
      description: "Information on securities transactions",
      difficulty: "Beginner",
      content: "During the quarter, the company did not engage in any unregistered sales of equity securities. All securities offerings were conducted through registered transactions.",
      part: "Part II",
      learning_objectives: "Understand securities regulations",
      smap_focus: "Securities compliance review"
    },
    {
      id: "senior_securities_defaults",
      title: "Senior Securities Defaults",
      description: "Defaults on senior securities",
      difficulty: "Beginner",
      content: "No defaults on senior securities occurred during the quarter. The company maintains strong credit ratings and has not experienced any payment defaults on its outstanding debt obligations.",
      part: "Part II",
      learning_objectives: "Monitor debt obligations",
      smap_focus: "Credit risk assessment"
    },
    {
      id: "other_information",
      title: "Other Information",
      description: "Additional company information",
      difficulty: "Intermediate",
      content: "The company continues to focus on digital transformation initiatives, including investments in technology infrastructure, cybersecurity enhancements, and customer experience improvements.",
      part: "Part II",
      learning_objectives: "Review supplementary disclosures",
      smap_focus: "Additional information analysis"
    }
  ];

  const handleSmapChange = (field, value) => {
    setSmapAnswers(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const submitSmap = async () => {
    console.log('Submitting SMAP:', smapAnswers, currentSection);
    setIsSubmitting(true);
    setError(null);
    
    try {
      // Call backend for AI-powered grading
      const response = await fetch('http://localhost:8000/api/session/demo123/practice', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'grade_submission',
          student_smap: JSON.stringify(smapAnswers),
          section: currentSection
        })
      });
      
      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      
      if (data.success && data.grading) {
        setGrading(data.grading);
      } else {
        setError(data.error || 'Failed to get AI grading. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting SMAP:', error);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const fallbackGrading = () => {
    // Enhanced simple grading logic
    const totalChars = Object.values(smapAnswers).join('').length;
    let score = Math.min(100, Math.max(20, totalChars / 5));
    
    // Bonus for having content in all fields
    const filledFields = Object.values(smapAnswers).filter(val => val.trim().length > 0).length;
    score += filledFields * 5;
    
    // Quality checks
    const hasNumbers = /[\d,.\$%]/.test(Object.values(smapAnswers).join(''));
    if (hasNumbers) score += 10;
    
    const hasAnalysis = /(analysis|assessment|evaluate|compare|trend)/i.test(Object.values(smapAnswers).join(''));
    if (hasAnalysis) score += 10;
    
    // Cap at 100
    score = Math.min(100, score);
    
    const grade = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : 'F';
    
    setGrading({
      overall_score: Math.round(score),
      letter_grade: grade,
      component_scores: {
        subjective: Math.round(score * 0.9 + Math.random() * 10),
        metrics: Math.round(score * 0.95 + Math.random() * 10),
        assessment: Math.round(score * 0.85 + Math.random() * 10),
        plan: Math.round(score * 0.8 + Math.random() * 10)
      },
      detailed_feedback: `Great work! You scored ${Math.round(score)}/100 (${grade}). Your analysis shows good understanding of the ${currentSection?.title} section. ${hasNumbers ? 'Excellent use of financial metrics!' : 'Try including more specific numbers and data.'} ${hasAnalysis ? 'Good analytical thinking!' : 'Consider adding more analysis and interpretation.'} Keep practicing to improve your SMAP analysis skills!`
    });
  };

  const resetPractice = () => {
    setCurrentSection(null);
    setGrading(null);
    setError(null);
    setIsSubmitting(false);
    setSmapAnswers({
      subjective: '',
      metrics: '',
      assessment: '',
      plan: ''
    });
  };

  if (!currentSection) {
    return (
      <div className="simple-practice">
        <div className="practice-header">
          <h1>📚 Practice Mode</h1>
          <p>Choose a section to practice your SMAP analysis skills</p>
        </div>

        <div className="sections-grid">
          {sections.map((section) => (
            <div 
              key={section.id} 
              className="section-card"
              onClick={() => setCurrentSection(section)}
            >
              <h3>{section.title}</h3>
              <p className="section-description">{section.description}</p>
              <div className="section-meta">
                <span className={`difficulty ${section.difficulty.toLowerCase()}`}>
                  {section.difficulty}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (grading) {
    return (
      <div className="simple-practice">
        <div className="grading-results">
          <h2>🎯 Your Results</h2>
          <div className="score-display">
            <div className="score-number">{grading.overall_score}</div>
            <div className="score-label">/100</div>
            <div className="grade">{grading.letter_grade}</div>
          </div>
          
          <div className="feedback">
            <h3>AI Feedback:</h3>
            <div className="feedback-content">
              {grading.detailed_feedback.split('\n').map((line, index) => {
                if (line.trim() === '') return null;
                
                // Structure the feedback based on content
                if (line.includes('OVERALL SCORE:') || line.includes('LETTER GRADE:')) {
                  return null; // Skip these as they're already displayed above
                }
                
                if (line.includes('COMPONENT SCORES:')) {
                  return null; // Skip as we show this separately
                }
                
                if (line.includes('WHAT THEY GOT RIGHT:')) {
                  return (
                    <div key={index} className="feedback-section">
                      <h4>✅ What You Did Well:</h4>
                    </div>
                  );
                }
                
                if (line.includes('AREAS FOR IMPROVEMENT:')) {
                  return (
                    <div key={index} className="feedback-section">
                      <h4>🔍 Areas for Improvement:</h4>
                    </div>
                  );
                }
                
                if (line.includes('NEXT STEPS:')) {
                  return (
                    <div key={index} className="feedback-section">
                      <h4>📈 Next Steps:</h4>
                    </div>
                  );
                }
                
                // Check if line starts with bullet points or dashes
                if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
                  return (
                    <div key={index} className="feedback-bullet">
                      <span className="bullet">•</span>
                      <span>{line.trim().substring(1).trim()}</span>
                    </div>
                  );
                }
                
                // Regular paragraph
                if (line.trim().length > 0) {
                  return (
                    <p key={index} className="feedback-paragraph">
                      {line.trim()}
                    </p>
                  );
                }
                
                return null;
              })}
            </div>
          </div>

          <div className="component-scores">
            <h3>Component Scores:</h3>
            <div className="score-grid">
              <div className="score-item">
                <span>Subjective</span>
                <span>{grading.component_scores.subjective}/100</span>
              </div>
              <div className="score-item">
                <span>Metrics</span>
                <span>{grading.component_scores.metrics}/100</span>
              </div>
              <div className="score-item">
                <span>Assessment</span>
                <span>{grading.component_scores.assessment}/100</span>
              </div>
              <div className="score-item">
                <span>Plan</span>
                <span>{grading.component_scores.plan}/100</span>
              </div>
            </div>
          </div>

          <button onClick={resetPractice} className="try-again-btn">
            Try Another Section
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="simple-practice">
      <div className="practice-header">
        <h2>Practice: {currentSection.title}</h2>
        <p>{currentSection.description}</p>
        <div className="section-content">
          <h4>Section Content:</h4>
          <p>{currentSection.content}</p>
        </div>
      </div>

      <div className="smap-form">
        <h3>Create your SMAP analysis:</h3>
        
        <div className="smap-grid">
          <div className="smap-field">
            <label>Subjective (S)</label>
            <textarea
              placeholder="Management's narrative, tone, strategic priorities..."
              value={smapAnswers.subjective}
              onChange={(e) => handleSmapChange('subjective', e.target.value)}
            />
          </div>

          <div className="smap-field">
            <label>Metrics (M)</label>
            <textarea
              placeholder="Key financial numbers, ratios, trends..."
              value={smapAnswers.metrics}
              onChange={(e) => handleSmapChange('metrics', e.target.value)}
            />
          </div>

          <div className="smap-field">
            <label>Assessment (A)</label>
            <textarea
              placeholder="Analysis of performance, risks, strengths..."
              value={smapAnswers.assessment}
              onChange={(e) => handleSmapChange('assessment', e.target.value)}
            />
          </div>

          <div className="smap-field">
            <label>Plan (P)</label>
            <textarea
              placeholder="Future outlook, strategic initiatives..."
              value={smapAnswers.plan}
              onChange={(e) => handleSmapChange('plan', e.target.value)}
            />
          </div>
        </div>

        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        <div className="submit-section">
          <button 
            onClick={submitSmap} 
            className="submit-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Grading with AI...' : 'Submit for AI Grading'}
          </button>
          <button onClick={resetPractice} className="back-btn">
            Back to Sections
          </button>
        </div>
      </div>
    </div>
  );
}

export default SimplePractice;
