import { useEffect } from "react";
import styles from "./Toast.module.css";

export type ToastType = "success" | "error" | "warning" | "info";

interface Props {
  message: string;
  type?: ToastType;
  onClose: () => void;
  duration?: number;
}

export function Toast({ message, type = "info", onClose, duration = 3000 }: Props) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [onClose, duration]);

  const style = type === "info" ? styles.warning : styles[type];

  return <div className={`${styles.toast} ${style}`}>{message}</div>;
}
