import {
  ArrowLeftRight,
  Building2,
  ClipboardCheck,
  LayoutDashboard,
  Package,
  Plane,
  Warehouse,
  LogOut,
  type LucideIcon,
} from "lucide-react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import styles from "./Sidebar.module.css";
import { useEffect, useState } from "react";

const links: Array<{ to: string; label: string; icon: LucideIcon }> = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/units", label: "Units", icon: Building2 },
  { to: "/hangars", label: "Hangars", icon: Warehouse },
  { to: "/aircraft", label: "Aircraft", icon: Plane },
  { to: "/assets", label: "Assets", icon: Package },
  { to: "/transactions", label: "Transactions", icon: ArrowLeftRight },
  { to: "/inspections", label: "Inspections", icon: ClipboardCheck },
];

export function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState<{full_name: string, role: string} | null>(null);

  useEffect(() => {
    const userData = localStorage.getItem("afm_user");
    if (userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {}
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("afm_token");
    localStorage.removeItem("afm_user");
    navigate("/login");
  };

  const getInitials = (name: string) => {
    if (!name) return "U";
    return name.split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>
        <Plane size={28} color="#7c3aed" />
        <span>{"Aircraft Fleet\nManagement"}</span>
      </div>

      <nav className={styles.nav}>
        {links.map(({ to, label, icon: Icon }) => {
          const active = to === "/" ? location.pathname === to : location.pathname.startsWith(to);
          return (
            <NavLink
              key={to}
              to={to}
              className={`${styles.navLink} ${active ? styles.navLinkActive : ""}`}
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className={styles.userCard}>
        <div className={styles.userAvatar}>{getInitials(user?.full_name || "")}</div>
        <div className={styles.userInfo}>
          <div className={styles.userName}>{user?.full_name || "User"}</div>
          <div className={styles.userRole}>{user?.role || "viewer"}</div>
        </div>
        <LogOut size={16} color="rgba(255,255,255,0.45)" className={styles.logoutIcon} onClick={handleLogout} />
      </div>
    </aside>
  );
}
