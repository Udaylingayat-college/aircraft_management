import styles from "./ProgressBar.module.css";

interface Props {
  value: number;
  max: number;
  showLabel?: boolean;
}

export function ProgressBar({ value, max, showLabel = true }: Props) {
  const pct = max > 0 ? Math.min(100, Math.round((value / max) * 100)) : 0;
  return (
    <div className={styles.wrapper}>
      <div className={styles.bar}>
        <div className={styles.fill} style={{ width: `${pct}%` }} />
      </div>
      {showLabel && (
        <span className={styles.label}>
          {value} / {max} ({pct}%)
        </span>
      )}
    </div>
  );
}
