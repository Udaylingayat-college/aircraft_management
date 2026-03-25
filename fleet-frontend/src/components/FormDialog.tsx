import { type ReactNode, useEffect, useRef } from "react";
import styles from "./FormDialog.module.css";

export interface FieldDef {
  name: string;
  label: string;
  type?: "text" | "number" | "date" | "select";
  options?: string[];
  required?: boolean;
}

interface Props {
  title: string;
  fields: FieldDef[];
  values: Record<string, string>;
  onChange: (name: string, value: string) => void;
  onSave: () => void;
  onClose: () => void;
  extraContent?: ReactNode;
}

export function FormDialog({
  title,
  fields,
  values,
  onChange,
  onSave,
  onClose,
  extraContent,
}: Props) {
  const firstRef = useRef<HTMLInputElement | HTMLSelectElement | null>(null);

  useEffect(() => {
    firstRef.current?.focus();

    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onClose]);

  return (
    <div className={styles.overlay} onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className={styles.dialog}>
        <div className={styles.title}>{title}</div>
        <div className={styles.form}>
          {fields.map((field, idx) => (
            <div key={field.name} className={styles.field}>
              <label className={styles.label}>{field.label}</label>
              {field.type === "select" ? (
                <select
                  className={styles.select}
                  value={values[field.name] ?? ""}
                  onChange={(e) => onChange(field.name, e.target.value)}
                  ref={idx === 0 ? (el) => { firstRef.current = el; } : undefined}
                >
                  <option value="">— Select —</option>
                  {(field.options ?? []).map((opt) => (
                    <option key={opt} value={opt}>
                      {opt}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  className={styles.input}
                  type={field.type ?? "text"}
                  value={values[field.name] ?? ""}
                  required={field.required}
                  onChange={(e) => onChange(field.name, e.target.value)}
                  ref={idx === 0 ? (el) => { firstRef.current = el; } : undefined}
                />
              )}
            </div>
          ))}
          {extraContent}
        </div>
        <div className={styles.actions}>
          <button className={styles.cancelBtn} onClick={onClose}>
            Cancel
          </button>
          <button className={styles.saveBtn} onClick={onSave}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
