# QNotes - 10Q Notes AI

**HackRU 2025 Project - Democratizing Finance Education with AI**

AI-powered SEC filing learning platform that transforms complex financial documents into structured SMAP (Subjective, Metrics, Assessment, Plan) notes for educational purposes.

## 🎯 Project Overview

QNotes makes SEC filings (10-Q/10-K reports) accessible to students through interactive AI-powered learning experiences. Students can upload financial documents and learn through three progressive modes:

1. **📖 Learn Mode** - Read with AI explanations and hover definitions
2. **✍️ Practice Mode** - Write their own analysis
3. **🎯 AI Feedback Mode** - Get scored feedback compared to AI Gold Standard

## 🏗️ Project Structure

```
QNotes/
├── Backend/           # Python FastAPI backend with all AI services
│   ├── backend_app.py         # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── start_backend.py       # Easy startup script
│   ├── test_backend_api.py    # Complete API test suite
│   ├── README_BACKEND.md      # Backend documentation
│   ├── education_service.py   # Core learning experience
│   ├── voice_agent_service.py # ElevenLabs voice integration
│   ├── gemini_service.py      # Google AI analysis
│   └── document_processor.py  # SEC filing processing
│
├── Frontend/          # React frontend (existing)
│   ├── src/
│   ├── package.json
│   └── ...
│
└── README.md         # This file
```

## 🚀 Quick Start

### Backend (Python AI Services)
```bash
cd Backend/
pip install -r requirements.txt
python start_backend.py
```

### Frontend (React UI)
```bash
cd Frontend/
npm install
npm start
```

## 🎓 Three Learning Modes

### 1. Learn Mode (Read & Hover)
- **Features**: 
  - Students see extracted sections with simplified explanations
  - Hover over jargon/ratios → plain-English definitions
  - Optional ElevenLabs voice synthesis reads sections aloud
  - Interactive AI guidance throughout

### 2. Practice Mode (Student Writes SMAP)
- **Features**:
  - Students fill in their own Subjective, Metrics, Assessment, Plan boxes
  - Try to identify key narrative points, ratios, risks, and next steps
  - Guided templates with word count targets
  - Real-time draft saving and progress tracking

### 3. AI Feedback Mode
- **Features**:
  - Gemini compares student's notes to AI Gold Standard
  - Detailed feedback generation:
    - ✅ What they got right
    - ⚠️ What they missed (e.g., "You missed Gross Margin trend")
    - 💡 Suggestions ("Connect debt level to refinancing risk")
    - Score out of 100 for Clarity, Completeness, Accuracy

## 🎤 Voice Agent Integration

**ElevenLabs Integration** for immersive learning:
- **Simulated Earnings Calls**: Realistic management and analyst voices
- **SMAP Audio Briefings**: Professional narration of analysis
- **Section Reading**: Voice synthesis for accessibility

## 🤖 AI Services

### Google Gemini AI
- **SMAP Analysis Generation**: Creates structured financial analysis
- **Educational Feedback**: Compares student work to Gold Standard
- **Content Simplification**: Plain-English explanations

### ElevenLabs Voice
- **Text-to-Speech**: Professional voice synthesis
- **Multi-Voice Support**: Management vs Analyst perspectives
- **Audio Learning**: Accessibility and engagement

## 🏆 HackRU 2025 Features

### MLH Prize Categories
- **✅ Best Use of Google AI**: Gemini-powered SMAP analysis and feedback
- **✅ Best Use of ElevenLabs**: Voice synthesis for earnings calls and briefings
- **✅ Best Education Hack**: Interactive learning platform for finance education

### Demo Flow
1. **Upload SEC Filing** (10-Q/10-K document)
2. **Learn Mode** - AI explains sections with hover definitions
3. **Practice Mode** - Student writes their own SMAP analysis
4. **AI Feedback** - Detailed scoring and improvement suggestions
5. **Voice Features** - Earnings call simulation and audio briefings

## 🔧 Technical Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini AI** - Advanced language model for analysis
- **ElevenLabs** - Professional voice synthesis
- **PyPDF2/pdfplumber** - SEC filing processing
- **SQLAlchemy** - Database management

### Frontend
- **React** - Interactive user interface
- **JavaScript/CSS** - Modern web technologies

## 📊 API Endpoints

### Core Learning Flow
- `POST /api/auth/login` - Student authentication
- `POST /api/upload/filing` - Upload SEC documents
- `GET /api/session/{id}/learn` - Enter Learn Mode
- `GET /api/session/{id}/practice` - Enter Practice Mode
- `POST /api/session/{id}/practice/submit` - Submit SMAP
- `GET /api/session/{id}/feedback` - Get AI feedback

### Voice Features
- `GET /api/session/{id}/earnings-call` - Earnings call simulation
- `GET /api/session/{id}/audio-briefing` - SMAP audio briefing
- `POST /api/session/{id}/voice/synthesize` - Text-to-speech

## 🧪 Testing

Complete test suite covering all three learning modes:
```bash
cd Backend/
python test_backend_api.py
```

Tests include:
- ✅ Student authentication (.edu emails)
- ✅ File upload and processing
- ✅ Learn Mode with hover definitions
- ✅ Practice Mode with SMAP writing
- ✅ AI Feedback with detailed scoring
- ✅ Voice agent features
- ✅ Session management

## 🎯 Educational Impact

**Target Audience**: Finance students, business majors, anyone learning financial analysis

**Learning Outcomes**:
- Understanding SEC filing structure and content
- Ability to extract key financial metrics
- Skills in qualitative business analysis
- Practice with professional financial communication
- Familiarity with earnings calls and investor relations

**Accessibility Features**:
- Plain-English explanations of financial jargon
- Voice synthesis for audio learning
- Interactive hover definitions
- Progressive difficulty levels

## 🚀 Getting Started for Development

1. **Clone Repository**:
```bash
git clone https://github.com/sameenmajid12/QNotes.git
cd QNotes
```

2. **Backend Setup**:
```bash
cd Backend/
pip install -r requirements.txt
# Optional: Add API keys to .env file
echo "GOOGLE_API_KEY=your_key" >> .env
echo "ELEVENLABS_API_KEY=your_key" >> .env
python start_backend.py
```

3. **Frontend Setup**:
```bash
cd Frontend/
npm install
npm start
```

4. **Test Everything**:
```bash
cd Backend/
python test_backend_api.py
```

## 📧 Contact

Built by **azrabano** for HackRU 2025

**Mission**: "Democratizing Finance Education with AI"

---

**🎉 Ready for HackRU judges!** Complete backend implementation with all three learning modes fully functional.