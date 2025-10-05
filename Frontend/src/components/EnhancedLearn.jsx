import { useState } from "react";
import "../styles/enhanced-learn.css";

function EnhancedLearn() {
  // State for active tab: 'summary', 'quiz'
  const [activeTab, setActiveTab] = useState('summary');
  
  // State for quiz answers
  const [quizAnswers, setQuizAnswers] = useState({
    q1: null,
    q2: null,
    q3: null,
    q4: null,
    q5: null
  });

  // Mock company data - in real app this would come from props or API
  const companyData = {
    name: "Apple Inc.",
    ticker: "AAPL",
    quarter: "Q1 2024",
    summary: {
      keyMetrics: `
        Apple reported strong Q1 2024 results with revenue of $119.6 billion, up 2% year-over-year. 
        The company's gross margin improved to 46.6% from 43.0% in the prior year quarter, 
        driven by favorable mix and cost efficiencies. Net income reached $33.9 billion, 
        representing a 13% increase compared to Q1 2023.
      `,
      topInsights: `
        iPhone revenue remained resilient at $69.7 billion despite market headwinds, 
        while Services revenue reached a new all-time high of $23.1 billion, up 11% year-over-year. 
        The company's active installed base of devices reached a new record across all geographic segments, 
        supporting continued Services growth and ecosystem monetization.
      `,
      trendHighlights: `
        China revenue declined 13% year-over-year to $20.8 billion, reflecting competitive pressures 
        and macroeconomic challenges. However, emerging markets showed strong growth with India 
        revenue setting a new record. The company continues to invest heavily in R&D, spending 
        $7.7 billion in the quarter, focused on AI, augmented reality, and other future technologies.
      `
    }
  };

  // Quiz questions and answers
  const quizQuestions = [
    {
      id: 'q1',
      question: 'What was Apple\'s Q1 2024 revenue?',
      type: 'multiple-choice',
      options: [
        { value: '115.6', label: '$115.6 billion' },
        { value: '119.6', label: '$119.6 billion' },
        { value: '123.6', label: '$123.6 billion' },
        { value: '127.6', label: '$127.6 billion' }
      ],
      correct: '119.6',
      explanation: 'Apple reported revenue of $119.6 billion in Q1 2024, representing a 2% year-over-year increase.'
    },
    {
      id: 'q2',
      question: 'Which segment showed the strongest year-over-year growth?',
      type: 'multiple-choice',
      options: [
        { value: 'iphone', label: 'iPhone' },
        { value: 'services', label: 'Services' },
        { value: 'mac', label: 'Mac' },
        { value: 'ipad', label: 'iPad' }
      ],
      correct: 'services',
      explanation: 'Services revenue grew 11% year-over-year to $23.1 billion, reaching a new all-time high.'
    },
    {
      id: 'q3',
      question: 'Apple\'s gross margin improved significantly in Q1 2024.',
      type: 'true-false',
      options: [
        { value: 'true', label: 'True' },
        { value: 'false', label: 'False' }
      ],
      correct: 'true',
      explanation: 'Gross margin improved to 46.6% from 43.0% in the prior year quarter, driven by favorable mix and cost efficiencies.'
    },
    {
      id: 'q4',
      question: 'What was the primary driver of Apple\'s improved gross margin?',
      type: 'multiple-choice',
      options: [
        { value: 'price_increases', label: 'Price increases on existing products' },
        { value: 'cost_reductions', label: 'Favorable product mix and cost efficiencies' },
        { value: 'new_products', label: 'Higher margins on new products' },
        { value: 'currency_benefits', label: 'Foreign exchange benefits' }
      ],
      correct: 'cost_reductions',
      explanation: 'The improved gross margin was primarily driven by favorable product mix and cost efficiencies, not price increases.'
    },
    {
      id: 'q5',
      question: 'Which geographic region showed the strongest performance?',
      type: 'multiple-choice',
      options: [
        { value: 'china', label: 'China' },
        { value: 'india', label: 'India' },
        { value: 'europe', label: 'Europe' },
        { value: 'americas', label: 'Americas' }
      ],
      correct: 'india',
      explanation: 'India revenue set a new record, while China revenue declined 13% year-over-year due to competitive pressures.'
    }
  ];

  const handleQuizAnswer = (questionId, answer) => {
    setQuizAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmitQuiz = () => {
    const answeredQuestions = Object.values(quizAnswers).filter(answer => answer !== null);
    const totalQuestions = quizQuestions.length;
    const correctAnswers = quizQuestions.filter(q => quizAnswers[q.id] === q.correct).length;
    
    alert(`Quiz submitted! You answered ${answeredQuestions.length}/${totalQuestions} questions. 
Correct answers: ${correctAnswers}/${totalQuestions}
Score: ${Math.round((correctAnswers / totalQuestions) * 100)}%`);
  };

  const renderQuizQuestion = (question) => {
    return (
      <div key={question.id} className="quiz-question">
        <h4>{question.question}</h4>
        <div className="quiz-options">
          {question.options.map(option => (
            <label key={option.value} className="quiz-option">
              <input
                type={question.type === 'true-false' ? 'radio' : 'radio'}
                name={question.id}
                value={option.value}
                checked={quizAnswers[question.id] === option.value}
                onChange={(e) => handleQuizAnswer(question.id, e.target.value)}
              />
              <span className="option-text">{option.label}</span>
            </label>
          ))}
        </div>
        {quizAnswers[question.id] && (
          <div className="quiz-explanation">
            <strong>Explanation:</strong> {question.explanation}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="enhanced-learn">
      <div className="learn-header">
        <div className="company-info">
          <h1>{companyData.name}</h1>
          <p className="company-subtitle">
            {companyData.ticker} • {companyData.quarter} • Enhanced Learning Mode
          </p>
        </div>
        <div className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveTab('summary')}
          >
            📊 Summary
          </button>
          <button 
            className={`tab-button ${activeTab === 'quiz' ? 'active' : ''}`}
            onClick={() => setActiveTab('quiz')}
          >
            🧠 Quiz
          </button>
        </div>
      </div>

      <div className="learn-content">
        {activeTab === 'summary' && (
          <div className="summary-tab">
            <div className="summary-section">
              <h2>📈 Key Metrics at a Glance</h2>
              <div className="summary-content">
                <p>{companyData.summary.keyMetrics}</p>
                <div className="key-numbers">
                  <div className="metric-card">
                    <div className="metric-value">$119.6B</div>
                    <div className="metric-label">Revenue</div>
                    <div className="metric-change positive">+2% YoY</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-value">46.6%</div>
                    <div className="metric-label">Gross Margin</div>
                    <div className="metric-change positive">+3.6pp</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-value">$33.9B</div>
                    <div className="metric-label">Net Income</div>
                    <div className="metric-change positive">+13% YoY</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="summary-section">
              <h2>💡 Top Insights</h2>
              <div className="summary-content">
                <p>{companyData.summary.topInsights}</p>
                <div className="insight-highlights">
                  <div className="insight-item">
                    <span className="insight-icon">📱</span>
                    <div>
                      <strong>iPhone Resilience:</strong> $69.7B revenue despite market headwinds
                    </div>
                  </div>
                  <div className="insight-item">
                    <span className="insight-icon">🔄</span>
                    <div>
                      <strong>Services Growth:</strong> New record $23.1B (+11% YoY)
                    </div>
                  </div>
                  <div className="insight-item">
                    <span className="insight-icon">🌍</span>
                    <div>
                      <strong>Global Reach:</strong> Record active installed base across all regions
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="summary-section">
              <h2>📊 Trend Highlights</h2>
              <div className="summary-content">
                <p>{companyData.summary.trendHighlights}</p>
                <div className="trend-analysis">
                  <div className="trend-item negative">
                    <span className="trend-icon">📉</span>
                    <div>
                      <strong>China:</strong> Revenue declined 13% to $20.8B due to competitive pressures
                    </div>
                  </div>
                  <div className="trend-item positive">
                    <span className="trend-icon">📈</span>
                    <div>
                      <strong>India:</strong> Record revenue performance in emerging markets
                    </div>
                  </div>
                  <div className="trend-item neutral">
                    <span className="trend-icon">🔬</span>
                    <div>
                      <strong>R&D Investment:</strong> $7.7B focused on AI, AR, and future technologies
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="action-buttons">
              <button 
                className="action-btn primary"
                onClick={() => setActiveTab('quiz')}
              >
                Take Quiz →
              </button>
              <button className="action-btn secondary">
                Save Summary
              </button>
            </div>
          </div>
        )}

        {activeTab === 'quiz' && (
          <div className="quiz-tab">
            <div className="quiz-header">
              <h2>🧠 Knowledge Check</h2>
              <p>Test your understanding of Apple's Q1 2024 performance</p>
            </div>

            <div className="quiz-questions">
              {quizQuestions.map(renderQuizQuestion)}
            </div>

            <div className="quiz-actions">
              <button 
                className="submit-btn"
                onClick={handleSubmitQuiz}
                disabled={Object.values(quizAnswers).every(answer => answer === null)}
              >
                Submit Quiz
              </button>
              <button 
                className="reset-btn"
                onClick={() => setQuizAnswers({
                  q1: null, q2: null, q3: null, q4: null, q5: null
                })}
              >
                Reset Answers
              </button>
            </div>

            <div className="quiz-progress">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ 
                    width: `${(Object.values(quizAnswers).filter(a => a !== null).length / quizQuestions.length) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="progress-text">
                {Object.values(quizAnswers).filter(a => a !== null).length} / {quizQuestions.length} questions answered
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default EnhancedLearn;
