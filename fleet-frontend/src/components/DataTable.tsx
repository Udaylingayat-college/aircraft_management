import { type ReactNode, useState } from "react";
import styles from "./DataTable.module.css";

export interface Column<T> {
  key: string;
  header: string;
  render?: (row: T) => ReactNode;
}

export interface FilterOption {
  key: string;
  label: string;
  options: string[];
}

interface Props<T> {
  columns: Column<T>[];
  data: T[];
  rowKey: (row: T) => string | number;
  rowClassName?: (row: T) => string;
  filters?: FilterOption[];
  onAdd?: () => void;
  onEdit?: (row: T) => void;
  onDelete?: (row: T) => void;
  loading?: boolean;
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  rowKey,
  rowClassName,
  filters = [],
  onAdd,
  onEdit,
  onDelete,
  loading = false,
}: Props<T>) {
  const [search, setSearch] = useState("");
  const [filterValues, setFilterValues] = useState<Record<string, string>>({});

  const filtered = data.filter((row) => {
    const searchLower = search.toLowerCase();
    const matchesSearch =
      search === "" ||
      Object.values(row).some((v) =>
        String(v ?? "").toLowerCase().includes(searchLower)
      );

    const matchesFilters = filters.every(({ key }) => {
      const filterVal = filterValues[key];
      if (!filterVal) return true;
      return String(row[key] ?? "").toLowerCase() === filterVal.toLowerCase();
    });

    return matchesSearch && matchesFilters;
  });

  return (
    <div className={styles.wrapper}>
      <div className={styles.toolbar}>
        <div className={styles.filtersRow}>
          <input
            className={styles.searchInput}
            placeholder="Search…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          {filters.map(({ key, label, options }) => (
            <select
              key={key}
              className={styles.filterSelect}
              value={filterValues[key] ?? ""}
              onChange={(e) =>
                setFilterValues((prev) => ({ ...prev, [key]: e.target.value }))
              }
            >
              <option value="">{label}</option>
              {options.map((o) => (
                <option key={o} value={o}>
                  {o}
                </option>
              ))}
            </select>
          ))}
        </div>
        {onAdd && (
          <button className={styles.addBtn} onClick={onAdd}>
            + Add New
          </button>
        )}
      </div>

      {loading ? (
        <div className={styles.loading}>Loading…</div>
      ) : (
        <table className={styles.table}>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.header}</th>
              ))}
              {(onEdit || onDelete) && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length + (onEdit || onDelete ? 1 : 0)}
                  className={styles.empty}
                >
                  No records found
                </td>
              </tr>
            ) : (
              filtered.map((row) => {
                const extra = rowClassName ? rowClassName(row) : "";
                return (
                  <tr
                    key={rowKey(row)}
                    className={
                      extra === "amber"
                        ? styles.rowAmber
                        : extra === "red"
                        ? styles.rowRed
                        : ""
                    }
                  >
                    {columns.map((col) => (
                      <td key={col.key}>
                        {col.render
                          ? col.render(row)
                          : String(row[col.key] ?? "—")}
                      </td>
                    ))}
                    {(onEdit || onDelete) && (
                      <td>
                        <div className={styles.actionCell}>
                          {onEdit && (
                            <button
                              className={styles.editBtn}
                              onClick={() => onEdit(row)}
                            >
                              Edit
                            </button>
                          )}
                          {onDelete && (
                            <button
                              className={styles.deleteBtn}
                              onClick={() => onDelete(row)}
                            >
                              Delete
                            </button>
                          )}
                        </div>
                      </td>
                    )}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
