import { useState, useEffect, useRef } from "react";
// 
// Using dynamic import to load Supabase from CDN to resolve build error.
// We declare the state variable, 'supabase', later after import.
// 
let supabase = null; 

<<<<<<< HEAD
// Separate component for the main landing page content
function LandingPage({ onLoginClick, onSignupClick }) {
  const fileInputRef = useRef(null);
  
  // SEC Search states
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState('cik'); // 'name' or 'cik'
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

=======
// --- Inline CSS for Styling (Consolidated from index.css) ---
const globalStyles = `
/* Global Reset and Setup */
:root {
    font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    font-weight: 400;
    color: #213547;
    background-color: #ffffff;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body {
    margin: 0;
    padding: 0;
}

/* Base Elements */
h1 {
    font-size: 3.2em;
    line-height: 1.1;
}

button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.25s, border-color 0.25s;
}

input {
    width: 100%;
    padding: 0.8rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 1rem;
    outline: none;
    transition: border 0.2s;
}

input:focus {
    border-color: #6d5dfc;
}

/* Authentication Container Styling */

.container,
.gradient-bg {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    width: 100%;
    margin: 0;
    padding: 0;
}

.gradient-bg {
    background: linear-gradient(135deg, #6d5dfc, #c76ff0);
}

.auth-view .card {
    background: white;
    color: #333;
    padding: 2.5rem 2rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    width: 100%;
    max-width: 380px;
    text-align: center;
}

.title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: #4a3aff;
}

.primary-btn {
    width: 100%;
    background: #6d5dfc;
    color: white;
    border: none;
    padding: 0.9rem;
    border-radius: 8px;
    font-weight: 600;
    margin-top: 0.5rem;
}

.primary-btn:hover {
    background: #5848e5;
}

.link-btn {
    background: none;
    border: none;
    color: #6d5dfc;
    cursor: pointer;
    font-weight: 600;
    font-size: 1rem;
    padding: 0;
}

.link-btn:hover {
    color: #4a3aff;
    text-decoration: underline;
}

.toggle-text {
    margin-top: 1.2rem;
    color: #555;
    font-size: 0.95rem;
}

.logged-in-container {
    background-color: #f7f7f7;
}

.logged-in {
    background: white;
    color: #333;
    padding: 2.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logout-btn {
    background: #ff4c4c;
    color: white;
    border: none;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    margin-top: 1.5rem;
    width: auto;
}

.logout-btn:hover {
    background: #e13d3d;
}

/* --- Landing Page Styling --- */

.landing-page {
    min-height: 100vh;
    padding: 0;
    background-color: white;
    color: #213547;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5rem;
    max-width: 1280px;
    margin: 0 auto;
}

.logo-placeholder {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4a3aff;
}

.auth-buttons button {
    padding: 0.6em 1.5em;
    margin-left: 0.75rem;
    width: auto;
}

.login-btn {
    background-color: #4a3aff;
    color: white;
    width: auto;
}

.secondary-btn {
    background-color: transparent;
    color: #4a3aff;
    border: 1px solid #4a3aff;
    font-weight: 600;
    width: auto;
}

.secondary-btn:hover {
    background-color: #f0f0ff;
    border-color: #5848e5;
    color: #5848e5;
}

.hero-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1100px;
    margin: 0 auto;
    padding: 5rem 5rem 10rem 5rem;
}

.hero-left {
    flex: 1;
    max-width: 50%;
    text-align: left;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.highlight-text {
    color: #4a3aff;
}

.subtitle-text {
    font-size: 1.15rem;
    color: #555;
    margin-top: 1rem;
    margin-bottom: 2rem;
    line-height: 1.5;
}

.search-box {
    display: flex;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 0.25rem;
    width: 100%;
    max-width: 450px;
    background-color: white;
}

.search-box input {
    flex-grow: 1;
    border: none;
    padding: 0.8rem;
    margin: 0;
    font-size: 1rem;
}

.search-box input:focus {
    border-color: transparent;
    box-shadow: none;
}

.search-btn {
    background-color: #4a3aff;
    color: white;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    border: none;
    width: auto;
    margin: 0.25rem;
}

.hero-right {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    max-width: 50%;
    padding-left: 2rem;
}

.upload-card {
    background: white;
    padding: 2.5rem 2.5rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 350px;
    text-align: center;
    border: 1px solid #eee;
}

.file-icon {
    margin-bottom: 1rem;
}

.upload-prompt {
    font-size: 1rem;
    color: #555;
    margin-bottom: 1.5rem;
    line-height: 1.4;
}

.upload-btn {
    background: #4a3aff;
    color: white;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.8rem;
    margin-top: 0;
}

.upload-icon {
    margin-left: 0.5rem;
}

/* Hide the actual file input */
.hidden-file-input {
    display: none;
}

/* --- Summary Screen Styling --- */

.summary-page {
    min-height: 100vh;
    background-color: white;
}

.summary-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0 1rem;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    z-index: 10;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.summary-header .auth-buttons {
    padding: 0.5rem 5rem;
}

.summary-container {
    display: flex;
    min-height: 100vh;
    max-width: 1280px;
    margin: 0 auto;
    padding-top: 5.5rem; /* Space for fixed header */
    background-color: white;
}

.sidebar {
    width: 250px;
    flex-shrink: 0;
    padding: 2rem 0;
    border-right: 1px solid #eee;
    background-color: #f9f9f9;
}

.sidebar h3 {
    padding: 0 2rem;
    font-size: 1rem;
    color: #888;
    margin-bottom: 0.5rem;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 2rem;
    cursor: pointer;
    font-weight: 500;
    color: #555;
    transition: background-color 0.2s;
}

.nav-item-active {
    background-color: #eef2ff; /* Light blue background for active */
    color: #4a3aff;
    font-weight: 600;
    border-right: 3px solid #4a3aff;
}

.nav-item svg {
    margin-right: 0.75rem;
}

.content-area {
    flex-grow: 1;
    padding: 2rem 5rem;
    overflow-y: auto;
}

.content-area .company-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.content-area .company-subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 2rem;
    line-height: 1.4;
}

.content-area h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #4a3aff;
    margin-top: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #eee;
}

.content-area p {
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.save-btn {
    background: white;
    color: #4a3aff;
    border: 1px solid #4a3aff;
    padding: 0.5rem 1rem;
    font-weight: 600;
    float: right;
    margin-top: -3rem;
    transition: background 0.2s;
}

.save-btn:hover {
    background: #f0f0ff;
}

.practice-btn {
    background: #4a3aff;
    color: white;
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    border-radius: 20px;
    margin-top: 2rem;
    display: inline-flex;
    align-items: center;
    width: auto;
}
.practice-btn svg {
    margin-left: 0.5rem;
}

/* --- Practice Mode Specific Styles --- */
.practice-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.practice-subtitle {
    font-size: 1rem;
    color: #555;
    margin-bottom: 2rem;
}

.smaps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.smaps-item {
    padding: 1rem;
    border: 1px solid #eee;
    border-radius: 8px;
    background: #fcfcfc;
}

.smaps-item h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    padding: 0;
    border: none;
}

.smaps-item textarea {
    width: 100%;
    min-height: 100px;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    resize: vertical;
    font-size: 0.95rem;
    color: #444;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.quiz-section h2 {
    color: #333;
    font-weight: 700;
    border: none;
    padding: 0;
}

.quiz-question {
    margin-bottom: 2rem;
    border-top: 1px solid #eee;
    padding-top: 1.5rem;
}

.quiz-question p {
    font-weight: 600;
    margin-bottom: 1rem;
}

.quiz-option-label {
    display: block;
    cursor: pointer;
    padding: 0.5rem 0;
    font-weight: 400;
    font-size: 1rem;
}

/* Custom Radio Button Styling */
.quiz-option-label input[type="radio"],
.quiz-option-label input[type="checkbox"] {
    width: auto;
    margin-right: 0.5rem;
    /* Hide default radio/checkbox */
    appearance: none;
    -webkit-appearance: none;
    border: none;
    display: inline-block;
    vertical-align: middle;
    width: 18px;
    height: 18px;
    min-width: 18px;
    min-height: 18px;
    border: 2px solid #ccc;
    border-radius: 50%; /* Radio style */
    position: relative;
    cursor: pointer;
    top: -1px;
}

.quiz-option-label input[type="checkbox"] {
    border-radius: 4px; /* Checkbox style */
}

.quiz-option-label input[type="radio"]:checked,
.quiz-option-label input[type="checkbox"]:checked {
    border-color: #4a3aff;
    background-color: #4a3aff;
}

.quiz-option-label input[type="radio"]:checked:after {
    content: '';
    display: block;
    width: 8px;
    height: 8px;
    background: white;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.submit-container {
    text-align: center;
    margin: 4rem 0 6rem 0;
}

.submit-btn {
    background: #4a3aff;
    color: white;
    padding: 0.8rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 20px;
    width: auto;
}

/* --- Voice Agent Specific Styles --- */
.voice-agent-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 0;
    text-align: center;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.voice-ai-circle {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    background: linear-gradient(135deg, #eef2ff, #f9f9ff);
    box-shadow: 0 8px 30px rgba(74, 58, 255, 0.15);
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.voice-ai-circle-pattern {
    /* Abstract pattern using SVG or CSS for the look in the image */
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 100 100'%3E%3Cpath fill='%234A3AFF' fill-opacity='0.1' d='M45.1 63.8L50 50l4.9 13.8L45.1 63.8z'/%3E%3Cpath fill='%236D5DFC' fill-opacity='0.2' d='M68.8 35.1L50 50l18.8 14.9L68.8 35.1z'/%3E%3Cpath fill='%23C76FF0' fill-opacity='0.15' d='M31.2 35.1L50 50L31.2 64.9L31.2 35.1z'/%3E%3Cpath fill='%234A3AFF' fill-opacity='0.25' d='M50 36.2L45.1 50L54.9 36.2L50 36.2z'/%3E%3C/svg%3E");
    background-size: 100px 100px;
    width: 100%;
    height: 100%;
    opacity: 0.8;
}

.voice-action-buttons {
    position: absolute;
    bottom: 20px;
    display: flex;
    gap: 20px;
}

.mic-btn, .cancel-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.1s;
}

.mic-btn {
    background-color: #4a3aff;
}

.mic-btn:hover {
    background-color: #5848e5;
    transform: scale(1.05);
}

.cancel-btn {
    background-color: #f0f0f0;
    color: #999;
}

.cancel-btn:hover {
    background-color: #e0e0e0;
    transform: scale(1.05);
}

.suggestions {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
    text-align: left;
}

.suggestions p {
    font-size: 0.95rem;
    color: #777;
    margin: 0.5rem 0;
    padding-left: 1rem;
    list-style: disc;
    position: relative;
    cursor: pointer;
}

.suggestions p::before {
    content: '•';
    color: #4a3aff;
    font-weight: bold;
    display: inline-block;
    width: 1em;
    margin-left: -1em;
}


/* Responsive adjustments */
@media (max-width: 1024px) {
    .summary-container {
        flex-direction: column;
        padding-top: 4rem;
    }
    
    .sidebar {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid #eee;
        padding: 1rem 0;
        padding-top: 0;
    }
    
    .content-area {
        padding: 2rem 1.5rem;
    }
    
    .summary-header .auth-buttons {
        padding: 0.5rem 1.5rem;
    }
    
    .smaps-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}
@media (max-width: 600px) {
    .summary-header .logo-placeholder {
        padding-left: 1rem;
    }
}
`;
// -----------------------------------------------------

// --- Voice Agent Component (New) ---

function VoiceAgentScreen() {
    const handleMicClick = () => {
        alert("Microphone listening... (Feature is mock)");
    };

    const handleCancelClick = () => {
        alert("Voice session cancelled.");
    };

    return (
        <div className="voice-agent-mode">
            <h1 className="practice-header">Voice Agent</h1>
            <p className="practice-subtitle">
                Ask our AI anything about the company's 10-Q, from definitions to deeper financial insights.
                Learn through conversation and get clear, plain-English explanations.
            </p>
            
            <div className="voice-agent-container">
                <div className="voice-ai-circle">
                    <div className="voice-ai-circle-pattern"></div>
                    
                    <div className="voice-action-buttons">
                        {/* Microphone Button */}
                        <button className="mic-btn" onClick={handleMicClick}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
                        </button>
                        {/* Cancel Button */}
                        <button className="cancel-btn" onClick={handleCancelClick}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>
                </div>

                <div className="suggestions">
                    <p style={{fontWeight: 700, color: '#4a3aff', marginBottom: '0.8rem'}}>Try asking:</p>
                    <p onClick={() => console.log('Try asking: What does net income mean?')}>What does net income mean?</p>
                    <p onClick={() => console.log('Try asking: Why did revenue drop this quarter?')}>Why did revenue drop this quarter?</p>
                    <p onClick={() => console.log('Try asking: Explain this company\'s debt ratio.')}>Explain this company's debt ratio.</p>
                </div>
            </div>
        </div>
    );
}

// --- Practice Mode Component ---

function PracticeScreen() {
    // State for SMAP notes (Summarize, Metrics, Assess, Plan)
    const [smapNotes, setSmapNotes] = useState({
        summary: '',
        metric: '',
        assessment: '',
        plan: ''
    });

    const [quizAnswers, setQuizAnswers] = useState({
        q1: null,
        q2: null
    });

    const handleSmapChange = (e) => {
        const { name, value } = e.target;
        setSmapNotes(prev => ({ ...prev, [name]: value }));
    };

    const handleQuizChange = (e) => {
        const { name, value, type, checked } = e.target;
        
        if (type === 'radio') {
            setQuizAnswers(prev => ({ ...prev, [name]: value }));
        } else if (type === 'checkbox') {
            // Placeholder for multi-select, but quiz is currently radio/true-false
            setQuizAnswers(prev => {
                const newAnswers = prev[name] || [];
                if (checked) {
                    return { ...prev, [name]: [...newAnswers, value] };
                } else {
                    return { ...prev, [name]: newAnswers.filter(v => v !== value) };
                }
            });
        }
    };

    const handleSubmit = () => {
        console.log("SMAP Notes:", smapNotes);
        console.log("Quiz Answers:", quizAnswers);
        // In a real application, this is where you would call the AI feedback API.
        console.log("Submitted for grading and feedback!");
        alert("SMAP notes and quiz submitted! Check the console for data.");
    };

    return (
        <div className="practice-mode">
            <h1 className="practice-header">Practice mode</h1>
            <p className="practice-subtitle">
                Fill in your own SMAP notes, identify key metrics, risks, and next steps,
                and get instant AI feedback to see what you got right and what you missed.
            </p>

            {/* SMAP NOTES SECTION */}
            <h2 style={{color: '#333'}}>SMAP Notes</h2>
            <div className="smaps-grid">
                {/* Summary */}
                <div className="smaps-item">
                    <h3>Summary</h3>
                    <textarea
                        name="summary"
                        value={smapNotes.summary}
                        onChange={handleSmapChange}
                        placeholder="Summarize the main points in a few sentences"
                    />
                </div>
                {/* Metric */}
                <div className="smaps-item">
                    <h3>Metric</h3>
                    <textarea
                        name="metric"
                        value={smapNotes.metric}
                        onChange={handleSmapChange}
                        placeholder="Highlight the metrics that matter most — revenue, EPS, margins, cash flow."
                    />
                </div>
                {/* Assessment */}
                <div className="smaps-item">
                    <h3>Assessment</h3>
                    <textarea
                        name="assessment"
                        value={smapNotes.assessment}
                        onChange={handleSmapChange}
                        placeholder="Explain what these numbers imply about the company's health"
                    />
                </div>
                {/* Plan */}
                <div className="smaps-item">
                    <h3>Plan</h3>
                    <textarea
                        name="plan"
                        value={smapNotes.plan}
                        onChange={handleSmapChange}
                        placeholder="What would you recommend next based on this info?"
                    />
                </div>
            </div>

            {/* QUIZ SECTION */}
            <div className="quiz-section">
                <h2>Quiz</h2>

                {/* Question 1: Multiple Choice */}
                <div className="quiz-question">
                    <p>Question 1</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor **incididunt** ut labore et dolore magna aliqua?</p>
                    
                    <label className="quiz-option-label">
                        <input type="radio" name="q1" value="dolor" checked={quizAnswers.q1 === 'dolor'} onChange={handleQuizChange} /> dolor
                    </label>
                    <label className="quiz-option-label">
                        <input type="radio" name="q1" value="lorem_ipsum" checked={quizAnswers.q1 === 'lorem_ipsum'} onChange={handleQuizChange} /> Lorem ipsum
                    </label>
                    <label className="quiz-option-label">
                        <input type="radio" name="q1" value="aliqua" checked={quizAnswers.q1 === 'aliqua'} onChange={handleQuizChange} /> aliqua
                    </label>
                    <label className="quiz-option-label">
                        <input type="radio" name="q1" value="consectetur" checked={quizAnswers.q1 === 'consectetur'} onChange={handleQuizChange} /> consectetur
                    </label>
                </div>

                {/* Question 2: True/False */}
                <div className="quiz-question">
                    <p>Question 2</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor **incididunt** ut labore et dolore magna aliqua?</p>
                    
                    <label className="quiz-option-label">
                        <input type="radio" name="q2" value="true" checked={quizAnswers.q2 === 'true'} onChange={handleQuizChange} /> True
                    </label>
                    <label className="quiz-option-label">
                        <input type="radio" name="q2" value="false" checked={quizAnswers.q2 === 'false'} onChange={handleQuizChange} /> False
                    </label>
                </div>
            </div>
            
            <div className="submit-container">
                <p style={{marginBottom: '1rem', color: '#4a3aff', fontWeight: '600'}}>
                    Ready to submit and get feedback?
                </p>
                <button className="submit-btn" onClick={handleSubmit}>
                    Submit
                </button>
            </div>
        </div>
    );
}

// --- Summary Screen Component (updated to include navigation logic) ---

function SummaryScreen({ companyName, onLogout, onLoginClick, onSignupClick }) {
    // State to manage which content view is active: 'summary', 'practice', or 'agent'
    const [activeNav, setActiveNav] = useState('summary');
    
    const PLACHOLDER_TEXT = `
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
        aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    `;

    // Mock content for the Summary tab
    const summaryContent = {
        title: `${companyName}`,
        subtitle: `A simplified summary of ${companyName}'s 10-Q, highlighting key metrics, trends, and insights.`,
        keyMetrics: PLACHOLDER_TEXT,
        topInsights: PLACHOLDER_TEXT,
        trendHighlights: PLACHOLDER_TEXT,
    };
    
    // Function to render the active content tab
    const renderContent = () => {
        switch (activeNav) {
            case 'summary':
                return (
                    <>
                        <button className="save-btn" onClick={() => console.log('Save analysis clicked')}>
                            Save analysis
                        </button>
                        
                        <h1 className="company-title">{summaryContent.title}</h1>
                        <p className="company-subtitle">{summaryContent.subtitle}</p>
    
                        <h2>Key metrics at a glance</h2>
                        <p>{summaryContent.keyMetrics}</p>
    
                        <h2>Top insights</h2>
                        <p>{summaryContent.topInsights}</p>
    
                        <h2>Trend Highlights</h2>
                        <p>{summaryContent.trendHighlights}</p>
    
                        <div style={{textAlign: 'center', margin: '3rem 0'}}>
                            <p style={{marginBottom: '1rem', color: '#4a3aff'}}>
                                Try to identify important trends and definitions before moving to Practice Mode.
                            </p>
                            <button className="practice-btn" onClick={() => setActiveNav('practice')}>
                                Practice Mode
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="M12 5l7 7-7 7"></path></svg>
                            </button>
                        </div>
                    </>
                );
            case 'practice':
                return <PracticeScreen />;
                
            case 'agent':
                return <VoiceAgentScreen />;
            default:
                return null;
        }
    };

    return (
        <div className="summary-page">
            <header className="summary-header">
                <div className="logo-placeholder">Q Notes</div>
                <div className="auth-buttons">
                    <button className="primary-btn login-btn" onClick={onLoginClick}>
                        Login
                    </button>
                    <button className="secondary-btn signup-btn" onClick={onSignupClick}>
                        Sign Up
                    </button>
                    <button className="secondary-btn logout-btn" onClick={onLogout}>
                        Logout (Mock)
                    </button>
                </div>
            </header>
            
            <div className="summary-container">
                <aside className="sidebar">
                    <h3>Roadmap</h3>
                    {/* Summary Nav */}
                    <div 
                        className={activeNav === 'summary' ? "nav-item nav-item-active" : "nav-item"}
                        onClick={() => setActiveNav('summary')}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        Summary
                    </div>
                    {/* Practice Nav */}
                    <div 
                        className={activeNav === 'practice' ? "nav-item nav-item-active" : "nav-item"}
                        onClick={() => setActiveNav('practice')}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg>
                        Practice
                    </div>
                    {/* Voice Agent Nav */}
                    <div 
                        className={activeNav === 'agent' ? "nav-item nav-item-active" : "nav-item"}
                        onClick={() => setActiveNav('agent')}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                        Voice Agent
                    </div>
                </aside>
                
                <div className="content-area">
                    {renderContent()}
                </div>
            </div>
        </div>
    );
}


// --- Landing Page Component ---

function LandingPage({ onLoginClick, onSignupClick, onSearch }) { 
  const [searchQuery, setSearchQuery] = useState("");
  const fileInputRef = useRef(null); 

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearch(searchQuery.trim()); 
    }
  };

