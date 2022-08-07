import "./Register.css";

export default function Register() {
  return (
    <div className="login">
      <div className="loginWrapper">
        <div className="loginLeft">
          <h3 className="loginLogo">Raabta</h3>
          <span className="loginDesc">
            Connect with your friends on Raabta.
          </span>
        </div>
        <div className="loginRight">
          <div className="loginBox">
            <input placeholder="Username" className="loginInput" />
            <input placeholder="Email" className="loginInput" />
            <input placeholder="Password" className="loginInput" />
            <input placeholder="Confirm Password" className="loginInput" />
            <button className="signUpButton">Sign Up</button>
            <button className="loginButtton">
              Log into Account
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
