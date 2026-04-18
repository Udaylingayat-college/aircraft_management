import {
  ArrowLeftRight,
  Building2,
  ChevronDown,
  ClipboardCheck,
  Compass,
  LayoutDashboard,
  Package,
  Plane,
  Warehouse,
  type LucideIcon,
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";
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

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>
        <Compass size={18} />
        <span>The NorthWest</span>
      </div>

      <nav className={styles.nav}>
        {links.map(({ to, label, icon: Icon }) => {
          const active = to === "/" ? location.pathname === to : location.pathname.startsWith(to);
          return (
            <Link
              key={to}
              to={to}
              className={`${styles.navLink} ${active ? styles.navLinkActive : ""}`}
            >
              <Icon size={16} />
              <span>{label}</span>
            </Link>
          );
        })}
      </nav>

      <div className={styles.userCard}>
        <span className={styles.userAvatar}>AU</span>
        <span className={styles.userName}>Admin User</span>
        <ChevronDown size={14} />
      </div>
    </aside>
  );
}
