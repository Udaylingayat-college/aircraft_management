import styles from "./StatusBadge.module.css";

interface Props {
  value: string | null | undefined;
}

function toClassName(value: string): string {
  return value.toLowerCase().replace(/\s+/g, "_");
}

export function StatusBadge({ value }: Props) {
  if (!value) return <span className={styles.badge + " " + styles.default}>—</span>;
  const cls = toClassName(value);
  const style = styles[cls] ?? styles.default;
  return <span className={`${styles.badge} ${style}`}>{value}</span>;
}
