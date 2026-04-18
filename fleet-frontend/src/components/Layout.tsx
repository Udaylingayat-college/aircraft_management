import { Bell, CircleHelp, Search, Settings } from "lucide-react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import styles from "./Layout.module.css";

export function Layout() {
  return (
    <div className={styles.layout}>
      <Sidebar />
      <div className={styles.contentArea}>
        <header className={styles.topbar}>
          <div className={styles.searchWrap}>
            <Search size={16} />
            <input className={styles.searchInput} placeholder="Search here…" />
          </div>
          <div className={styles.topbarRight}>
            <button className={styles.iconButton} aria-label="Support">
              <CircleHelp size={16} />
            </button>
            <button className={styles.iconButton} aria-label="Settings">
              <Settings size={16} />
            </button>
            <button className={styles.iconButton} aria-label="Notifications">
              <Bell size={16} />
            </button>
            <div className={styles.userChip}>
              <span className={styles.userAvatar}>AU</span>
              <span>Admin User</span>
            </div>
          </div>
        </header>
        <main className={styles.main}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
