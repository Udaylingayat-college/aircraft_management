import { FormEvent, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Plane } from "lucide-react";
import client from "../api/client";
import styles from "./AuthPages.module.css";

interface LoginResponse {
  token: string;
  user: {
    id: number;
    full_name: string;
    email: string;
    role: string;
  };
}

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const successMessage = (location.state as { message?: string } | null)?.message;

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");

    try {
      const { data } = await client.post<LoginResponse>("/auth/login", { email, password });
      localStorage.setItem("afm_token", data.token);
      localStorage.setItem("afm_user", JSON.stringify(data.user));
      navigate("/");
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.brand}>
          <Plane size={40} color="#7c3aed" />
          <h1 className={styles.title}>{"Aircraft Fleet\nManagement"}</h1>
        </div>
        <p className={styles.subtitle}>Sign in to your account</p>
        {successMessage && <p className={styles.success}>{successMessage}</p>}

        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="login-email">Email</label>
            <input
              id="login-email"
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="login-password">Password</label>
            <input
              id="login-password"
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className={styles.button} type="submit">Sign In</button>
          {error && <p className={styles.error}>{error}</p>}
        </form>

        <p className={styles.footer}>
          Don&apos;t have an account? <Link className={styles.footerLink} to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
