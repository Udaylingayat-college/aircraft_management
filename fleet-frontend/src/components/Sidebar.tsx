import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.css";

const links = [
  { to: "/", label: "Dashboard", icon: "📊" },
  { to: "/units", label: "Units", icon: "🏛️" },
  { to: "/hangars", label: "Hangars", icon: "🏗️" },
  { to: "/aircraft", label: "Aircraft", icon: "✈️" },
  { to: "/assets", label: "Assets", icon: "📦" },
  { to: "/transactions", label: "Transactions", icon: "🔄" },
  { to: "/inspections", label: "Inspections", icon: "🔍" },
];

export function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>✈ Fleet Manager</div>
      <nav className={styles.nav}>
        {links.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.navLinkActive : ""}`
            }
          >
            <span>{icon}</span>
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
