# 10Q Notes AI - Backend API Documentation

**HackRU 2025 Project by azrabano**

AI-powered SEC filing learning platform with SMAP (Subjective, Metrics, Assessment, Plan) framework.

## 🎯 Three Main Learning Features

### 1. **Learn Mode (Read & Hover)**
- Students see extracted sections with simplified explanations
- Hover over jargon/ratios → plain-English definitions (e.g., "Liquidity = cash flexibility")
- Optional voice agent (ElevenLabs) reads sections aloud
- Interactive learning experience with AI guidance

### 2. **Practice Mode (Student Writes SMAP)**
- Students fill in their own S, M, A, P boxes
- Identify key narrative points, ratios, risks, and next steps
- Guided templates with word count targets
- Real-time draft saving and completion tracking

### 3. **AI Feedback Mode**
- Gemini compares student's notes to Gold Standard
- Generates detailed feedback:
  - ✅ What they got right
  - ⚠️ What they missed (e.g., "You missed Gross Margin trend")
  - 💡 Suggestions ("Connect debt level to refinancing risk")
  - Score out of 100 (Clarity, Completeness, Accuracy)

### 4. **Voice Agent (ElevenLabs Integration)**
- Simulated earnings calls with management and analyst voices
- Audio briefings of SMAP notes
- Immersive learning experience

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/azrabano/10q-notes-ai
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Optional)
Create a `.env` file for full functionality:
```bash
GOOGLE_API_KEY=your_gemini_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
```
*Note: The backend works in simulation mode without API keys*

### 3. Start the Backend Server
```bash
python start_backend.py
```
or
```bash
python backend_app.py
```

### 4. Test the API
```bash
python test_backend_api.py
```

The server will start at:
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Authentication & Session Management
- `POST /api/auth/login` - Authenticate student with .edu email
- `GET /api/student/{student_id}/dashboard` - Student progress dashboard
- `GET /api/session/{session_id}/status` - Session status and progress
- `DELETE /api/session/{session_id}` - End learning session

### File Upload & Document Processing
- `POST /api/upload/filing` - Upload SEC filing (PDF/text file)
- `POST /api/upload/text` - Upload filing as raw text

### Learn Mode (Feature #1)
- `GET /api/session/{session_id}/learn` - Enter Learn Mode
- `GET /api/session/{session_id}/learn/section/{section}` - Get section details
- `POST /api/session/{session_id}/voice/synthesize` - Generate voice synthesis

### Practice Mode (Feature #2)
- `GET /api/session/{session_id}/practice` - Enter Practice Mode
- `PUT /api/session/{session_id}/practice/save-draft` - Save work-in-progress
- `POST /api/session/{session_id}/practice/submit` - Submit SMAP for feedback

### AI Feedback Mode (Feature #3)
- `GET /api/session/{session_id}/feedback` - Get AI feedback and scores
- `GET /api/session/{session_id}/gold-standard` - Compare to Gold Standard

### Voice Agent Features
- `GET /api/session/{session_id}/earnings-call` - Earnings call simulation
- `GET /api/session/{session_id}/audio-briefing` - SMAP audio briefing

### Health & Info
- `GET /` - API information
- `GET /health` - Backend health check

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_backend_api.py
```

This tests all three learning modes with a sample JPMorgan 10-Q filing:
1. ✅ Student authentication
2. ✅ File upload and session creation  
3. ✅ Learn Mode with hover definitions
4. ✅ Practice Mode with SMAP writing
5. ✅ AI Feedback with scoring
6. ✅ Voice agent features
7. ✅ Session management
8. ✅ Student dashboard

## 🏗️ Architecture

### Core Services Integration
- **EducationService**: Complete learning experience management
- **VoiceAgentService**: ElevenLabs voice synthesis integration
- **GeminiService**: AI analysis and feedback generation
- **DocumentProcessor**: SEC filing text extraction and processing

### Data Models
- **StudentProfile**: User authentication and progress tracking
- **LearningSession**: Session state and SMAP work management
- **SMAPNotes**: Structured analysis format (Subjective, Metrics, Assessment, Plan)
- **FeedbackScore**: AI-generated scoring and suggestions

### Session Flow
1. **Authentication** → Student logs in with .edu email
2. **Upload** → SEC filing (10Q/10K) uploaded and processed
3. **Learn** → AI-generated sections with explanations
4. **Practice** → Student writes own SMAP analysis  
5. **Feedback** → AI compares to Gold Standard and scores
6. **Voice** → Earnings call simulation and audio briefings

## 🔧 Configuration

### Environment Variables
```bash
# Required for production AI features
GOOGLE_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key

