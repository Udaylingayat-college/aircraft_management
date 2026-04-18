import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Plane } from "lucide-react";
import client from "../api/client";
import styles from "./AuthPages.module.css";

export function SignupPage() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("viewer");
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");

    if (!email.includes("@")) {
      setError("Please enter a valid email");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await client.post("/auth/signup", {
        full_name: fullName,
        email,
        password,
        role,
      });
      navigate("/login", { state: { message: "Account created successfully. Please sign in." } });
    } catch {
      setError("Failed to create account");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.brand}>
          <Plane size={40} color="#7c3aed" />
          <h1 className={styles.title}>{"Aircraft Fleet\nManagement"}</h1>
        </div>
        <p className={styles.subtitle}>Create your account</p>

        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="signup-full-name">Full Name</label>
            <input
              id="signup-full-name"
              className={styles.input}
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="signup-email">Email</label>
            <input
              id="signup-email"
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="signup-password">Password</label>
            <input
              id="signup-password"
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="signup-confirm-password">Confirm Password</label>
            <input
              id="signup-confirm-password"
              className={styles.input}
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="signup-role">Role</label>
            <select
              id="signup-role"
              className={styles.select}
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="viewer">Viewer</option>
              <option value="engineer">Engineer</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <button className={styles.button} type="submit">Create Account</button>
          {error && <p className={styles.error}>{error}</p>}
        </form>

        <p className={styles.footer}>
          Already have an account? <Link className={styles.footerLink} to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
