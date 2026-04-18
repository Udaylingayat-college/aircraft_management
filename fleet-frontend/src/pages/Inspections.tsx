import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Inspection, Aircraft } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Inspection>[] = [
  { key: "Inspection_id", header: "ID" },
  { key: "Registration_no", header: "Aircraft" },
  { key: "Inspection_type", header: "Type" },
  { key: "Inspection_date", header: "Inspection Date" },
  { key: "Valid_till", header: "Valid Till" },
];

const EMPTY: Record<string, string> = {
  Inspection_id: "",
  Aircraft_id: "",
  Inspection_type: "",
  Inspection_date: "",
  Valid_till: "",
};

const INSPECTION_TYPES = [
  "Annual Inspection",
  "Safety Check",
  "Engine Inspection",
  "Avionics Check",
  "Structural Inspection",
  "Routine Maintenance",
];

export function Inspections() {
  const [data, setData] = useState<Inspection[]>([]);
  const [aircraft, setAircraft] = useState<Aircraft[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Inspection | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);

  const today = new Date().toISOString().slice(0, 10);
  const soon = new Date();
  soon.setDate(soon.getDate() + 30);
  const soonStr = soon.toISOString().slice(0, 10);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [inspList, aircraftList] = await Promise.all([
        api.getInspections(),
        api.getAircraft(),
      ]);
      setData(inspList);
      setAircraft(aircraftList);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const fields: FieldDef[] = [
    { name: "Inspection_id", label: "Inspection ID", type: "number", required: true },
    {
      name: "Aircraft_id",
      label: "Aircraft",
      type: "select",
      options: aircraft.map((a) => String(a.Aircraft_id)),
    },
    {
      name: "Inspection_type",
      label: "Type",
      type: "select",
      options: INSPECTION_TYPES,
    },
    { name: "Inspection_date", label: "Inspection Date", type: "date" },
    { name: "Valid_till", label: "Valid Till", type: "date" },
  ];

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Inspection) => {
    setEditing(row);
    setValues({
      Inspection_id: String(row.Inspection_id),
      Aircraft_id: row.Aircraft_id != null ? String(row.Aircraft_id) : "",
      Inspection_type: row.Inspection_type ?? "",
      Inspection_date: row.Inspection_date ?? "",
      Valid_till: row.Valid_till ?? "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Inspection) => {
    if (!confirm(`Delete inspection #${row.Inspection_id}?`)) return;
    try {
      await api.deleteInspection(row.Inspection_id);
      setToast({ msg: "Inspection deleted", type: "success" });
      load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      const payload = {
        Aircraft_id: values.Aircraft_id ? Number(values.Aircraft_id) : null,
        Inspection_type: values.Inspection_type || null,
        Inspection_date: values.Inspection_date || null,
        Valid_till: values.Valid_till || null,
      };
      if (editing) {
        await api.updateInspection(editing.Inspection_id, payload);
        setToast({ msg: "Inspection updated", type: "success" });
      } else {
        await api.createInspection({
          Inspection_id: Number(values.Inspection_id),
          ...payload,
        });
        setToast({ msg: "Inspection created", type: "success" });
      }
      setDialogOpen(false);
      load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  // Overdue = Valid_till < today → red; expiring soon (within 30 days) → amber
  const rowClassName = (r: Record<string, unknown>) => {
    const insp = r as unknown as Inspection;
    if (!insp.Valid_till) return "";
    if (insp.Valid_till < today) return "red";
    if (insp.Valid_till <= soonStr) return "amber";
    return "";
  };

  return (
    <div>
      <div className={layoutStyles.pageHeader}>
        <h1 className={layoutStyles.pageTitle}>Inspections</h1>
        <div className={layoutStyles.pageHeaderFilters}>
          <span className={layoutStyles.headerFilter}>All Aircraft ▾</span>
          <span className={layoutStyles.headerFilter}>Last 90 days</span>
        </div>
      </div>
      <DataTable
        columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
        data={data as unknown as Record<string, unknown>[]}
        rowKey={(r) => (r as unknown as Inspection).Inspection_id}
        rowClassName={rowClassName}
        onAdd={openAdd}
        onEdit={(r) => openEdit(r as unknown as Inspection)}
        onDelete={(r) => handleDelete(r as unknown as Inspection)}
        loading={loading}
      />

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Inspection" : "Add Inspection"}
          fields={
            editing
              ? fields.filter((f) => f.name !== "Inspection_id")
              : fields
          }
          values={values}
          onChange={(n, v) => setValues((prev) => ({ ...prev, [n]: v }))}
          onSave={handleSave}
          onClose={() => setDialogOpen(false)}
        />
      )}

      {toast && (
        <Toast message={toast.msg} type={toast.type} onClose={() => setToast(null)} />
      )}
    </div>
  );
}