# Optional database (defaults to in-memory for demo)
DATABASE_URL=postgresql://user:pass@localhost/db

# Server settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Development vs Production
- **Development**: Uses in-memory storage, simulation modes
- **Production**: Add database, real API keys, authentication

## 📊 Sample API Usage

### 1. Student Authentication
```python
import requests

response = requests.post("http://localhost:8000/api/auth/login", json={
    "email": "student@rutgers.edu", 
    "name": "John Smith"
})
student_id = response.json()["student"]["student_id"]
```

### 2. Upload SEC Filing
```python
filing_text = "APPLE INC. FORM 10-Q..."

response = requests.post("http://localhost:8000/api/upload/text", data={
    "student_id": student_id,
    "company_name": "Apple Inc.",
    "ticker": "AAPL", 
    "filing_text": filing_text
})
session_id = response.json()["session"]["session_id"]
```

### 3. Learn Mode
```python
response = requests.get(f"http://localhost:8000/api/session/{session_id}/learn")
learn_content = response.json()["content"]
print(f"Sections: {list(learn_content['sections'].keys())}")
```

### 4. Practice Mode
```python
# Enter practice mode
response = requests.get(f"http://localhost:8000/api/session/{session_id}/practice")

# Submit SMAP notes
smap_data = {
    "session_id": session_id,
    "subjective": "Management was confident about Q1 results...",
    "metrics": "Revenue $42.5B (+6.8%), Net income $13.4B...", 
    "assessment": "Strong performance with solid fundamentals...",
    "plan": "Monitor credit trends and digital transformation..."
}
response = requests.post(f"http://localhost:8000/api/session/{session_id}/practice/submit", json=smap_data)
```

### 5. AI Feedback
```python
response = requests.get(f"http://localhost:8000/api/session/{session_id}/feedback")
feedback = response.json()
print(f"Overall Score: {feedback['overall_score']}/100")
print(f"Strengths: {feedback['feedback']['strengths']}")
```

## 🏆 HackRU 2025 Features

### MLH Prize Categories
- **Best Use of Google AI**: Gemini-powered SMAP analysis and feedback
- **Best Use of ElevenLabs**: Voice synthesis for earnings calls and briefings  
- **Best Education Hack**: Interactive learning platform for finance education

### Demo Flow for Judges
1. **Health Check**: `GET /health` - Show all services active
2. **Upload Filing**: Upload sample 10-Q filing
3. **Learn Mode**: Interactive sections with hover definitions
4. **Practice Mode**: Student writes SMAP analysis
5. **AI Feedback**: Detailed scoring and suggestions  
6. **Voice Features**: Earnings call simulation
7. **Dashboard**: Student progress and achievements

## 🔍 Troubleshooting

### Common Issues
1. **"Backend not responding"**: Make sure server is running on port 8000
2. **"Authentication failed"**: Use .edu email addresses only
3. **"Voice synthesis simulation"**: Add ELEVENLABS_API_KEY for real audio
4. **"Gemini errors"**: Add GOOGLE_API_KEY for AI features

### Debug Commands
```bash
# Check server status
curl http://localhost:8000/health

# View API documentation  
open http://localhost:8000/docs

# Run specific test
python -c "from test_backend_api import BackendAPITester; t=BackendAPITester(); t.test_health_check()"
```

## 🎉 Success Metrics

When everything works correctly, you should see:
- ✅ All services active in health check
- ✅ Student authentication with .edu emails
- ✅ File upload and SMAP generation
- ✅ Interactive Learn Mode with hover definitions
- ✅ Practice Mode with draft saving
- ✅ AI feedback with detailed scores
- ✅ Voice agent features (simulation or real)
- ✅ Complete learning flow from upload to feedback

**The backend is ready for HackRU judges when all tests pass!**

---

## 📧 Contact
Built by **azrabano** for HackRU 2025  
**"Democratizing Finance Education with AI"**