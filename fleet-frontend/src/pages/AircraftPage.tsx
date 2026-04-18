import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Aircraft, Unit, Hangar } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { StatusBadge } from "../components/StatusBadge";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Aircraft>[] = [
  { key: "Aircraft_id", header: "ID" },
  { key: "Registration_no", header: "Registration" },
  { key: "Aircraft_type", header: "Type" },
  { key: "Unit_name", header: "Unit" },
  { key: "Hangar_name", header: "Hangar" },
  {
    key: "Status",
    header: "Status",
    render: (row) => <StatusBadge value={row.Status} />,
  },
];

const EMPTY: Record<string, string> = {
  Aircraft_id: "",
  Registration_no: "",
  Aircraft_type: "",
  Unit_id: "",
  Hangar_id: "",
  Status: "",
};

const STATUS_OPTIONS = ["Operational", "Under Maintenance", "Grounded", "In Transit"];

export function AircraftPage() {
  const [data, setData] = useState<Aircraft[]>([]);
  const [units, setUnits] = useState<Unit[]>([]);
  const [hangars, setHangars] = useState<Hangar[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Aircraft | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [aircraft, unitList, hangarList] = await Promise.all([
        api.getAircraft(),
        api.getUnits(),
        api.getHangars(),
      ]);
      setData(aircraft);
      setUnits(unitList);
      setHangars(hangarList);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const fields: FieldDef[] = [
    { name: "Aircraft_id", label: "Aircraft ID", type: "number", required: true },
    { name: "Registration_no", label: "Registration No", required: true },
    { name: "Aircraft_type", label: "Type" },
    {
      name: "Unit_id",
      label: "Unit",
      type: "select",
      options: units.map((u) => String(u.Unit_id)),
    },
    {
      name: "Hangar_id",
      label: "Hangar",
      type: "select",
      options: hangars.map((h) => String(h.Hangar_id)),
    },
    {
      name: "Status",
      label: "Status",
      type: "select",
      options: STATUS_OPTIONS,
    },
  ];

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Aircraft) => {
    setEditing(row);
    setValues({
      Aircraft_id: String(row.Aircraft_id),
      Registration_no: row.Registration_no,
      Aircraft_type: row.Aircraft_type ?? "",
      Unit_id: row.Unit_id != null ? String(row.Unit_id) : "",
      Hangar_id: row.Hangar_id != null ? String(row.Hangar_id) : "",
      Status: row.Status ?? "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Aircraft) => {
    if (!confirm(`Delete aircraft "${row.Registration_no}"?`)) return;
    try {
      await api.deleteAircraft(row.Aircraft_id);
      setToast({ msg: "Aircraft deleted", type: "success" });
      load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      if (editing) {
        await api.updateAircraft(editing.Aircraft_id, {
          Registration_no: values.Registration_no,
          Aircraft_type: values.Aircraft_type || null,
          Unit_id: values.Unit_id ? Number(values.Unit_id) : null,
          Hangar_id: values.Hangar_id ? Number(values.Hangar_id) : null,
          Status: values.Status || null,
        });
        setToast({ msg: "Aircraft updated", type: "success" });
      } else {
        await api.createAircraft({
          Aircraft_id: Number(values.Aircraft_id),
          Registration_no: values.Registration_no,
          Aircraft_type: values.Aircraft_type || null,
          Unit_id: values.Unit_id ? Number(values.Unit_id) : null,
          Hangar_id: values.Hangar_id ? Number(values.Hangar_id) : null,
          Status: values.Status || null,
        });
        setToast({ msg: "Aircraft created", type: "success" });
      }
      setDialogOpen(false);
      load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  const unitNames = units.map((u) => u.Unit_name);
  const statusOptions = STATUS_OPTIONS;

  return (
    <div>
      <div className={layoutStyles.pageHeader}>
        <h1 className={layoutStyles.pageTitle}>Aircraft</h1>
        <div className={layoutStyles.pageHeaderFilters}>
          <span className={layoutStyles.headerFilter}>All Hangars ▾</span>
          <span className={layoutStyles.headerFilter}>Last 90 days</span>
        </div>
      </div>
      <DataTable
        columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
        data={data as unknown as Record<string, unknown>[]}
        rowKey={(r) => (r as unknown as Aircraft).Aircraft_id}
        filters={[
          { key: "Unit_name", label: "All Units", options: unitNames },
          { key: "Status", label: "All Statuses", options: statusOptions },
        ]}
        onAdd={openAdd}
        onEdit={(r) => openEdit(r as unknown as Aircraft)}
        onDelete={(r) => handleDelete(r as unknown as Aircraft)}
        loading={loading}
      />

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Aircraft" : "Add Aircraft"}
          fields={editing ? fields.filter((f) => f.name !== "Aircraft_id") : fields}
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
