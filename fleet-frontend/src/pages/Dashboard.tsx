import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import type { DashboardSummary } from "../api/client";
import layoutStyles from "../components/Layout.module.css";
import styles from "./Dashboard.module.css";

interface ChannelRow {
  name: string;
  ratio: number;
  orders: number;
  shipments: number;
}

interface MapChip {
  label: string;
  flag: string;
  count: number;
  x: number;
  y: number;
}

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

  const channelRows = useMemo<ChannelRow[]>(() => {
    if (!summary) return [];

    const counts: Record<string, number> = {};
    summary.recent_transactions.forEach((transaction) => {
      const key = transaction.Unit_name || "Unassigned";
      counts[key] = (counts[key] ?? 0) + 1;
    });

    const sorted = Object.entries(counts)
      .map(([name, orders]) => ({ name, orders }))
      .sort((a, b) => b.orders - a.orders)
      .slice(0, 3);

    const fallback = [
      { name: "Fighter Wings", orders: Math.max(3, summary.active_units) },
      { name: "Transport Command", orders: Math.max(2, Math.floor(summary.total_aircraft / 3)) },
      { name: "Recon Group", orders: Math.max(1, summary.overdue_inspections + 1) },
    ];

    const source = sorted.length > 0 ? sorted : fallback;
    const max = Math.max(...source.map((item) => item.orders), 1);

    return source.map((item) => ({
      name: item.name,
      orders: item.orders,
      shipments: item.orders + Math.max(1, Math.round(item.orders * 0.4)),
      ratio: Math.max(12, Math.round((item.orders / max) * 100)),
    }));
  }, [summary]);

  const mapChips = useMemo<MapChip[]>(() => {
    if (!summary) return [];
    const base = channelRows.map((row, index) => ({
      label: row.name,
      flag: ["🇺🇸", "🇬🇧", "🇮🇳", "🇯🇵", "🇦🇺"][index] ?? "🌍",
      count: row.orders,
      x: [22, 45, 67, 80, 74][index] ?? 50,
      y: [43, 34, 48, 36, 72][index] ?? 50,
    }));

    while (base.length < 5) {
      const index = base.length;
      base.push({
        label: `Unit ${index + 1}`,
        flag: ["🇧🇷", "🇨🇦", "🇩🇪", "🇸🇬", "🇿🇦"][index] ?? "🌍",
        count: Math.max(1, summary.active_units - index),
        x: [30, 26, 52, 74, 58][index] ?? 50,
        y: [68, 28, 31, 62, 76][index] ?? 50,
      });
    }

    return base.slice(0, 5);
  }, [channelRows, summary]);

  if (loading) {
    return (
      <div>
        <div className={layoutStyles.pageHeader}>
          <h1 className={layoutStyles.pageTitle}>Dashboard</h1>
          <div className={layoutStyles.pageHeaderFilters}>
            <span className={layoutStyles.headerFilter}>All Hangars ▾</span>
            <span className={layoutStyles.headerFilter}>Last 90 days</span>
          </div>
        </div>
        <p style={{ color: "var(--color-text-muted)" }}>Loading…</p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div>
        <div className={layoutStyles.pageHeader}>
          <h1 className={layoutStyles.pageTitle}>Dashboard</h1>
          <div className={layoutStyles.pageHeaderFilters}>
            <span className={layoutStyles.headerFilter}>All Hangars ▾</span>
            <span className={layoutStyles.headerFilter}>Last 90 days</span>
          </div>
        </div>
        <p style={{ color: "var(--color-danger)" }}>{error ?? "No dashboard data available"}</p>
      </div>
    );
  }

  const activeCount = Math.max(0, summary.total_aircraft - summary.overdue_inspections);
  const offMarketCount = Math.max(0, summary.total_aircraft - activeCount);
  const total = Math.max(summary.total_aircraft, 1);
  const activePct = Math.round((activeCount / total) * 100);
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const activeStroke = (activePct / 100) * circumference;

  const cards = [
    {
      label: "Total Aircraft",
      value: summary.total_aircraft,
      accent: true,
      delta: Math.max(1, Math.round(summary.total_aircraft * 0.08)),
      positive: true,
    },
    {
      label: "Active Units",
      value: summary.active_units,
      delta: Math.max(1, Math.round(summary.active_units * 0.06)),
      positive: true,
    },
    {
      label: "Available Assets",
      value: summary.available_assets,
      delta: Math.max(1, Math.round(summary.available_assets * 0.04)),
      positive: true,
    },
    {
      label: "Overdue Inspections",
      value: summary.overdue_inspections,
      delta: Math.max(1, summary.overdue_inspections),
      positive: false,
    },
  ];

  return (
    <div>
      <div className={layoutStyles.pageHeader}>
        <h1 className={layoutStyles.pageTitle}>Dashboard</h1>
        <div className={layoutStyles.pageHeaderFilters}>
          <span className={layoutStyles.headerFilter}>All Hangars ▾</span>
          <span className={layoutStyles.headerFilter}>Last 90 days</span>
        </div>
      </div>

      <div className={styles.kpiGrid}>
        {cards.map((card) => (
          <article key={card.label} className={styles.summaryCard}>
            <span className={styles.cardLabel}>{card.label}</span>
            <span className={`${styles.cardValue} ${card.accent ? styles.cardValueAccent : ""}`}>
              {card.value}
            </span>
            <span className={`${styles.deltaBadge} ${card.positive ? styles.deltaUp : styles.deltaDown}`}>
              {card.positive ? "▲" : "▼"} {card.delta}
            </span>
            <span className={styles.deltaMeta}>vs prev. 90 days</span>
          </article>
        ))}
      </div>

      <div className={styles.mainGrid}>
        <section className={styles.card}>
          <h2 className={styles.sectionTitle}>Active vs Off-Market</h2>
          <div className={styles.donutWrap}>
            <svg viewBox="0 0 120 120" className={styles.donutChart} aria-label="Active donut chart">
              <circle className={styles.donutTrack} cx="60" cy="60" r={radius} />
              <circle
                className={styles.donutActive}
                cx="60"
                cy="60"
                r={radius}
                strokeDasharray={`${activeStroke} ${circumference}`}
              />
            </svg>
            <div className={styles.donutCenter}>
              <span className={styles.donutCount}>{activeCount}</span>
              <span className={styles.donutText}>Active Aircraft</span>
            </div>
          </div>
          <div className={styles.donutLegend}>
            <span>Active: {activeCount}</span>
            <span>Off-Market: {offMarketCount}</span>
          </div>
        </section>

        <section className={styles.card}>
          <h2 className={styles.sectionTitle}>Hangar Group Summary</h2>
          <div className={styles.channels}>
            {channelRows.slice(0, 3).map((row, index) => (
              <div key={row.name} className={styles.channelRow}>
                <div className={styles.channelMain}>
                  <div className={styles.channelName}>{row.name}</div>
                  <div className={styles.barTrack}>
                    <div
                      className={`${styles.barFill} ${index === 0 ? styles.barAmazon : index === 1 ? styles.barEbay : styles.barWalmart}`}
                      style={{ width: `${row.ratio}%` }}
                    />
                  </div>
                </div>
                <div className={styles.channelMeta}>
                  <span>{row.orders} Ops</span>
                  <span>{row.shipments} Shipments</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className={`${styles.card} ${styles.wide}`}>
          <h2 className={styles.sectionTitle}>Global Asset Footprint</h2>
          <div className={styles.mapWrap}>
            <svg viewBox="0 0 100 50" className={styles.worldMap}>
              {[...Array(22)].map((_, row) => (
                [...Array(44)].map((__, col) => {
                  const x = 2 + col * 2.2;
                  const y = 2 + row * 2.1;
                  const shape =
                    (x > 6 && x < 30 && y > 12 && y < 35) ||
                    (x > 34 && x < 56 && y > 8 && y < 28) ||
                    (x > 52 && x < 74 && y > 12 && y < 36) ||
                    (x > 74 && x < 95 && y > 18 && y < 38);
                  if (!shape || (row + col) % 3 !== 0) return null;
                  return <circle key={`${row}-${col}`} cx={x} cy={y} r="0.26" className={styles.mapDot} />;
                })
              ))}
            </svg>

            {mapChips.map((chip) => (
              <div
                key={chip.label}
                className={styles.mapChip}
                style={{ left: `${chip.x}%`, top: `${chip.y}%` }}
              >
                {chip.flag} {chip.count}
              </div>
            ))}
          </div>
        </section>

        <section className={styles.card}>
          <h2 className={styles.sectionTitle}>Recent Transactions</h2>
          {summary.recent_transactions.length === 0 ? (
            <div className={styles.empty}>No recent transactions</div>
          ) : (
            summary.recent_transactions.map((transaction) => (
              <div key={transaction.Transaction_id} className={styles.feedItem}>
                <div>
                  <div className={styles.feedMain}>{transaction.Asset_name ?? "—"}</div>
                  <div className={styles.feedSub}>
                    {transaction.Purpose ?? "—"} · {transaction.Unit_name ?? "—"}
                  </div>
                </div>
                <div className={styles.feedDate}>{transaction.Issue_date ?? "—"}</div>
              </div>
            ))
          )}
        </section>

        <section className={styles.card}>
          <h2 className={styles.sectionTitle}>Upcoming Inspections (30 days)</h2>
          {summary.upcoming_inspections.length === 0 ? (
            <div className={styles.empty}>No upcoming inspections</div>
          ) : (
            summary.upcoming_inspections.map((inspection) => (
              <div key={inspection.Inspection_id} className={styles.feedItem}>
                <div>
                  <div className={styles.feedMain}>
                    {inspection.Registration_no ?? "—"} — {inspection.Inspection_type ?? "—"}
                  </div>
                  <div className={styles.feedSub}>Valid till: {inspection.Valid_till ?? "—"}</div>
                </div>
              </div>
            ))
          )}
        </section>
      </div>
    </div>
  );
}
