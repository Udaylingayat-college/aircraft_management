import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import type { Asset } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { StatusBadge } from "../components/StatusBadge";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Asset>[] = [
  { key: "Asset_id", header: "ID" },
  { key: "Asset_name", header: "Name" },
  { key: "Category", header: "Category" },
  { key: "blocked_at", header: "Location" },
  {
    key: "Status",
    header: "Status",
    render: (row) => <StatusBadge value={row.Status} />,
  },
  { key: "Condition", header: "Condition" },
  {
    key: "Criticality",
    header: "Criticality",
    render: (row) => <StatusBadge value={row.Criticality} />,
  },
];

const FIELDS: FieldDef[] = [
  { name: "Asset_id", label: "Asset ID", type: "number", required: true },
  { name: "Asset_name", label: "Name", required: true },
  { name: "Category", label: "Category" },
  { name: "blocked_at", label: "Location / Blocked At" },
  {
    name: "Status",
    label: "Status",
    type: "select",
    options: ["Available", "Issued", "Under Repair", "Decommissioned"],
  },
  {
    name: "Condition",
    label: "Condition",
    type: "select",
    options: ["Excellent", "Good", "Fair", "Poor", "Damaged"],
  },
  {
    name: "Criticality",
    label: "Criticality",
    type: "select",
    options: ["Critical", "High", "Medium", "Low"],
  },
];

const EMPTY: Record<string, string> = {
  Asset_id: "",
  Asset_name: "",
  Category: "",
  blocked_at: "",
  Status: "",
  Condition: "",
  Criticality: "",
};

export function Assets() {
  const [data, setData] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Asset | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);

  const load = useCallback(() => {
    setLoading(true);
    api.getAssets().then(setData).finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Asset) => {
    setEditing(row);
    setValues({
      Asset_id: String(row.Asset_id),
      Asset_name: row.Asset_name,
      Category: row.Category ?? "",
      blocked_at: row.blocked_at ?? "",
      Status: row.Status ?? "",
      Condition: row.Condition ?? "",
      Criticality: row.Criticality ?? "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Asset) => {
    if (!confirm(`Delete asset "${row.Asset_name}"?`)) return;
    try {
      await api.deleteAsset(row.Asset_id);
      setToast({ msg: "Asset deleted", type: "success" });
      load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      if (editing) {
        await api.updateAsset(editing.Asset_id, {
          Asset_name: values.Asset_name,
          Category: values.Category || null,
          blocked_at: values.blocked_at || null,
          Status: values.Status || null,
          Condition: values.Condition || null,
          Criticality: values.Criticality || null,
        });
        setToast({ msg: "Asset updated", type: "success" });
      } else {
        await api.createAsset({
          Asset_id: Number(values.Asset_id),
          Asset_name: values.Asset_name,
          Category: values.Category || null,
          blocked_at: values.blocked_at || null,
          Status: values.Status || null,
          Condition: values.Condition || null,
          Criticality: values.Criticality || null,
        });
        setToast({ msg: "Asset created", type: "success" });
      }
      setDialogOpen(false);
      load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  return (
    <div>
      <h1 className={layoutStyles.pageTitle}>Assets</h1>
      <div className={layoutStyles.card}>
        <DataTable
          columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
          data={data as unknown as Record<string, unknown>[]}
          rowKey={(r) => (r as unknown as Asset).Asset_id}
          filters={[
            {
              key: "Status",
              label: "All Statuses",
              options: ["Available", "Issued", "Under Repair", "Decommissioned"],
            },
            {
              key: "Criticality",
              label: "All Criticality",
              options: ["Critical", "High", "Medium", "Low"],
            },
          ]}
          rowClassName={(r) => {
            const asset = r as unknown as Asset;
            if (asset.Criticality === "Critical") return "red";
            if (asset.Criticality === "High") return "amber";
            return "";
          }}
          onAdd={openAdd}
          onEdit={(r) => openEdit(r as unknown as Asset)}
          onDelete={(r) => handleDelete(r as unknown as Asset)}
          loading={loading}
        />
      </div>

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Asset" : "Add Asset"}
          fields={editing ? FIELDS.filter((f) => f.name !== "Asset_id") : FIELDS}
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
