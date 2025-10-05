import "../styles/header.css";
function Header({ onLoginClick, onSignupClick, type }) {
  return (
    <header
      className={`${type === "dashboard" ? "header-dashboard" : "header"}`}
    >
      <div className="logo-placeholder"><img className="logo" src="/assets/Logo.png"></img></div>
      <div className="auth-buttons">
        <button className="primary-btn login-btn" onClick={onLoginClick}>
          Login
        </button>
        <button className="secondary-btn signup-btn" onClick={onSignupClick}>
          Sign Up
        </button>
      </div>
    </header>
  );
}
export default Header;
