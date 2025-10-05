import "./index.css";
import LandingPage from "./components/LandingPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AuthView from "./components/AuthView";
import useUser from "./hooks/useUser";
import { useState } from "react";
import Learn from "./components/Learn";
import Practice from "./components/Practice";
import VoiceAgent from "./components/VoiceAgent";
import Sidebar from "./components/Sidebar";
import Header from "./components/header";
function App() {
  const { user, handleAuth, handleLogout, loading } = useUser();
  const [authMode, setAuthMode] = useState(null);
  const [file, setFile] = useState(null);
  if (authMode) {
    return (
      <div className="gradient-bg">
        <AuthView
          onLogin={(email, password) => handleAuth(false, email, password)}
          onSignup={(email, password) => handleAuth(true, email, password)}
          onToggleAuth={() =>
            setAuthMode(authMode === "login" ? "signup" : "login")
          }
          showSignup={authMode === "signup"}
        />
      </div>
    );
  }
  if (file) {
    return (
      <div>
        <Header
          onLoginClick={() => setAuthMode("login")}
          onSignupClick={() => setAuthMode("signup")}
          type={"dashboard"}
        />
        <Router>
          <div className="app-layout">
            <Sidebar handleLogout={handleLogout} />
            <main className="main-content">
              {file ? (
                <Routes>
                  <Route path="/" element={<Learn />} />
                  <Route path="/practice" element={<Practice />} />
                  <Route path="/agent" element={<VoiceAgent />} />
                </Routes>
              ) : (
                <NoFileScreen onSelectFile={setFile} />
              )}
            </main>
          </div>
        </Router>
      </div>
    );
  }

  return (
    <div>
      <Header
        onLoginClick={() => setAuthMode("login")}
        onSignupClick={() => setAuthMode("signup")}
      />
      <LandingPage setFile={setFile}/>
    </div>
  );
}

export default App;
