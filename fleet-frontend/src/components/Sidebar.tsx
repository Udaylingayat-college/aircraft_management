import {
  ArrowLeftRight,
  Building2,
  ClipboardCheck,
  LayoutDashboard,
  LogOut,
  Package,
  Plane,
  Warehouse,
  type LucideIcon,
} from "lucide-react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useMemo } from "react";
import styles from "./Sidebar.module.css";

const links: Array<{ to: string; label: string; icon: LucideIcon }> = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/units", label: "Units", icon: Building2 },
  { to: "/hangars", label: "Hangars", icon: Warehouse },
  { to: "/aircraft", label: "Aircraft", icon: Plane },
  { to: "/assets", label: "Assets", icon: Package },
  { to: "/transactions", label: "Transactions", icon: ArrowLeftRight },
  { to: "/inspections", label: "Inspections", icon: ClipboardCheck },
];

interface StoredUser {
  full_name?: string;
  role?: string;
}

export function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const user = useMemo<StoredUser>(() => {
    try {
      const raw = localStorage.getItem("afm_user");
      return raw ? (JSON.parse(raw) as StoredUser) : {};
    } catch {
      return {};
    }
  }, []);

  const fullName = user.full_name ?? "Guest User";
  const role = user.role ?? "viewer";
  const initials = fullName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("") || "GU";

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logoArea}>
        <Plane size={28} color="#7c3aed" />
        <span className={styles.logoText}>{"Aircraft Fleet\nManagement"}</span>
      </div>

      <nav className={styles.nav}>
        {links.map(({ to, label, icon: Icon }) => {
          const active = to === "/" ? location.pathname === to : location.pathname.startsWith(to);
          return (
            <NavLink
              key={to}
              to={to}
              className={`${styles.navItem} ${active ? styles.navItemActive : ""}`}
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className={styles.userArea}>
        <div className={styles.avatar}>{initials}</div>
        <div>
          <div className={styles.userName}>{fullName}</div>
          <div className={styles.userRole}>{role}</div>
        </div>
        <LogOut className={styles.logoutIcon} size={16} onClick={handleLogout} />
      </div>
    </aside>
  );
}
