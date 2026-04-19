import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Plane } from "lucide-react";

export function SignupPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("viewer");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password !== confirmPassword) {
      setError("Passwords do not match"); return;
    }
    if (!email.includes("@")) {
      setError("Email must contain @"); return;
    }
    
    try {
      const res = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ full_name: fullName, email, password, role }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Signup failed");
      navigate("/login", { state: { message: "Account created successfully. Please sign in." } });
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--color-bg)', padding: '24px' }}>
      <div style={{ backgroundColor: '#ffffff', borderRadius: '16px', boxShadow: '0 4px 24px rgba(0,0,0,0.10)', width: '420px', padding: '48px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Plane size={40} color="#7c3aed" />
        <h1 style={{ fontFamily: "'Inter', sans-serif", fontWeight: 800, fontSize: '26px', color: '#1a1a2e', lineHeight: 1.2, textAlign: 'center', marginTop: '16px', marginBottom: '8px', whiteSpace: 'pre-line' }}>Aircraft Fleet{"\n"}Management</h1>
        <p style={{ fontSize: '14px', color: '#6b7280', textAlign: 'center', marginBottom: '24px', marginTop: 0 }}>Create a new account</p>
        
        <form onSubmit={handleSignup} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: 500 }}>Full Name</label>
            <input type="text" value={fullName} onChange={e => setFullName(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: 500 }}>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: 500 }}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: 500 }}>Confirm Password</label>
            <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: 500 }}>Role</label>
            <select value={role} onChange={e => setRole(e.target.value)} style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '10px 14px', fontSize: '14px', outline: 'none', background: 'white' }} onFocus={e => { e.currentTarget.style.borderColor = '#7c3aed'; e.currentTarget.style.boxShadow = '0 0 0 3px #ede9fe'; }} onBlur={e => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.boxShadow = 'none'; }}>
              <option value="viewer">Viewer</option>
              <option value="engineer">Engineer</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          
          <button type="submit" style={{ width: '100%', background: '#7c3aed', color: 'white', border: 'none', borderRadius: '8px', padding: '12px', fontWeight: 600, fontSize: '15px', cursor: 'pointer', marginTop: '8px' }} onMouseOver={e => e.currentTarget.style.background = '#6d28d9'} onMouseOut={e => e.currentTarget.style.background = '#7c3aed'}>Create Account</button>
          
          {error && <div style={{ color: 'red', marginTop: '8px', textAlign: 'center', fontSize: '14px' }}>{error}</div>}
          
          <div style={{ textAlign: 'center', marginTop: '16px', fontSize: '14px' }}>
            <Link to="/login" style={{ color: '#7c3aed', textDecoration: 'none', fontWeight: 500 }}>Already have an account? Sign in</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
