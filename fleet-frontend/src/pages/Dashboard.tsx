import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { DashboardSummary } from "../api/client";
import layoutStyles from "../components/Layout.module.css";
import styles from "./Dashboard.module.css";

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getDashboardSummary()
      .then(setSummary)
      .catch(() => setError("Failed to load dashboard data"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>;
  if (error) return <p style={{ color: "var(--color-danger)" }}>{error}</p>;
  if (!summary) return null;

  return (
    <div>
      <h1 className={layoutStyles.pageTitle}>Dashboard</h1>

      <div className={styles.grid}>
        <div className={styles.summaryCard}>
          <span className={styles.cardLabel}>Total Aircraft</span>
          <span className={styles.cardValue}>{summary.total_aircraft}</span>
        </div>
        <div className={styles.summaryCard}>
          <span className={styles.cardLabel}>Active Units</span>
          <span className={styles.cardValue}>{summary.active_units}</span>
        </div>
        <div className={styles.summaryCard}>
          <span className={styles.cardLabel}>Available Assets</span>
          <span className={styles.cardValue}>{summary.available_assets}</span>
        </div>
        <div className={styles.summaryCard}>
          <span className={styles.cardLabel}>Overdue Inspections</span>
          <span
            className={`${styles.cardValue} ${
              summary.overdue_inspections > 0 ? styles.cardValueDanger : ""
            }`}
          >
            {summary.overdue_inspections}
          </span>
        </div>
      </div>

      <div className={styles.sectionsRow}>
        <div className={styles.section}>
          <div className={styles.sectionTitle}>Recent Transactions</div>
          {summary.recent_transactions.length === 0 ? (
            <div className={styles.empty}>No recent transactions</div>
          ) : (
            summary.recent_transactions.map((t) => (
              <div key={t.Transaction_id} className={styles.feedItem}>
                <div>
                  <div className={styles.feedAsset}>{t.Asset_name ?? "—"}</div>
                  <div className={styles.feedMeta}>
                    {t.Purpose ?? "—"} · {t.Unit_name ?? "—"}
                  </div>
                </div>
                <div className={styles.feedDate}>{t.Issue_date ?? "—"}</div>
              </div>
            ))
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionTitle}>Upcoming Inspections (30 days)</div>
          {summary.upcoming_inspections.length === 0 ? (
            <div className={styles.empty}>No upcoming inspections</div>
          ) : (
            summary.upcoming_inspections.map((insp) => (
              <div key={insp.Inspection_id} className={styles.alertItem}>
                <div className={styles.alertReg}>
                  {insp.Registration_no ?? "—"} — {insp.Inspection_type ?? "—"}
                </div>
                <div className={styles.alertExpiry}>
                  Valid till: {insp.Valid_till ?? "—"}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
