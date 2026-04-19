import { useState } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { Plane } from "lucide-react";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const successMessage = location.state?.message;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Login failed");
      }
      localStorage.setItem("afm_token", data.token);
      localStorage.setItem("afm_user", JSON.stringify(data.user));
      navigate("/");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--color-bg)' }}>
      <div style={{ backgroundColor: '#ffffff', borderRadius: '16px', boxShadow: '0 4px 24px rgba(0,0,0,0.10)', width: '420px', padding: '48px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Plane size={40} color="#7c3aed" />
        <h1 style={{ fontFamily: "'Inter', sans-serif", fontWeight: 800, fontSize: '26px', color: '#1a1a2e', lineHeight: 1.2, textAlign: 'center', marginTop: '16px', marginBottom: '8px', whiteSpace: 'pre-line' }}>Aircraft Fleet{"\n"}Management</h1>
        <p style={{ fontSize: '14px', color: '#6b7280', textAlign: 'center', marginBottom: '32px', marginTop: 0 }}>Sign in to your account</p>
        
        {successMessage && <div style={{ color: 'green', fontSize: '14px', marginBottom: '16px', textAlign: 'center' }}>{successMessage}</div>}

        <form onSubmit={handleLogin} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontSize: '14px', fontWeight: 500 }}>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none', transition: 'all 0.2s' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontSize: '14px', fontWeight: 500 }}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none', transition: 'all 0.2s' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          
          <button type="submit" style={{ width: '100%', background: '#7c3aed', color: 'white', border: 'none', borderRadius: '8px', padding: '12px', fontWeight: 600, fontSize: '15px', cursor: 'pointer', marginTop: '8px', transition: 'background 0.2s' }} onMouseOver={e => e.currentTarget.style.background = '#6d28d9'} onMouseOut={e => e.currentTarget.style.background = '#7c3aed'}>Sign In</button>
          
          {error && <div style={{ color: 'red', marginTop: '8px', textAlign: 'center', fontSize: '14px' }}>{error}</div>}
          
          <div style={{ textAlign: 'center', marginTop: '16px', fontSize: '14px' }}>
            <Link to="/signup" style={{ color: '#7c3aed', textDecoration: 'none', fontWeight: 500 }}>Don't have an account? Sign up</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
