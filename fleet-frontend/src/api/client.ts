import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("afm_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default client;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface Unit {
  Unit_id: number;
  Unit_name: string;
  Status: string | null;
  Unit_type: string | null;
  Location: string | null;
}

export interface Hangar {
  Hangar_id: number;
  Unit_id: number | null;
  Hangar_name: string;
  Capacity: number | null;
  Unit_name?: string | null;
  aircraft_count?: number;
}

export interface Aircraft {
  Aircraft_id: number;
  Registration_no: string;
  Aircraft_type: string | null;
  Unit_id: number | null;
  Hangar_id: number | null;
  Status: string | null;
  Unit_name?: string | null;
  Hangar_name?: string | null;
}

export interface Asset {
  Asset_id: number;
  Asset_name: string;
  Category: string | null;
  blocked_at: string | null;
  Status: string | null;
  Condition: string | null;
  Criticality: string | null;
}

export interface Transaction {
  Transaction_id: number;
  Issue_date: string | null;
  Serial_id: number | null;
  Return_date: string | null;
  Purpose: string | null;
  State_after_return: string | null;
  Unit_id: number | null;
  Asset_name?: string | null;
  Unit_name?: string | null;
}

export interface Inspection {
  Inspection_id: number;
  Aircraft_id: number | null;
  Inspection_type: string | null;
  Inspection_date: string | null;
  Valid_till: string | null;
  Registration_no?: string | null;
}

export interface DashboardSummary {
  total_aircraft: number;
  active_units: number;
  available_assets: number;
  overdue_inspections: number;
  recent_transactions: Transaction[];
  upcoming_inspections: Inspection[];
}

// ---------------------------------------------------------------------------
// API helpers
// ---------------------------------------------------------------------------

export const api = {
  // Units
  getUnits: () => client.get<Unit[]>("/units").then((r) => r.data),
  getUnit: (id: number) => client.get<Unit>(`/units/${id}`).then((r) => r.data),
  createUnit: (data: Omit<Unit, never>) => client.post<Unit>("/units", data).then((r) => r.data),
  updateUnit: (id: number, data: Partial<Unit>) =>
    client.put<Unit>(`/units/${id}`, data).then((r) => r.data),
  deleteUnit: (id: number) => client.delete(`/units/${id}`),

  // Hangars
  getHangars: () => client.get<Hangar[]>("/hangars").then((r) => r.data),
  getHangar: (id: number) => client.get<Hangar>(`/hangars/${id}`).then((r) => r.data),
  createHangar: (data: Omit<Hangar, "Unit_name" | "aircraft_count">) =>
    client.post<Hangar>("/hangars", data).then((r) => r.data),
  updateHangar: (id: number, data: Partial<Hangar>) =>
    client.put<Hangar>(`/hangars/${id}`, data).then((r) => r.data),
  deleteHangar: (id: number) => client.delete(`/hangars/${id}`),

  // Aircraft
  getAircraft: () => client.get<Aircraft[]>("/aircraft").then((r) => r.data),
  getAircraftById: (id: number) =>
    client.get<Aircraft>(`/aircraft/${id}`).then((r) => r.data),
  createAircraft: (data: Omit<Aircraft, "Unit_name" | "Hangar_name">) =>
    client.post<Aircraft>("/aircraft", data).then((r) => r.data),
  updateAircraft: (id: number, data: Partial<Aircraft>) =>
    client.put<Aircraft>(`/aircraft/${id}`, data).then((r) => r.data),
  deleteAircraft: (id: number) => client.delete(`/aircraft/${id}`),

  // Assets
  getAssets: () => client.get<Asset[]>("/assets").then((r) => r.data),
  getAsset: (id: number) => client.get<Asset>(`/assets/${id}`).then((r) => r.data),
  createAsset: (data: Asset) => client.post<Asset>("/assets", data).then((r) => r.data),
  updateAsset: (id: number, data: Partial<Asset>) =>
    client.put<Asset>(`/assets/${id}`, data).then((r) => r.data),
  deleteAsset: (id: number) => client.delete(`/assets/${id}`),

  // Transactions
  getTransactions: () =>
    client.get<Transaction[]>("/transactions").then((r) => r.data),
  getTransaction: (id: number) =>
    client.get<Transaction>(`/transactions/${id}`).then((r) => r.data),
  createTransaction: (data: Transaction) =>
    client.post<Transaction>("/transactions", data).then((r) => r.data),
  updateTransaction: (id: number, data: Partial<Transaction>) =>
    client.put<Transaction>(`/transactions/${id}`, data).then((r) => r.data),
  deleteTransaction: (id: number) => client.delete(`/transactions/${id}`),

  // Inspections
  getInspections: () =>
    client.get<Inspection[]>("/inspections").then((r) => r.data),
  getInspection: (id: number) =>
    client.get<Inspection>(`/inspections/${id}`).then((r) => r.data),
  createInspection: (data: Inspection) =>
    client.post<Inspection>("/inspections", data).then((r) => r.data),
  updateInspection: (id: number, data: Partial<Inspection>) =>
    client.put<Inspection>(`/inspections/${id}`, data).then((r) => r.data),
  deleteInspection: (id: number) => client.delete(`/inspections/${id}`),

  // Dashboard
  getDashboardSummary: () =>
    client.get<DashboardSummary>("/dashboard/summary").then((r) => r.data),
};
