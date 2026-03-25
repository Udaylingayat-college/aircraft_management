import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Hangar, Unit } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { ProgressBar } from "../components/ProgressBar";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Hangar & { aircraft_count: number }>[] = [
  { key: "Hangar_id", header: "ID" },
  { key: "Hangar_name", header: "Name" },
  { key: "Unit_name", header: "Unit" },
  { key: "Capacity", header: "Capacity" },
  {
    key: "aircraft_count",
    header: "Usage",
    render: (row) => (
      <ProgressBar value={row.aircraft_count ?? 0} max={row.Capacity ?? 1} />
    ),
  },
];

const EMPTY: Record<string, string> = {
  Hangar_id: "",
  Unit_id: "",
  Hangar_name: "",
  Capacity: "",
};

export function Hangars() {
  const [data, setData] = useState<(Hangar & { aircraft_count: number })[]>([]);
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Hangar | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [hangars, unitList] = await Promise.all([api.getHangars(), api.getUnits()]);
      setUnits(unitList);
      // Count aircraft per hangar
      const aircraftList = await api.getAircraft();
      const countMap: Record<number, number> = {};
      aircraftList.forEach((a) => {
        if (a.Hangar_id != null) {
          countMap[a.Hangar_id] = (countMap[a.Hangar_id] ?? 0) + 1;
        }
      });
      setData(
        hangars.map((h) => ({ ...h, aircraft_count: countMap[h.Hangar_id] ?? 0 }))
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const unitOptions = units.map((u) => String(u.Unit_id));

  const fields: FieldDef[] = [
    { name: "Hangar_id", label: "Hangar ID", type: "number", required: true },
    { name: "Unit_id", label: "Unit ID", type: "select", options: unitOptions },
    { name: "Hangar_name", label: "Name", required: true },
    { name: "Capacity", label: "Capacity", type: "number" },
  ];

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Hangar) => {
    setEditing(row);
    setValues({
      Hangar_id: String(row.Hangar_id),
      Unit_id: row.Unit_id != null ? String(row.Unit_id) : "",
      Hangar_name: row.Hangar_name,
      Capacity: row.Capacity != null ? String(row.Capacity) : "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Hangar) => {
    if (!confirm(`Delete hangar "${row.Hangar_name}"?`)) return;
    try {
      await api.deleteHangar(row.Hangar_id);
      setToast({ msg: "Hangar deleted", type: "success" });
      load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      if (editing) {
        await api.updateHangar(editing.Hangar_id, {
          Unit_id: values.Unit_id ? Number(values.Unit_id) : null,
          Hangar_name: values.Hangar_name,
          Capacity: values.Capacity ? Number(values.Capacity) : null,
        });
        setToast({ msg: "Hangar updated", type: "success" });
      } else {
        await api.createHangar({
          Hangar_id: Number(values.Hangar_id),
          Unit_id: values.Unit_id ? Number(values.Unit_id) : null,
          Hangar_name: values.Hangar_name,
          Capacity: values.Capacity ? Number(values.Capacity) : null,
        });
        setToast({ msg: "Hangar created", type: "success" });
      }
      setDialogOpen(false);
      load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  return (
    <div>
      <h1 className={layoutStyles.pageTitle}>Hangars</h1>
      <div className={layoutStyles.card}>
        <DataTable
          columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
          data={data as unknown as Record<string, unknown>[]}
          rowKey={(r) => (r as unknown as Hangar).Hangar_id}
          onAdd={openAdd}
          onEdit={(r) => openEdit(r as unknown as Hangar)}
          onDelete={(r) => handleDelete(r as unknown as Hangar)}
          loading={loading}
        />
      </div>

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Hangar" : "Add Hangar"}
          fields={editing ? fields.filter((f) => f.name !== "Hangar_id") : fields}
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
