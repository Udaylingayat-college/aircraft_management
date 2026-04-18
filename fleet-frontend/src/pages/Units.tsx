import { useCallback, useEffect, useState } from "react";
import client, { api } from "../api/client";
import type { Unit } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { StatusBadge } from "../components/StatusBadge";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Unit>[] = [
  { key: "Unit_id", header: "ID" },
  { key: "Unit_name", header: "Name" },
  {
    key: "Status",
    header: "Status",
    render: (row) => <StatusBadge value={row.Status} />,
  },
  { key: "Unit_type", header: "Type" },
  { key: "Location", header: "Location" },
];

const FIELDS: FieldDef[] = [
  { name: "Unit_id", label: "Unit ID", type: "number", required: true },
  { name: "Unit_name", label: "Name", required: true },
  {
    name: "Status",
    label: "Status",
    type: "select",
    options: ["Active", "Inactive"],
  },
  {
    name: "Unit_type",
    label: "Type",
    type: "select",
    options: ["Fighter", "Transport", "Training", "Helicopter", "Reconnaissance"],
  },
  { name: "Location", label: "Location" },
];

const EMPTY: Record<string, string> = {
  Unit_id: "",
  Unit_name: "",
  Status: "",
  Unit_type: "",
  Location: "",
};

export function Units() {
  const [data, setData] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Unit | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);
  const [statusFilter, setStatusFilter] = useState("");
  const [statusOptions, setStatusOptions] = useState<string[]>([]);

  const load = useCallback(async (selectedStatus: string = statusFilter) => {
    setLoading(true);
    try {
      const params = selectedStatus ? { status: selectedStatus } : undefined;
      const { data: units } = await client.get<Unit[]>("/units", { params });
      setData(units);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    client.get<string[]>("/units/statuses").then((response) => setStatusOptions(response.data));
  }, []);

  useEffect(() => {
    void load(statusFilter);
  }, [load, statusFilter]);

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Unit) => {
    setEditing(row);
    setValues({
      Unit_id: String(row.Unit_id),
      Unit_name: row.Unit_name,
      Status: row.Status ?? "",
      Unit_type: row.Unit_type ?? "",
      Location: row.Location ?? "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Unit) => {
    if (!confirm(`Delete unit "${row.Unit_name}"?`)) return;
    try {
      await api.deleteUnit(row.Unit_id);
      setToast({ msg: "Unit deleted", type: "success" });
      await load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      if (editing) {
        await api.updateUnit(editing.Unit_id, {
          Unit_name: values.Unit_name,
          Status: values.Status || null,
          Unit_type: values.Unit_type || null,
          Location: values.Location || null,
        });
        setToast({ msg: "Unit updated", type: "success" });
      } else {
        await api.createUnit({
          Unit_id: Number(values.Unit_id),
          Unit_name: values.Unit_name,
          Status: values.Status || null,
          Unit_type: values.Unit_type || null,
          Location: values.Location || null,
        });
        setToast({ msg: "Unit created", type: "success" });
      }
      setDialogOpen(false);
      await load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  return (
    <div>
      <div className={layoutStyles.pageHeader}>
        <h1 className={layoutStyles.pageTitle}>Units</h1>
        <div className={layoutStyles.pageHeaderFilters}>
          <select
            className={layoutStyles.headerSelect}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Status</option>
            {statusOptions.map((status) => (
              <option key={status} value={status}>{status}</option>
            ))}
          </select>
        </div>
      </div>
      <DataTable
        columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
        data={data as unknown as Record<string, unknown>[]}
        rowKey={(r) => (r as unknown as Unit).Unit_id}
        onAdd={openAdd}
        onEdit={(r) => openEdit(r as unknown as Unit)}
        onDelete={(r) => handleDelete(r as unknown as Unit)}
        loading={loading}
      />

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Unit" : "Add Unit"}
          fields={editing ? FIELDS.filter((f) => f.name !== "Unit_id") : FIELDS}
          values={values}
          onChange={(n, v) => setValues((prev) => ({ ...prev, [n]: v }))}
          onSave={handleSave}
          onClose={() => setDialogOpen(false)}
        />
      )}

      {toast && (
        <Toast
          message={toast.msg}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
