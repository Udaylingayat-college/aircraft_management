import { useCallback, useEffect, useState } from "react";
import client, { api } from "../api/client";
import type { Transaction, Asset, Unit, Aircraft } from "../api/client";
import { DataTable } from "../components/DataTable";
import type { Column } from "../components/DataTable";
import { FormDialog } from "../components/FormDialog";
import type { FieldDef } from "../components/FormDialog";
import { Toast } from "../components/Toast";
import type { ToastType } from "../components/Toast";
import layoutStyles from "../components/Layout.module.css";

const COLUMNS: Column<Transaction>[] = [
  { key: "Transaction_id", header: "ID" },
  { key: "Asset_name", header: "Asset" },
  { key: "Unit_name", header: "Unit" },
  { key: "Issue_date", header: "Issue Date" },
  { key: "Return_date", header: "Return Date" },
  { key: "Purpose", header: "Purpose" },
  { key: "State_after_return", header: "State After Return" },
];

const EMPTY: Record<string, string> = {
  Transaction_id: "",
  Issue_date: "",
  Serial_id: "",
  Return_date: "",
  Purpose: "",
  State_after_return: "",
  Unit_id: "",
};

export function Transactions() {
  const [data, setData] = useState<Transaction[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [units, setUnits] = useState<Unit[]>([]);
  const [aircraft, setAircraft] = useState<Aircraft[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Transaction | null>(null);
  const [values, setValues] = useState<Record<string, string>>(EMPTY);
  const [toast, setToast] = useState<{ msg: string; type: ToastType } | null>(null);
  const [aircraftFilter, setAircraftFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const load = useCallback(async (selectedAircraft: string = aircraftFilter, selectedStatus: string = statusFilter) => {
    setLoading(true);
    try {
      const params: Record<string, string | number> = {};
      if (selectedAircraft) params.aircraft_id = Number(selectedAircraft);
      if (selectedStatus) params.status = selectedStatus;

      const [txnsResp, assetList, unitList] = await Promise.all([
        client.get<Transaction[]>("/transactions", { params: Object.keys(params).length ? params : undefined }),
        api.getAssets(),
        api.getUnits(),
      ]);
      setData(txnsResp.data);
      setAssets(assetList);
      setUnits(unitList);
    } finally {
      setLoading(false);
    }
  }, [aircraftFilter, statusFilter]);

  useEffect(() => {
    api.getAircraft().then(setAircraft);
  }, []);

  useEffect(() => {
    void load(aircraftFilter, statusFilter);
  }, [aircraftFilter, load, statusFilter]);

  const fields: FieldDef[] = [
    { name: "Transaction_id", label: "Transaction ID", type: "number", required: true },
    { name: "Issue_date", label: "Issue Date", type: "date" },
    {
      name: "Serial_id",
      label: "Asset",
      type: "select",
      options: assets.map((a) => String(a.Asset_id)),
    },
    { name: "Return_date", label: "Return Date", type: "date" },
    { name: "Purpose", label: "Purpose" },
    { name: "State_after_return", label: "State After Return" },
    {
      name: "Unit_id",
      label: "Unit",
      type: "select",
      options: units.map((u) => String(u.Unit_id)),
    },
  ];

  const openAdd = () => {
    setEditing(null);
    setValues(EMPTY);
    setDialogOpen(true);
  };

  const openEdit = (row: Transaction) => {
    setEditing(row);
    setValues({
      Transaction_id: String(row.Transaction_id),
      Issue_date: row.Issue_date ?? "",
      Serial_id: row.Serial_id != null ? String(row.Serial_id) : "",
      Return_date: row.Return_date ?? "",
      Purpose: row.Purpose ?? "",
      State_after_return: row.State_after_return ?? "",
      Unit_id: row.Unit_id != null ? String(row.Unit_id) : "",
    });
    setDialogOpen(true);
  };

  const handleDelete = async (row: Transaction) => {
    if (!confirm(`Delete transaction #${row.Transaction_id}?`)) return;
    try {
      await api.deleteTransaction(row.Transaction_id);
      setToast({ msg: "Transaction deleted", type: "success" });
      await load();
    } catch {
      setToast({ msg: "Delete failed", type: "error" });
    }
  };

  const handleSave = async () => {
    try {
      const payload = {
        Issue_date: values.Issue_date || null,
        Serial_id: values.Serial_id ? Number(values.Serial_id) : null,
        Return_date: values.Return_date || null,
        Purpose: values.Purpose || null,
        State_after_return: values.State_after_return || null,
        Unit_id: values.Unit_id ? Number(values.Unit_id) : null,
      };
      if (editing) {
        await api.updateTransaction(editing.Transaction_id, payload);
        setToast({ msg: "Transaction updated", type: "success" });
      } else {
        await api.createTransaction({
          Transaction_id: Number(values.Transaction_id),
          ...payload,
        });
        setToast({ msg: "Transaction created", type: "success" });
      }
      setDialogOpen(false);
      await load();
    } catch {
      setToast({ msg: "Save failed", type: "error" });
    }
  };

  const rowClassName = (r: Record<string, unknown>) => {
    const txn = r as unknown as Transaction;
    return !txn.Return_date ? "amber" : "";
  };

  return (
    <div>
      <div className={layoutStyles.pageHeader}>
        <h1 className={layoutStyles.pageTitle}>Transactions</h1>
        <div className={layoutStyles.pageHeaderFilters}>
          <select
            className={layoutStyles.headerSelect}
            value={aircraftFilter}
            onChange={(e) => setAircraftFilter(e.target.value)}
          >
            <option value="">All Aircraft</option>
            {aircraft.map((aircraftItem) => (
              <option key={aircraftItem.Aircraft_id} value={aircraftItem.Aircraft_id}>{aircraftItem.Registration_no}</option>
            ))}
          </select>
          <select
            className={layoutStyles.headerSelect}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Status</option>
            <option value="issued">issued</option>
            <option value="returned">returned</option>
          </select>
        </div>
      </div>
      <DataTable
        columns={COLUMNS as unknown as Column<Record<string, unknown>>[]}
        data={data as unknown as Record<string, unknown>[]}
        rowKey={(r) => (r as unknown as Transaction).Transaction_id}
        rowClassName={rowClassName}
        onAdd={openAdd}
        onEdit={(r) => openEdit(r as unknown as Transaction)}
        onDelete={(r) => handleDelete(r as unknown as Transaction)}
        loading={loading}
      />

      {dialogOpen && (
        <FormDialog
          title={editing ? "Edit Transaction" : "Add Transaction"}
          fields={
            editing
              ? fields.filter((f) => f.name !== "Transaction_id")
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
