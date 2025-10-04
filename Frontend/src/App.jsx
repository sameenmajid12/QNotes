import { useState, useEffect } from "react";
import { supabase } from "./supabaseClient";
import "./index.css";

function App() {
  const [user, setUser] = useState(null);
  const [showSignup, setShowSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (data.session) setUser(data.session.user);
    });

    const { data: subscription } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription?.subscription?.unsubscribe();
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) alert(error.message);
    else setUser(data.user);
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    const { data, error } = await supabase.auth.signUp({ email, password });
    if (error) alert(error.message);
    else alert("Signup successful! Check your email for confirmation.");
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  if (user) {
    return (
      <div className="container">
        <div className="card logged-in">
          <h1>Welcome, {user.email}</h1>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container gradient-bg">
      <div className="card">
        <h1 className="title">Q Notes</h1>
        <form onSubmit={showSignup ? handleSignup : handleLogin}>
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
            onClick={() => setShowSignup(!showSignup)}
          >
            {showSignup ? "Login" : "Sign Up"}
          </button>
        </p>
      </div>
    </div>
  );
}

export default App;
