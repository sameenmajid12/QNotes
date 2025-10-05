import { useState } from 'react';
import '../styles/practice.css';

function Practice() {
  const [answers, setAnswers] = useState({
    question1: 'dolor',
    question2: 'false'
  });

  const handleAnswerChange = (question, value) => {
    setAnswers(prev => ({ ...prev, [question]: value }));
  };

  return (
    <div className="practice">
      <div className="practice-header">
        <h1>Practice mode</h1>
        <p className="practice-description">
          Fill in your own SMAP notes, identify key metrics, risks, and next steps,
          <br />
          and get instant AI feedback to see what you got right and what you missed.
        </p>
        <div className="header-underline"></div>
      </div>

      <section className="smap-section">
        <h2 className="section-title">SMAP Notes</h2>

        <div className="smap-grid">
          <div className="smap-field">
            <label className="smap-label">Summary</label>
            <textarea
              className="smap-textarea"
              placeholder="Summarize the main points in a few sentences"
              rows="6"
            />
          </div>

          <div className="smap-field">
            <label className="smap-label">Metric</label>
            <textarea
              className="smap-textarea"
              placeholder="Highlight the metrics that matter most — revenue, EPS, margins, cash flow."
              rows="6"
            />
          </div>

          <div className="smap-field">
            <label className="smap-label">Assessment</label>
            <textarea
              className="smap-textarea"
              placeholder="Explain what these numbers imply about the company's health"
              rows="6"
            />
          </div>

          <div className="smap-field">
            <label className="smap-label">Plan</label>
            <textarea
              className="smap-textarea"
              placeholder="What would you recommend next based on this info?"
              rows="6"
            />
          </div>
        </div>
      </section>

      <section className="quiz-section">
        <h2 className="section-title">Quiz</h2>

        <div className="quiz-question">
          <p className="question-label">Question 1</p>
          <p className="question-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor <strong>incididunt</strong> ut labore et dolore magna aliqua?
          </p>

          <div className="options">
            {['dolor', 'Lorem ipsum', 'labore et', 'aliqua', 'consectetur'].map((option) => (
              <label key={option} className="option">
                <input
                  type="radio"
                  name="question1"
                  value={option}
                  checked={answers.question1 === option}
                  onChange={(e) => handleAnswerChange('question1', e.target.value)}
                />
                <span className="option-label">{option}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="quiz-divider"></div>

        <div className="quiz-question">
          <p className="question-label">Question 2</p>
          <p className="question-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor <strong>incididunt</strong> ut labore et dolore magna aliqua?
          </p>

          <div className="options">
            {['True', 'False'].map((option) => (
              <label key={option} className="option">
                <input
                  type="radio"
                  name="question2"
                  value={option.toLowerCase()}
                  checked={answers.question2 === option.toLowerCase()}
                  onChange={(e) => handleAnswerChange('question2', e.target.value)}
                />
                <span className="option-label">{option}</span>
              </label>
            ))}
          </div>
        </div>
      </section>

      <div className="submit-section">
        <p className="submit-prompt">Ready to submit and get feedback?</p>
        <button className="submit-btn">Submit</button>
      </div>
    </div>
  );
}

export default Practice;
