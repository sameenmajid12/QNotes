import "./index.css";
import LandingPage from "./components/LandingPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthView from "./components/AuthView";
import EnhancedAuthView from "./components/EnhancedAuthView";
import useUser from "./hooks/useUser";
import { useState } from "react";
import Learn from "./components/Learn";
import EnhancedLearn from "./components/EnhancedLearn";
import Practice from "./components/Practice";
import EnhancedPractice from "./components/EnhancedPractice";
import SimplePractice from "./components/SimplePractice";
import VoiceAgent from "./components/VoiceAgent";
import EnhancedVoiceAgent from "./components/EnhancedVoiceAgent";
import SimpleVoiceAgent from "./components/SimpleVoiceAgent";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import WelcomeDashboard from "./components/WelcomeDashboard";

function App() {
  const { user, handleAuth, handleLogout, loading } = useUser();
  const [authMode, setAuthMode] = useState(null);
  const [file, setFile] = useState({ name: "Apple_10Q_2024.pdf" }); // Auto-set file for demo
  
  // Skip auth for demo - go straight to dashboard
  return (
    <div>
      <Header
        user={{ name: "Demo User" }}
        onLoginClick={() => setAuthMode("login")}
        onSignupClick={() => setAuthMode("signup")}
        onLogout={() => {}}
        type="dashboard"
      />
      <Router>
        <div className="app-layout">
          <Sidebar handleLogout={handleLogout} user={{ name: "Demo User" }} />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<EnhancedLearn file={file} />} />
              <Route path="/learn" element={<EnhancedLearn file={file} />} />
              <Route path="/practice" element={<EnhancedPractice file={file} />} />
              <Route path="/agent" element={<EnhancedVoiceAgent file={file} />} />
            </Routes>
          </main>
        </div>
      </Router>
    </div>
  );
}

export default App;
