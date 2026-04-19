import {
  ArrowLeftRight,
  Building2,
  ClipboardCheck,
  LayoutDashboard,
  Package,
  Plane,
  Warehouse,
  LogOut,
} from "lucide-react";
import { NavLink, Outlet, useNavigate, useLocation } from "react-router-dom";
import styles from "./Layout.module.css";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/units", label: "Units", icon: Building2 },
  { to: "/hangars", label: "Hangars", icon: Warehouse },
  { to: "/aircraft", label: "Aircraft", icon: Plane },
  { to: "/assets", label: "Assets", icon: Package },
  { to: "/transactions", label: "Transactions", icon: ArrowLeftRight },
  { to: "/inspections", label: "Inspections", icon: ClipboardCheck },
];

export function Layout() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    if (window.confirm("Do you want to logout?\n\nContinue or Cancel")) {
      localStorage.removeItem("afm_token");
      localStorage.removeItem("afm_user");
      navigate("/login");
    }
  };

  return (
    <div className={styles.layout}>
      <header className={styles.topbar}>
        <div className={styles.topbarUpper}>
          <div className={styles.brand}>
            <Plane size={24} color="#7c3aed" />
            <span>Aircraft Fleet Management</span>
          </div>
          <div className={styles.topbarRight}>
            <button onClick={handleLogout} className={styles.logoutBtn}>
              <LogOut size={16} /> Logout
            </button>
          </div>
        </div>
        <nav className={styles.navBar}>
          {links.map(({ to, label, icon: Icon }) => {
            const active = to === "/" ? location.pathname === to : location.pathname.startsWith(to);
            return (
              <NavLink
                key={to}
                to={to}
                className={`${styles.navLink} ${active ? styles.navLinkActive : ""}`}
              >
                <Icon size={16} />
                <span>{label}</span>
              </NavLink>
            );
          })}
        </nav>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  );
}
