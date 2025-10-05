import React, { useState, useEffect } from 'react'
import './App.css'

// Main App Component for 10Q Notes AI
function App() {
  const [currentView, setCurrentView] = useState('upload')
  const [sessionData, setSessionData] = useState(null)
  const [studentData, setStudentData] = useState(null)
  const [currentMode, setCurrentMode] = useState('learn')
  const [smapData, setSmapData] = useState(null)
  const [feedbackData, setFeedbackData] = useState(null)

  // Mock API calls (in production, these would be real API calls)
  const mockApiCall = async (endpoint, data = {}) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock responses based on endpoint
    switch (endpoint) {
      case '/api/auth/login':
        return {
          success: true,
          student: {
            student_id: 'john_smith_rutgers_edu',
            name: 'John Smith',
            email: 'john.smith@rutgers.edu',
            university: 'Rutgers',
            total_sessions: 3,
            average_score: 85.5,
            streak_days: 7
          }
        }
      case '/api/upload/filing':
        return {
          success: true,
          session: {
            session_id: 'abc123',
            company_name: 'JPMorgan Chase & Co.',
            ticker: 'JPM',
            filing_type: '10-Q',
            filing_period: 'Q1 2025',
            status: 'active'
          }
        }
      default:
        return { success: true, data: {} }
    }
  }

  const handleLogin = async (email, name) => {
    try {
      const response = await mockApiCall('/api/auth/login', { email, name })
      if (response.success) {
        setStudentData(response.student)
        setCurrentView('dashboard')
      }
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  const handleFileUpload = async (file) => {
    try {
      const response = await mockApiCall('/api/upload/filing', { file })
      if (response.success) {
        setSessionData(response.session)
        setCurrentView('smap-dashboard')
        // Mock SMAP data
        setSmapData({
          subjective: "Management expressed strong confidence in Q1 performance, highlighting robust revenue growth and disciplined expense management. The tone was optimistic about future opportunities in digital banking and maintained focus on fortress balance sheet strategy.",
          metrics: "Total revenue of $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, Net interest margin 2.74%, Book value per share $95.35",
          assessment: "JPMorgan demonstrates solid fundamental strength with revenue growth across segments. The fortress balance sheet provides flexibility for economic volatility while maintaining strong profitability metrics. Credit provisions remain well-controlled despite economic uncertainty.",
          plan: "1. Monitor credit provision trends for potential economic impact 2. Assess interest rate sensitivity and NIM expansion opportunities 3. Evaluate investment banking recovery in market conditions 4. Track digital transformation progress and efficiency gains"
        })
      }
    } catch (error) {
      console.error('Upload failed:', error)
    }
  }

  const handlePracticeMode = () => {
    setCurrentMode('practice')
  }

  const handleVoiceAgentMode = () => {
    setCurrentMode('voice_agent')
  }

  // Render different views
  if (currentView === 'upload') {
    return <UploadView onLogin={handleLogin} onFileUpload={handleFileUpload} />
  }

  if (currentView === 'dashboard') {
    return <DashboardView studentData={studentData} onFileUpload={handleFileUpload} />
  }

  if (currentView === 'smap-dashboard') {
    return (
      <SMAPDashboard 
        sessionData={sessionData}
        smapData={smapData}
        currentMode={currentMode}
        onModeChange={setCurrentMode}
        onPracticeMode={handlePracticeMode}
        onVoiceAgentMode={handleVoiceAgentMode}
      />
    )
  }

  return <div>Loading...</div>
}

// Upload View Component
function UploadView({ onLogin, onFileUpload }) {
  const [email, setEmail] = useState('john.smith@rutgers.edu')
  const [name, setName] = useState('John Smith')
  const [file, setFile] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (file) {
      onFileUpload(file)
    } else {
      onLogin(email, name)
    }
  }

  return (
    <div className="upload-view">
      <div className="header">
        <h1>🔹 10Q Notes AI</h1>
        <p className="tagline">Transform 10-Q and 10-K filings into structured SMAP Notes</p>
        <p className="subtitle">The Bloomberg Terminal for students and analysts</p>
      </div>

      <div className="upload-container">
        <div className="login-section">
          <h2>Student Login</h2>
          <div className="form-group">
            <label>Email (.edu required)</label>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
              placeholder="student@university.edu"
            />
          </div>
          <div className="form-group">
            <label>Name</label>
            <input 
              type="text" 
              value={name} 
              onChange={(e) => setName(e.target.value)}
              placeholder="Your Name"
            />
          </div>
        </div>

        <div className="upload-section">
          <h2>Upload SEC Filing</h2>
          <div className="upload-options">
            <div className="upload-option">
              <label className="file-upload">
                📄 Upload SEC Filing (10-Q / 10-K PDF)
                <input 
                  type="file" 
                  accept=".pdf,.txt"
                  onChange={(e) => setFile(e.target.files[0])}
                  style={{display: 'none'}}
                />
              </label>
            </div>
            <div className="upload-option">
              <label>🔗 Paste Filing Link (EDGAR, Yahoo Finance)</label>
              <input type="url" placeholder="https://..." />
            </div>
            <div className="upload-option">
              <label>📝 Paste Raw Text</label>
              <textarea placeholder="Paste SEC filing text here..."></textarea>
            </div>
          </div>
        </div>

        <button className="cta-button" onClick={handleSubmit}>
          {file ? 'Generate SMAP Notes' : 'Continue to Dashboard'}
        </button>
      </div>

      <div className="features-preview">
        <h3>🎯 What You'll Get</h3>
        <div className="features-grid">
          <div className="feature-card">
            <h4>S – Subjective</h4>
            <p>What management said - narratives, tone, qualitative insights</p>
          </div>
          <div className="feature-card">
            <h4>M – Metrics</h4>
            <p>Hard numbers, ratios, financials pulled directly from filings</p>
          </div>
          <div className="feature-card">
            <h4>A – Assessment</h4>
            <p>AI interprets meaning of metrics + narrative</p>
          </div>
          <div className="feature-card">
            <h4>P – Plan</h4>
            <p>Next steps for investor/analyst, compliance or strategy</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// Dashboard View Component
function DashboardView({ studentData, onFileUpload }) {
  return (
    <div className="dashboard-view">
      <div className="header">
        <h1>🔹 10Q Notes AI Dashboard</h1>
        <div className="student-info">
          <h2>Welcome, {studentData?.name}!</h2>
          <p>{studentData?.university} • {studentData?.total_sessions} sessions completed</p>
          <p>Average Score: {studentData?.average_score}/100 • Streak: {studentData?.streak_days} days</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="quick-upload">
          <h3>📄 Start New Analysis</h3>
          <div className="upload-options">
            <label className="file-upload">
              Upload 10-Q or 10-K Filing
              <input 
                type="file" 
                accept=".pdf,.txt"
                onChange={(e) => onFileUpload(e.target.files[0])}
                style={{display: 'none'}}
              />
            </label>
          </div>
        </div>

        <div className="learning-modes">
          <h3>🎓 Learning Modes</h3>
          <div className="mode-cards">
            <div className="mode-card">
              <h4>📖 Learn Mode</h4>
              <p>Study AI-generated SMAP notes with interactive explanations</p>
              <button className="mode-button">Start Learning</button>
            </div>
            <div className="mode-card">
              <h4>✍️ Practice Mode</h4>
              <p>Write your own SMAP notes and get instant feedback</p>
              <button className="mode-button">Start Practice</button>
            </div>
            <div className="mode-card voice-agent">
              <h4>🎤 Voice Agent</h4>
              <p>Practice investor calls with AI-powered voice agent and realistic simulations</p>
              <button className="mode-button voice-button">Start Voice Practice</button>
            </div>
          </div>
        </div>

        <div className="recent-sessions">
          <h3>📊 Recent Sessions</h3>
          <div className="session-card">
            <h4>JPMorgan Chase & Co. (JPM)</h4>
            <p>10-Q Q1 2025 • Learn Mode Completed</p>
            <span className="status completed">Completed</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// SMAP Dashboard Component
function SMAPDashboard({ 
  sessionData, 
  smapData, 
  currentMode, 
  onModeChange, 
  onPracticeMode, 
  onVoiceAgentMode 
}) {
  return (
    <div className="smap-dashboard">
      <div className="header">
        <h1>🔹 SMAP Analysis: {sessionData?.company_name}</h1>
        <div className="session-info">
          <span className="ticker">{sessionData?.ticker}</span>
          <span className="filing">{sessionData?.filing_type} • {sessionData?.filing_period}</span>
        </div>
      </div>

      <div className="mode-selector">
        <button 
          className={currentMode === 'learn' ? 'active' : ''}
          onClick={() => onModeChange('learn')}
        >
          📖 Learn Mode
        </button>
        <button 
          className={currentMode === 'practice' ? 'active' : ''}
          onClick={onPracticeMode}
        >
          ✍️ Practice Mode
        </button>
        <button 
          className={currentMode === 'voice_agent' ? 'active' : ''}
          onClick={onVoiceAgentMode}
        >
          🎤 Voice Agent
        </button>
      </div>

      <div className="smap-content">
        {currentMode === 'learn' && <LearnModeView smapData={smapData} />}
        {currentMode === 'practice' && <PracticeModeView sessionData={sessionData} />}
        {currentMode === 'voice_agent' && <VoiceAgentView sessionData={sessionData} />}
      </div>
    </div>
  )
}

// Learn Mode Component
function LearnModeView({ smapData }) {
  const [activeSection, setActiveSection] = useState('subjective')

  const sections = [
    {
      id: 'subjective',
      title: 'S – Subjective',
      subtitle: 'What Management Said',
      icon: '🗣️',
      content: smapData?.subjective || 'Loading...',
      explanation: 'This section captures the narrative and tone from management, including strategic priorities and forward-looking statements.'
    },
    {
      id: 'metrics',
      title: 'M – Metrics',
      subtitle: 'Key Financial Numbers',
      icon: '📊',
      content: smapData?.metrics || 'Loading...',
      explanation: 'Hard numbers, ratios, and financial data extracted directly from the filing.'
    },
    {
      id: 'assessment',
      title: 'A – Assessment',
      subtitle: 'What It All Means',
      icon: '🧐',
      content: smapData?.assessment || 'Loading...',
      explanation: 'AI interprets the numbers and narrative to identify trends, strengths, and concerns.'
    },
    {
      id: 'plan',
      title: 'P – Plan',
      subtitle: 'Recommended Next Steps',
      icon: '✅',
      content: smapData?.plan || 'Loading...',
      explanation: 'Specific actionable recommendations for investors, analysts, or advisors.'
    }
  ]

  return (
    <div className="learn-mode">
      <div className="sections-sidebar">
        <h3>SMAP Sections</h3>
        {sections.map(section => (
          <button
            key={section.id}
            className={`section-button ${activeSection === section.id ? 'active' : ''}`}
            onClick={() => setActiveSection(section.id)}
          >
            <span className="icon">{section.icon}</span>
      <div>
              <div className="title">{section.title}</div>
              <div className="subtitle">{section.subtitle}</div>
            </div>
          </button>
        ))}
      </div>

      <div className="section-content">
        {sections.map(section => (
          activeSection === section.id && (
            <div key={section.id} className="section-detail">
              <div className="section-header">
                <h2>{section.icon} {section.title}</h2>
                <p className="explanation">{section.explanation}</p>
              </div>
              <div className="content">
                <p>{section.content}</p>
              </div>
              <div className="learning-tools">
                <button className="tool-button">🎤 Listen to Audio</button>
                <button className="tool-button">💡 Key Concepts</button>
                <button className="tool-button">📚 Flashcards</button>
              </div>
            </div>
          )
        ))}
      </div>
    </div>
  )
}

// Feedback Mode Component

// Practice Mode Component
function PracticeModeView({ sessionData }) {
  const [currentStep, setCurrentStep] = useState('sections') // 'sections', 'teaching', 'practice', 'grading', 'insights'
  const [sections, setSections] = useState([])
  const [currentSection, setCurrentSection] = useState(null)
  const [teachingData, setTeachingData] = useState(null)
  const [studentSmap, setStudentSmap] = useState({ subjective: '', metrics: '', assessment: '', plan: '' })
  const [gradingData, setGradingData] = useState(null)
  const [sessionHistory, setSessionHistory] = useState([])
  const [insights, setInsights] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const extractSections = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/practice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'get_sections',
          filing_content: sessionData?.filing_content || 'Demo filing content for practice mode'
        })
      })
      
      const result = await response.json()
      if (result.success) {
        setSections(result.sections)
        setCurrentStep('sections')
      } else {
        alert('Error extracting sections: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const startTeaching = async (section) => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/practice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'teach_smap',
          section: section
        })
      })
      
      const result = await response.json()
      if (result.success) {
        setCurrentSection(section)
        setTeachingData(result.teaching)
        setCurrentStep('teaching')
      } else {
        alert('Error loading teaching: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const submitSmap = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/practice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'grade_submission',
          student_smap: studentSmap,
          section: currentSection,
          teaching_data: teachingData
        })
      })
      
      const result = await response.json()
      if (result.success) {
        setGradingData(result.grading)
        setCurrentStep('grading')
        
        // Add to session history
        const newSession = {
          section_title: currentSection.title,
          overall_score: result.grading.overall_score,
          difficulty: currentSection.difficulty,
          date: new Date().toISOString()
        }
        setSessionHistory([...sessionHistory, newSession])
      } else {
        alert('Error grading submission: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const getInsights = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/practice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'get_insights',
          session_history: sessionHistory
        })
      })
      
      const result = await response.json()
      if (result.success) {
        setInsights(result.insights)
        setCurrentStep('insights')
      } else {
        alert('Error getting insights: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const assignNextSection = async () => {
    setIsLoading(true)
    try {
      const completedSections = sessionHistory.map(s => s.section_title.toLowerCase().replace(/\s+/g, '_'))
      const response = await fetch(`http://localhost:8000/api/session/demo123/practice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'assign_next_section',
          completed_sections: completedSections,
          available_sections: sections
        })
      })
      
      const result = await response.json()
      if (result.success && result.assignment.section) {
        await startTeaching(result.assignment.section)
      } else {
        alert('All sections completed! Great job!')
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  // Initialize sections when component mounts
  useEffect(() => {
    extractSections()
  }, [])

  return (
    <div className="practice-mode-view">
      <div className="header">
        <h2>🎯 Practice Mode - Interactive SMAP Learning</h2>
        <button className="back-button">← Back to Dashboard</button>
      </div>
      
      {currentStep === 'sections' && (
          <div className="sections-step">
            <h3>📄 Available Practice Sections</h3>
            <p>Choose a section to practice your SMAP analysis skills:</p>
          
          <div className="sections-grid">
            {sections.map((section, index) => (
              <div key={section.id} className="section-card">
                <h4>{section.title}</h4>
                <p>{section.description}</p>
                <div className="section-meta">
                  <span className={`difficulty ${section.difficulty}`}>
                    {section.difficulty.toUpperCase()}
                  </span>
                  <span className="smap-focus">{section.smap_focus}</span>
                </div>
                <button 
                  className="start-practice-btn"
                  onClick={() => startTeaching(section)}
                  disabled={isLoading}
                >
                  {isLoading ? 'Loading...' : 'Start Practice'}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {currentStep === 'teaching' && (
        <div className="teaching-step">
          <h3>📚 Learning SMAP Framework</h3>
          <h4>Section: {currentSection.title}</h4>
          
          <div className="smap-explanation">
            <h4>🎯 SMAP Framework Components</h4>
            {teachingData && Object.entries(teachingData.smap_explanation).map(([component, data]) => (
              <div key={component} className="smap-component">
                <h5>{component.toUpperCase()}</h5>
                <p><strong>Definition:</strong> {data.definition}</p>
                <p><strong>Examples:</strong> {data.examples.join(', ')}</p>
                <p><strong>For this section:</strong> {data.for_this_section}</p>
              </div>
            ))}
          </div>
          
          <div className="example-smap">
            <h4>💡 Example SMAP Analysis</h4>
            {teachingData && Object.entries(teachingData.example_smap).map(([component, content]) => (
              <div key={component} className="example-component">
                <strong>{component.toUpperCase()}:</strong> {content}
              </div>
            ))}
          </div>
          
          <div className="learning-tips">
            <h4>💡 Learning Tips</h4>
            <ul>
              {teachingData?.learning_tips.map((tip, index) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </div>
          
          <button 
            className="start-practice-btn"
            onClick={() => setCurrentStep('practice')}
          >
            Ready to Practice! →
          </button>
        </div>
      )}

      {currentStep === 'practice' && (
        <div className="practice-step">
          <h3>✏️ Create Your SMAP Analysis</h3>
          <h4>Section: {currentSection.title}</h4>
          
          <div className="section-content">
            <h5>📄 Section Content:</h5>
            <p>{currentSection.content}</p>
          </div>
          
          <div className="smap-input-form">
            <div className="smap-input">
              <label>Subjective (S)</label>
              <textarea 
                value={studentSmap.subjective}
                onChange={(e) => setStudentSmap({...studentSmap, subjective: e.target.value})}
                placeholder="What are management's opinions and tone?"
              />
            </div>
            
            <div className="smap-input">
              <label>Metrics (M)</label>
              <textarea 
                value={studentSmap.metrics}
                onChange={(e) => setStudentSmap({...studentSmap, metrics: e.target.value})}
                placeholder="What are the key numbers and ratios?"
              />
            </div>
            
            <div className="smap-input">
              <label>Assessment (A)</label>
              <textarea 
                value={studentSmap.assessment}
                onChange={(e) => setStudentSmap({...studentSmap, assessment: e.target.value})}
                placeholder="How is the company performing?"
              />
            </div>
            
            <div className="smap-input">
              <label>Plan (P)</label>
              <textarea 
                value={studentSmap.plan}
                onChange={(e) => setStudentSmap({...studentSmap, plan: e.target.value})}
                placeholder="What are the strategic initiatives?"
              />
            </div>
          </div>
          
          <button 
            className="submit-btn"
            onClick={submitSmap}
            disabled={isLoading}
          >
            {isLoading ? 'Grading...' : 'Submit SMAP Analysis'}
          </button>
        </div>
      )}

      {currentStep === 'grading' && (
        <div className="grading-step">
          <h3>📊 Your Results</h3>
          
          <div className="grade-summary">
            <div className="overall-score">
              <h4>Overall Score: {gradingData.overall_score}/100</h4>
              <span className={`grade-letter ${gradingData.grade_letter}`}>
                {gradingData.grade_letter}
              </span>
            </div>
          </div>
          
          <div className="component-scores">
            <h4>📈 Component Breakdown</h4>
            {Object.entries(gradingData.component_scores).map(([component, data]) => (
              <div key={component} className="component-score">
                <h5>{component.toUpperCase()}: {data.score}/100</h5>
                <p><strong>Feedback:</strong> {data.feedback}</p>
                {data.strengths.length > 0 && (
                  <p><strong>Strengths:</strong> {data.strengths.join(', ')}</p>
                )}
                {data.improvements.length > 0 && (
                  <p><strong>Improvements:</strong> {data.improvements.join(', ')}</p>
                )}
              </div>
            ))}
          </div>
          
          <div className="detailed-feedback">
            <h4>💬 Detailed Feedback</h4>
            <div className="feedback-section">
              <h5>✅ What You Did Well:</h5>
              <ul>
                {gradingData.detailed_feedback.what_you_did_well.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            
            <div className="feedback-section">
              <h5>🎯 Areas for Improvement:</h5>
              <ul>
                {gradingData.detailed_feedback.areas_for_improvement.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            
            <div className="feedback-section">
              <h5>📋 Next Steps:</h5>
              <ul>
                {gradingData.detailed_feedback.next_steps.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="encouragement">
            <p><em>{gradingData.encouragement}</em></p>
          </div>
          
          <div className="grading-actions">
            <button 
              className="insights-btn"
              onClick={getInsights}
              disabled={isLoading}
            >
              📊 View Progress Insights
            </button>
            <button 
              className="next-section-btn"
              onClick={assignNextSection}
              disabled={isLoading}
            >
              ➡️ Practice Next Section
            </button>
          </div>
        </div>
      )}

      {currentStep === 'insights' && (
        <div className="insights-step">
          <h3>📊 Your Learning Progress</h3>
          
          <div className="progress-overview">
            <h4>📈 Overall Progress</h4>
            <div className="progress-stats">
              <div className="stat">
                <span className="stat-value">{insights.overall_progress.average_score}</span>
                <span className="stat-label">Average Score</span>
              </div>
              <div className="stat">
                <span className="stat-value">{insights.overall_progress.total_sessions}</span>
                <span className="stat-label">Sessions</span>
              </div>
              <div className="stat">
                <span className="stat-value">{insights.overall_progress.trend}</span>
                <span className="stat-label">Trend</span>
              </div>
            </div>
          </div>
          
          <div className="strengths-weaknesses">
            <div className="strengths">
              <h4>✅ Your Strengths</h4>
              <ul>
                {insights.strengths.map((strength, index) => (
                  <li key={index}>{strength}</li>
                ))}
              </ul>
            </div>
            
            <div className="weaknesses">
              <h4>🎯 Areas to Improve</h4>
              <ul>
                {insights.weaknesses.map((weakness, index) => (
                  <li key={index}>{weakness}</li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="recommendations">
            <h4>💡 Recommendations</h4>
            <ul>
              {insights.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
          
          <div className="next-focus">
            <h4>🎯 Next Focus Areas</h4>
            <ul>
              {insights.next_focus.map((focus, index) => (
                <li key={index}>{focus}</li>
              ))}
            </ul>
          </div>
          
          <div className="insights-actions">
            <button 
              className="next-section-btn"
              onClick={assignNextSection}
              disabled={isLoading}
            >
              ➡️ Continue Practice
            </button>
            <button 
              className="restart-btn"
              onClick={() => setCurrentStep('sections')}
            >
              🔄 Choose Different Section
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// Comparison Mode Component
function VoiceAgentView({ sessionData }) {
  const [currentMode, setCurrentMode] = useState('convai') // 'convai' or 'audio'
  const [convaiAgent, setConvaiAgent] = useState(null)
  const [voiceContent, setVoiceContent] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [convaiReady, setConvaiReady] = useState(false)

  const initializeConvAI = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/convai`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'get_info'
        })
      })
      
      const result = await response.json()
      
      if (result.success) {
        setConvaiAgent(result.convai_agent)
        setConvaiReady(true)
      } else {
        alert('Error initializing ConvAI: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const generateVoiceContent = async (voiceType) => {
    setIsLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/demo123/voice`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          voice_type: voiceType
        })
      })
      
      const result = await response.json()
      
      if (result.success) {
        setVoiceContent(result.voice_content)
      } else {
        alert('Error generating voice content: ' + (result.error || 'Unknown error'))
      }
    } catch (error) {
      alert('Error: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  // Initialize ConvAI when component mounts
  useEffect(() => {
    initializeConvAI()
  }, [])

  return (
    <div className="voice-agent-view">
      <div className="header">
        <h2>🎤 Voice Agent - Practice Investor Calls</h2>
        <button className="back-button">← Back to Dashboard</button>
      </div>
      
      {/* Mode Toggle */}
      <div className="mode-toggle">
        <button 
          className={`mode-button ${currentMode === 'convai' ? 'active' : ''}`}
          onClick={() => setCurrentMode('convai')}
        >
          🤖 Interactive ConvAI Agent
        </button>
        <button 
          className={`mode-button ${currentMode === 'audio' ? 'active' : ''}`}
          onClick={() => setCurrentMode('audio')}
        >
          🎧 Audio Content
        </button>
      </div>
      
      <div className="voice-content">
        {currentMode === 'convai' ? (
          <div className="convai-section">
            <h3>🤖 Interactive ConvAI Agent</h3>
            <p>Practice investor calls with our AI financial advisor. Ask questions about earnings, financial metrics, and investment strategies.</p>
            
            {convaiAgent && convaiReady ? (
              <div className="convai-widget-container">
                <div className="convai-info">
                  <h4>🎯 Agent Ready</h4>
                  <p><strong>Agent ID:</strong> {convaiAgent.agent_id}</p>
                  <p><strong>Type:</strong> {convaiAgent.type}</p>
                  <p><strong>Capabilities:</strong> {convaiAgent.capabilities.join(', ')}</p>
                </div>
                
                {/* ConvAI Widget */}
                <div className="convai-widget">
                  <elevenlabs-convai agent-id="agent_2001k6r67ejzejx930t22kwwaw5j"></elevenlabs-convai>
                </div>
                
                <div className="convai-instructions">
                  <h4>💡 How to Use:</h4>
                  <ul>
                    <li>Click the microphone to start talking</li>
                    <li>Ask about Apple's financial performance</li>
                    <li>Practice investor questions and analysis</li>
                    <li>Get AI feedback on your understanding</li>
                  </ul>
                </div>
              </div>
            ) : (
              <div className="convai-loading">
                {isLoading ? (
                  <p>🔄 Initializing ConvAI agent...</p>
                ) : (
                  <p>❌ ConvAI agent not available. Check API key permissions.</p>
                )}
              </div>
            )}
          </div>
        ) : (
          <div className="audio-section">
            <h3>🎤 Audio Content Generation</h3>
            <p>Generate realistic financial audio content using ElevenLabs Text-to-Speech. Choose from earnings calls, SMAP briefings, or interactive quizzes.</p>
            
            <div className="voice-options">
              <button 
                className="voice-button earnings-call" 
                onClick={() => generateVoiceContent('earnings_call')}
                disabled={isLoading}
              >
                📞 Earnings Call
              </button>
              <button 
                className="voice-button briefing" 
                onClick={() => generateVoiceContent('audio_briefing')}
                disabled={isLoading}
              >
                🎧 SMAP Briefing
              </button>
              <button 
                className="voice-button quiz" 
                onClick={() => generateVoiceContent('interactive_quiz')}
                disabled={isLoading}
              >
                🧠 Interactive Quiz
              </button>
            </div>
            
            {voiceContent && voiceContent.audio_available && (
              <div className="audio-player">
                <h4>🎧 {voiceContent.title}</h4>
                <audio controls className="audio-controls">
                  <source src={voiceContent.audio_url} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
                <p className="audio-info">
                  Duration: {voiceContent.duration} • Generated with ElevenLabs API
                </p>
              </div>
            )}
          </div>
        )}

        {voiceContent && (
          <div className="voice-results">
            <h3>🎤 {voiceContent.title}</h3>
            <p><strong>Duration:</strong> {voiceContent.duration}</p>
            
            {currentVoiceType === 'earnings_call' && (
              <div className="earnings-call-content">
                <h4>🎭 Participants</h4>
                <div className="participants">
                  {Object.entries(voiceContent.participants).map(([role, name]) => (
                    <div key={role} className="participant">
                      <strong>{role.replace('_', ' ').toUpperCase()}:</strong> {name}
                    </div>
                  ))}
                </div>
                
                <h4>📝 Script Preview</h4>
                <div className="script-preview">
                  {Object.entries(voiceContent.script).map(([section, text]) => (
                    <div key={section} className="script-section">
                      <strong>{section.replace('_', ' ').toUpperCase()}:</strong>
                      <p>{text}</p>
                    </div>
                  ))}
                </div>
                
                <h4>❓ Learning Questions</h4>
                <ul className="learning-questions">
                  {voiceContent.learning_questions.map((question, index) => (
                    <li key={index}>{question}</li>
                  ))}
                </ul>
              </div>
            )}

            {currentVoiceType === 'audio_briefing' && (
              <div className="briefing-content">
                <h4>📋 Executive Summary</h4>
                <div className="summary">
                  <p>{voiceContent.summary}</p>
                </div>
                
                <h4>⭐ Key Highlights</h4>
                <ul className="highlights">
                  {voiceContent.highlights.map((highlight, index) => (
                    <li key={index}>{highlight}</li>
                  ))}
                </ul>
                
                <h4>📊 SMAP Breakdown</h4>
                <div className="smap-breakdown">
                  {Object.entries(voiceContent.smap_breakdown).map(([section, content]) => (
                    <div key={section} className="breakdown-section">
                      <strong>{section.toUpperCase()}:</strong>
                      <p>{content}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {currentVoiceType === 'interactive_quiz' && (
              <div className="quiz-content">
                <h4>❓ Quiz Questions</h4>
                {voiceContent.questions.map((question, index) => (
                  <div key={index} className="quiz-question">
                    <p><strong>Question {index + 1}:</strong> {question.question}</p>
                    <div className="options">
                      {question.options.map((option, i) => (
                        <div key={i} className={`option ${i === question.correct ? 'correct' : ''}`}>
                          {String.fromCharCode(65 + i)}) {option}
                        </div>
                      ))}
                    </div>
                    <p className="explanation"><em>{question.explanation}</em></p>
                  </div>
                ))}
                
                <div className="final-feedback">
                  <h4>🎯 Final Score Explanation</h4>
                  <p>{voiceContent.final_score_explanation}</p>
                </div>
              </div>
            )}

            <div className="audio-note">
              <p><em>🎧 In production, this would generate realistic audio using ElevenLabs API</em></p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App