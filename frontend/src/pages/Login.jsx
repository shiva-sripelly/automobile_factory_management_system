import { Lock, Mail } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "../services/http";

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [signupForm, setSignupForm] = useState({
    full_name: "",
    email: "",
    password: "",
    role: "worker",
  });
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [mode, setMode] = useState("login");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSignupChange = (event) => {
    const { name, value } = event.target;
    setSignupForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setNotice("");
    setIsSubmitting(true);

    try {
      const { data } = await http.post("/auth/login", form);
      localStorage.setItem("afms_token", data.access_token);

      try {
        const me = await http.get("/auth/me");
        localStorage.setItem("afms_user", JSON.stringify(me.data));
      } catch {
        localStorage.removeItem("afms_user");
      }

      navigate("/", { replace: true });
    } catch (loginError) {
      setError(loginError.response?.data?.detail || "Unable to sign in.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignup = async (event) => {
    event.preventDefault();
    setError("");
    setNotice("");
    setIsSubmitting(true);

    try {
      await http.post("/auth/register", signupForm);
      setForm({
        email: signupForm.email,
        password: signupForm.password,
      });
      setSignupForm({
        full_name: "",
        email: "",
        password: "",
        role: "worker",
      });
      setMode("login");
      setNotice("Account created. Sign in with your new credentials.");
    } catch (signupError) {
      setError(signupError.response?.data?.detail || "Unable to create account.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleForgotPassword = () => {
    setError("");
    setNotice("Password reset is not connected yet. Ask an admin to reset it.");
  };

  const showSignup = mode === "signup";

  return (
    <main className="login-page">
      <section className="login-panel" aria-labelledby="login-title">
        <div className="login-copy">
          <span className="eyebrow">Automobile Factory ERP</span>
          <h1 id="login-title">
            {showSignup ? "Create your account" : "Sign in to operations"}
          </h1>
          <p>
            Track departments, factories, people, production, inventory, and
            quality from one focused workspace.
          </p>
        </div>

        {showSignup ? (
          <form className="login-form" onSubmit={handleSignup}>
            <label>
              <span>Full name</span>
              <div className="field">
                <input
                  autoComplete="name"
                  name="full_name"
                  onChange={handleSignupChange}
                  placeholder="Development Admin"
                  required
                  type="text"
                  value={signupForm.full_name}
                />
              </div>
            </label>

            <label>
              <span>Email address</span>
              <div className="field">
                <Mail size={18} />
                <input
                  autoComplete="email"
                  name="email"
                  onChange={handleSignupChange}
                  placeholder="name@factory.com"
                  required
                  type="email"
                  value={signupForm.email}
                />
              </div>
            </label>

            <label>
              <span>Password</span>
              <div className="field">
                <Lock size={18} />
                <input
                  autoComplete="new-password"
                  name="password"
                  onChange={handleSignupChange}
                  placeholder="Create password"
                  required
                  type="password"
                  value={signupForm.password}
                />
              </div>
            </label>

            <label>
              <span>Role</span>
              <select
                className="select-field"
                name="role"
                onChange={handleSignupChange}
                value={signupForm.role}
              >
                <option value="worker">Worker</option>
                <option value="supervisor">Supervisor</option>
                <option value="engineer">Engineer</option>
                <option value="manager">Manager</option>
                <option value="admin">Admin</option>
              </select>
            </label>

            {error ? <p className="form-error">{error}</p> : null}
            {notice ? <p className="form-notice">{notice}</p> : null}

            <button disabled={isSubmitting} type="submit">
              {isSubmitting ? "Creating..." : "Create account"}
            </button>

            <div className="form-actions">
              <button
                className="text-button"
                onClick={() => {
                  setMode("login");
                  setError("");
                  setNotice("");
                }}
                type="button"
              >
                Back to login
              </button>
            </div>
          </form>
        ) : (
          <form className="login-form" onSubmit={handleSubmit}>
            <label>
              <span>Email address</span>
              <div className="field">
                <Mail size={18} />
                <input
                  autoComplete="email"
                  name="email"
                  onChange={handleChange}
                  placeholder="dev.admin@factory.com"
                  required
                  type="email"
                  value={form.email}
                />
              </div>
            </label>

            <label>
              <span>Password</span>
              <div className="field">
                <Lock size={18} />
                <input
                  autoComplete="current-password"
                  name="password"
                  onChange={handleChange}
                  placeholder="Enter password"
                  required
                  type="password"
                  value={form.password}
                />
              </div>
            </label>

            {error ? <p className="form-error">{error}</p> : null}
            {notice ? <p className="form-notice">{notice}</p> : null}

            <button disabled={isSubmitting} type="submit">
              {isSubmitting ? "Signing in..." : "Sign in"}
            </button>

            <div className="form-actions">
              <button
                className="text-button"
                onClick={() => {
                  setMode("signup");
                  setError("");
                  setNotice("");
                }}
                type="button"
              >
                Sign up
              </button>
              <button
                className="text-button"
                onClick={handleForgotPassword}
                type="button"
              >
                Forgot password?
              </button>
            </div>
          </form>
        )}
      </section>
    </main>
  );
}

export default Login;
