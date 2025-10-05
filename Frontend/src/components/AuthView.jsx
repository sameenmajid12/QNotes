import { useState } from "react";
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

export default AuthView;