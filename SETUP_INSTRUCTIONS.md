# 🚀 10Q Notes AI - Complete Setup Instructions

**HackRU 2025 Project** - SMAP Finance Notes AI

## 📋 Prerequisites

### **Required Software**
- Python 3.8+ 
- Node.js 16+ and npm
- Git

### **API Keys Required**
- Google Gemini API key
- ElevenLabs API key (optional - runs in simulation mode without)
- Snowflake account (optional - runs in simulation mode without)

## 🛠️ Installation Steps

### **1. Clone Repository**
```bash
git clone <repository-url>
cd 10q-notes-ai
```

### **2. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Install Frontend Dependencies**
```bash
cd Frontend
npm install
cd ..
```

### **4. Set Up Environment Variables**
Create a `.env` file in the root directory:
```env
# Required: Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: ElevenLabs (for voice synthesis)
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Optional: Snowflake (for data analytics)
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=HACKRU_10Q_NOTES
SNOWFLAKE_SCHEMA=FINANCIAL_DATA
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

## 🚀 Running the Application

### **Option 1: Complete Application (Recommended)**
```bash
python start_complete_app.py
```
This will:
- Check all requirements
- Show usage instructions
- Let you choose what to run (demo, backend, frontend, or both)

### **Option 2: Run Demo Script**
```bash
python demo_script.py
```
This demonstrates the complete product flow without starting servers.

### **Option 3: Run Integration Tests**
```bash
python test_complete_integration.py
```
This tests all components and generates a report.

### **Option 4: Manual Server Start**

#### **Backend Only:**
```bash
python backend_app.py
```
Backend runs on: http://localhost:8000

#### **Frontend Only:**
```bash
cd Frontend
npm run dev
```
Frontend runs on: http://localhost:3000

#### **Both Servers:**
```bash
# Terminal 1 - Backend
python backend_app.py

# Terminal 2 - Frontend  
cd Frontend
npm run dev
```

## 🎯 Demo Flow

### **1. Access Application**
- Open browser to: http://localhost:3000
- You'll see the upload/login screen

### **2. Student Authentication**
- Use any `.edu` email (e.g., `student@university.edu`)
- Enter your name
- Click "Continue to Dashboard"

### **3. Upload SEC Filing**
- Upload a 10-Q PDF file, OR
- Paste filing text, OR  
- Use the demo data provided

### **4. Explore Learning Modes**

#### **📖 Learn Mode**
- View AI-generated SMAP notes
- Hover over terms for definitions
- Navigate through S, M, A, P sections

#### **✍️ Practice Mode**
- Write your own SMAP notes
- Use guided templates and tips
- Auto-save drafts as you work

#### **🎯 Feedback Mode**
- Submit your work for AI feedback
- View comprehensive scoring
- Read strengths and improvements

#### **🔄 Comparison Mode**
- Compare your work to AI Gold Standard
- See visual highlights of what you got right/missed

### **5. Voice Experience**
- Listen to simulated earnings calls
- Hear management and analyst voices
- Engage with learning activities

## 📊 Sample Data

### **Demo Company: JPMorgan Chase & Co. (JPM)**
- **Filing:** 10-Q Q1 2025
- **Revenue:** $42.5B (+6.8% YoY)
- **Net Income:** $13.4B (+6.1% YoY)
- **ROE:** 17.8%
- **CET1 Ratio:** 15.9%

### **Sample SMAP Output**
```
S – Subjective: Management expressed strong confidence in Q1 performance, highlighting robust revenue growth and disciplined expense management.

M – Metrics: Total revenue of $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%.

A – Assessment: JPMorgan demonstrates solid fundamental strength with revenue growth across segments. The fortress balance sheet provides flexibility for economic volatility.

P – Plan: Monitor credit provision trends, assess interest rate sensitivity, evaluate investment banking recovery, track digital transformation progress.
```

## 🏆 MLH Prize Features

### **Best Use of Gemini API**
- Advanced SMAP generation with structured data extraction
- Risk factor categorization and financial metrics parsing
- Educational feedback generation

### **Best Use of ElevenLabs**
- Voice synthesis for earnings call simulation
- Management and analyst voices
- Audio briefings for study purposes

### **Best Use of Snowflake API**
- Financial data storage and analytics
- Historical benchmarking and comparisons
- Risk factor and business segment tracking

### **Other Prize Categories**
- **Social Good:** Democratizing financial education
- **Education:** Interactive learning platform
- **Maverick:** Innovative AI + finance solution

## 🔧 Troubleshooting

### **Common Issues**

#### **API Quota Exceeded**
- Gemini API has daily limits on free tier
- ElevenLabs may have usage limits
- System runs in simulation mode when limits hit

#### **Frontend Not Loading**
```bash
cd Frontend
npm install
npm run dev
```

#### **Backend Errors**
```bash
pip install -r requirements.txt
python backend_app.py
```

#### **Port Already in Use**
- Backend uses port 8000
- Frontend uses port 3000
- Change ports in respective config files if needed

### **Logs and Debugging**
- Backend logs appear in terminal
- Frontend logs in browser console
- Check `integration_test_report.json` for test results

## 📱 API Endpoints

### **Main Endpoints**
- **Root:** http://localhost:8000/
- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs

### **Key API Routes**
- `POST /api/auth/login` - Student authentication
- `POST /api/upload/filing` - Upload SEC filing
- `GET /api/session/{id}/learn` - Enter learn mode
- `GET /api/session/{id}/practice` - Enter practice mode
- `POST /api/session/{id}/practice/submit` - Submit student work
- `GET /api/session/{id}/feedback` - Get AI feedback
- `GET /api/session/{id}/earnings-call` - Generate earnings call

## 🎯 For Judges Demo

### **Quick Demo Script**
1. Run: `python start_complete_app.py`
2. Choose option 1 (Run Complete Demo)
3. Show the complete product flow
4. Highlight MLH prize features
5. Demonstrate all three learning modes

### **Key Points to Emphasize**
- **Innovation:** SMAP framework for finance education
- **AI Integration:** Gemini, ElevenLabs, Snowflake
- **Educational Value:** Interactive learning with feedback
- **Social Impact:** Democratizing financial literacy
- **Technical Excellence:** Full-stack implementation

## 📞 Support

### **Documentation**
- `README_COMPLETE_PRODUCT_FLOW.md` - Detailed product overview
- `HACKRU_2025_SUBMISSION_SUMMARY.md` - Submission summary
- `integration_test_report.json` - Test results

### **Contact**
- **Project:** 10Q Notes AI
- **HackRU 2025:** SMAP Finance Notes AI
- **Developer:** azrabano

---

*Ready to win multiple MLH prizes with innovative AI + finance solution!*