>>>>>>> cd81d8f (Added more screens)
  const handleUploadButtonClick = () => {
    if (fileInputRef.current) {
        fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Selected file:", file.name);
      console.log(`File selected: ${file.name}. Ready for analysis! (Feature is mock for now)`);
      const companyName = file.name.replace(/\.(txt|pdf|doc|docx)$/i, '');
      onSearch(companyName); 
      e.target.value = null; 
    }
  };

  const searchCompany = async () => {
    if (!searchTerm.trim()) {
      setError('Please enter a company name, ticker, or CIK');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);
    setSearched(true);

    try {
      // If searching by CIK, directly create the result
      if (searchType === 'cik') {
        const cikNumber = searchTerm.replace(/\D/g, ''); // Remove non-digits
        
        if (!cikNumber) {
          setError('Please enter a valid CIK number');
          setLoading(false);
          return;
        }

        const cikPadded = cikNumber.padStart(10, '0');
        
        // Fetch company info to verify CIK exists
        try {
          const response = await fetch(
            `https://data.sec.gov/submissions/CIK${cikPadded}.json`,
            {
              headers: {
                'User-Agent': 'Company Search Tool'
              }
            }
          );

          if (!response.ok) {
            throw new Error('CIK not found');
          }

          const companyInfo = await response.json();
          
          setResults([{
            title: companyInfo.name,
            ticker: companyInfo.tickers?.[0] || 'N/A',
            cik_str: parseInt(cikNumber),
            cik_padded: cikPadded,
            edgarUrl: `https://www.sec.gov/edgar/browse/?CIK=${cikPadded}&owner=exclude`
          }]);
        } catch (err) {
          setError('CIK number not found in SEC database');
        }
        
        setLoading(false);
        return;
      }

      // Search by name/ticker
      const response = await fetch(
        'https://www.sec.gov/files/company_tickers.json',
        {
          headers: {
            'User-Agent': 'Company Search Tool'
          }
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch company data');
      }

      const data = await response.json();
      
      // Convert to array and search
      const companies = Object.values(data);
      const searchLower = searchTerm.toLowerCase();
      
      const matches = companies.filter(company => 
        company.title.toLowerCase().includes(searchLower) ||
        company.ticker?.toLowerCase().includes(searchLower)
      );

      if (matches.length === 0) {
        setError('No companies found matching your search');
      } else {
        // Add padded CIK to results
        const formattedResults = matches.map(company => ({
          ...company,
          cik_padded: String(company.cik_str).padStart(10, '0'),
          edgarUrl: `https://www.sec.gov/edgar/browse/?CIK=${String(company.cik_str).padStart(10, '0')}&owner=exclude`
        }));
        setResults(formattedResults);
      }
    } catch (err) {
      setError('Error fetching data from SEC. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchCompany();
    }
  };

  return (
    <div className="landing-page">
      <header className="header">
        <div className="logo-placeholder">Q Notes</div>
        <div className="auth-buttons">
          <button className="primary-btn login-btn" onClick={onLoginClick}>
            Login
          </button>
          <button className="secondary-btn signup-btn" onClick={onSignupClick}>
            Sign Up
          </button>
        </div>
      </header>

      <main className="hero-section">
        {/* Left Column: Text and Search */}
        <div className="hero-left">
          <h1 className="main-title">
            Learn Finance Through <span className="highlight-text">Real Reports</span>
          </h1>
          <p className="subtitle-text">
            Search for a company or upload a 10-Q file, and we'll turn it into simple
            summaries, charts, and explanations you can understand with definitions
            for any financial terms you don't know.
          </p>
          <div className="p-6 max-w-3xl mx-auto">

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            searchType === 'name'
              ? 'Enter company name or ticker'
              : 'Enter CIK number'
          }
          className="flex-1 px-3 py-2 border border-gray-300 rounded"
        />
        <button
          onClick={searchCompany}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-300 rounded text-red-700">
          {error}
        </div>
      )}

      {searched && !loading && results.length > 0 && (
        <div>
          <p className="mb-3 font-semibold">
            Found {results.length} {results.length === 1 ? 'company' : 'companies'}
          </p>
          
          {results.map((company, idx) => (
            <div key={idx} className="mb-3 p-4 border border-gray-300 rounded">
              <div className="mb-2">
                <div className="font-bold">{company.title}</div>
                <div className="text-sm text-gray-600">
                  Ticker: {company.ticker || 'N/A'} | CIK: {company.cik_padded}
                </div>
              </div>
              
              <a
                href={company.edgarUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                View SEC Filings →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
        </div>

        

        {/* Right Column: Upload Card */}
        <div className="hero-right">
          <div className="upload-card">
            {/* File Icon */}
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#6d5dfc" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="file-icon">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <p className="upload-prompt">
              Upload your 10Q file here for
              <br />
              us to analyze and simplify it
              <br />
              for you!
            </p>
            {/* The actual hidden file input */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden-file-input"
                accept=".txt,.pdf,.doc,.docx" // Accept only common document types
            />
            {/* The visible button to trigger the hidden input */}
            <button 
                className="primary-btn upload-btn" 
                onClick={handleUploadButtonClick}
            >
              Upload File
              {/* Upload Icon */}
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="upload-icon">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

// Separate component for the Authentication (Login/Signup) Modal/View
function AuthView({ onLogin, onSignup, onToggleAuth, showSignup }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = showSignup ? onSignup : onLogin;
    
    return (
        <div className="container auth-view">
            <div className="card">
                <h1 className="title">Q Notes</h1>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit(email, password);
                }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit" className="primary-btn">
                        {showSignup ? "Sign Up" : "Login"}
                    </button>
                </form>
                <p className="toggle-text">
                    {showSignup ? "Already have an account?" : "Don't have an account?"}{" "}
                    <button
                        type="button"
                        className="link-btn"
                        onClick={onToggleAuth}
                    >
                        {showSignup ? "Login" : "Sign Up"}
                    </button>
                </p>
            </div>
        </div>
    );
}

// Main App Component
function App() {
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState(null); 
  const [summaryData, setSummaryData] = useState(null); 
  const [isSupabaseReady, setIsSupabaseReady] = useState(false); 

  // Load Supabase dynamically on component mount
  useEffect(() => {
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"; 
    script.onload = () => {
        const { createClient } = window.supabase;
        const SUPABASE_URL = "https://rpwvpanvccswvhddxpdj.supabase.co";
        const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwd3ZwYW52Y2Nzd3ZoZGR4cGRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1OTgyMTIsImV4cCI6MjA3NTE3NDIxMn0.lB08q1ctotUf6SZoLEL4ImtY9wHNFUpuWUiVyl6z52U";

        supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        setIsSupabaseReady(true);
    };
    document.head.appendChild(script);

    return () => {
        if (script.parentNode) {
            script.parentNode.removeChild(script);
        }
    };
  }, []);

  // Effect to handle authentication state changes, dependent on Supabase being ready
  useEffect(() => {
    if (!isSupabaseReady) return; 

    supabase.auth.getSession().then(({ data }) => {
      if (data.session) setUser(data.session.user);
    });

    const { data: subscription } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription?.subscription?.unsubscribe();
  }, [isSupabaseReady]); 

  // Centralized function to handle both login and signup
  const handleAuth = async (isSignup, currentEmail, currentPassword) => {
    if (!isSupabaseReady) {
      console.log("Supabase not ready yet. Please wait.");
      return;
    }
    
    const method = isSignup 
        ? supabase.auth.signUp 
        : supabase.auth.signInWithPassword;

    const { data, error } = await method({
        email: currentEmail,
        password: currentPassword,
    });

    if (error) {
        console.error("Authentication error:", error.message);
        console.log(`Error: ${error.message}`); 
    } else if (isSignup) {
        console.log("Signup successful! Check your email for confirmation.");
        setAuthMode(null);
    } else {
        setUser(data.user);
        setAuthMode(null);
    }
  };
  
  const handleLogout = async () => {
    if (!isSupabaseReady) return;

    await supabase.auth.signOut();
    setUser(null);
    setSummaryData(null); 
  };
  
  const handleSearchAndTransition = (companyName) => {
    console.log(`Transitioning to summary for: ${companyName}`);
    setSummaryData({ companyName: companyName.toUpperCase() });
  };
  
  // RENDER LOGIC: Check state to decide which view to show
  
  if (!isSupabaseReady) {
    return (
        <div className="container" style={{backgroundColor: '#f7f7f7'}}>
            <style>{globalStyles}</style>
            <h1 className="title" style={{color: '#4a3aff'}}>Loading Application...</h1>
        </div>
    );
  }

  // 1. Logged-in view (only shows simple card)
  if (user && !summaryData) {
    return (
      <div className="container logged-in-container">
        <style>{globalStyles}</style>
        <div className="card logged-in">
          <h1>Welcome, {user.email}</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    );
  }
  
  // 2. Summary/Results View (triggered by search/upload, overrides Auth/Landing)
  if (summaryData) {
    return (
      <>
        <style>{globalStyles}</style>
        <SummaryScreen 
            companyName={summaryData.companyName}
            onLogout={handleLogout}
            onLoginClick={() => setAuthMode('login')}
            onSignupClick={() => setAuthMode('signup')}
        />
      </>
    );
  }

  // 3. Login/Signup Modal/View (triggered by header buttons)
  if (authMode) {
    return (
        <div className="gradient-bg">
            <style>{globalStyles}</style>
            <AuthView 
                onLogin={(email, password) => handleAuth(false, email, password)}
                onSignup={(email, password) => handleAuth(true, email, password)}
                onToggleAuth={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}
                showSignup={authMode === 'signup'}
            />
        </div>
    )
  }

  // 4. Default: Landing Page View
  return (
    <>
      <style>{globalStyles}</style>
      <LandingPage
          onLoginClick={() => setAuthMode('login')}
          onSignupClick={() => setAuthMode('signup')}
          onSearch={handleSearchAndTransition} 
      />
    </>
  );
}

export default App;
