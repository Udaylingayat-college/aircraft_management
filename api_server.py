"""
api_server.py

FastAPI bridge for the Aircraft Fleet Management System.
Exposes REST endpoints for all entities and a dashboard summary.
CORS is enabled only for http://localhost:5173 (Vite dev server).

Run with:
    uvicorn api_server:app --reload --port 8000
"""

from datetime import date
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aircraft_management.models import (
    aircraft as aircraft_model,
    asset as asset_model,
    asset_transaction as transaction_model,
    hangar as hangar_model,
    inspection as inspection_model,
    unit as unit_model,
)

app = FastAPI(title="Aircraft Fleet Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class UnitIn(BaseModel):
    Unit_id: int
    Unit_name: str
    Status: Optional[str] = None
    Unit_type: Optional[str] = None
    Location: Optional[str] = None


class UnitUpdate(BaseModel):
    Unit_name: str
    Status: Optional[str] = None
    Unit_type: Optional[str] = None
    Location: Optional[str] = None


class HangarIn(BaseModel):
    Hangar_id: int
    Unit_id: Optional[int] = None
    Hangar_name: str
    Capacity: Optional[int] = None


class HangarUpdate(BaseModel):
    Unit_id: Optional[int] = None
    Hangar_name: str
    Capacity: Optional[int] = None


class AircraftIn(BaseModel):
    Aircraft_id: int
    Registration_no: str
    Aircraft_type: Optional[str] = None
    Unit_id: Optional[int] = None
    Hangar_id: Optional[int] = None
    Status: Optional[str] = None


class AircraftUpdate(BaseModel):
    Registration_no: str
    Aircraft_type: Optional[str] = None
    Unit_id: Optional[int] = None
    Hangar_id: Optional[int] = None
    Status: Optional[str] = None


class AssetIn(BaseModel):
    Asset_id: int
    Asset_name: str
    Category: Optional[str] = None
    blocked_at: Optional[str] = None
    Status: Optional[str] = None
    Condition: Optional[str] = None
    Criticality: Optional[str] = None


class AssetUpdate(BaseModel):
    Asset_name: str
    Category: Optional[str] = None
    blocked_at: Optional[str] = None
    Status: Optional[str] = None
    Condition: Optional[str] = None
    Criticality: Optional[str] = None


class TransactionIn(BaseModel):
    Transaction_id: int
    Issue_date: Optional[date] = None
    Serial_id: Optional[int] = None
    Return_date: Optional[date] = None
    Purpose: Optional[str] = None
    State_after_return: Optional[str] = None
    Unit_id: Optional[int] = None


class TransactionUpdate(BaseModel):
    Issue_date: Optional[date] = None
    Serial_id: Optional[int] = None
    Return_date: Optional[date] = None
    Purpose: Optional[str] = None
    State_after_return: Optional[str] = None
    Unit_id: Optional[int] = None


class InspectionIn(BaseModel):
    Inspection_id: int
    Aircraft_id: Optional[int] = None
    Inspection_type: Optional[str] = None
    Inspection_date: Optional[date] = None
    Valid_till: Optional[date] = None


class InspectionUpdate(BaseModel):
    Aircraft_id: Optional[int] = None
    Inspection_type: Optional[str] = None
    Inspection_date: Optional[date] = None
    Valid_till: Optional[date] = None


# ---------------------------------------------------------------------------
# Helper: serialize rows (convert date objects to ISO strings)
# ---------------------------------------------------------------------------

def _serialize(obj: Any) -> Any:
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def _serialize_row(row: dict) -> dict:
    return {k: _serialize(v) for k, v in row.items()}


def _serialize_rows(rows: list) -> list:
    return [_serialize_row(r) for r in rows]


# ---------------------------------------------------------------------------
# Units
# ---------------------------------------------------------------------------

@app.get("/units")
def list_units():
    return _serialize_rows(unit_model.get_all())


@app.get("/units/{unit_id}")
def get_unit(unit_id: int):
    row = unit_model.get_by_id(unit_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return _serialize_row(row)


@app.post("/units", status_code=201)
def create_unit(body: UnitIn):
    unit_model.create(body.model_dump())
    return unit_model.get_by_id(body.Unit_id)


@app.put("/units/{unit_id}")
def update_unit(unit_id: int, body: UnitUpdate):
    unit_model.update(unit_id, body.model_dump())
    return unit_model.get_by_id(unit_id)


@app.delete("/units/{unit_id}", status_code=204)
def delete_unit(unit_id: int):
    unit_model.delete(unit_id)


# ---------------------------------------------------------------------------
# Hangars
# ---------------------------------------------------------------------------

@app.get("/hangars")
def list_hangars():
    return _serialize_rows(hangar_model.get_all())


@app.get("/hangars/{hangar_id}")
def get_hangar(hangar_id: int):
    row = hangar_model.get_by_id(hangar_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Hangar not found")
    return _serialize_row(row)


@app.post("/hangars", status_code=201)
def create_hangar(body: HangarIn):
    hangar_model.create(body.model_dump())
    return hangar_model.get_by_id(body.Hangar_id)


@app.put("/hangars/{hangar_id}")
def update_hangar(hangar_id: int, body: HangarUpdate):
    hangar_model.update(hangar_id, body.model_dump())
    return hangar_model.get_by_id(hangar_id)


@app.delete("/hangars/{hangar_id}", status_code=204)
def delete_hangar(hangar_id: int):
    hangar_model.delete(hangar_id)


# ---------------------------------------------------------------------------
# Aircraft
# ---------------------------------------------------------------------------

@app.get("/aircraft")
def list_aircraft():
    return _serialize_rows(aircraft_model.get_all())


@app.get("/aircraft/{aircraft_id}")
def get_aircraft(aircraft_id: int):
    row = aircraft_model.get_by_id(aircraft_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return _serialize_row(row)


@app.post("/aircraft", status_code=201)
def create_aircraft(body: AircraftIn):
    aircraft_model.create(body.model_dump())
    return aircraft_model.get_by_id(body.Aircraft_id)


@app.put("/aircraft/{aircraft_id}")
def update_aircraft(aircraft_id: int, body: AircraftUpdate):
    aircraft_model.update(aircraft_id, body.model_dump())
    return aircraft_model.get_by_id(aircraft_id)


@app.delete("/aircraft/{aircraft_id}", status_code=204)
def delete_aircraft(aircraft_id: int):
    aircraft_model.delete(aircraft_id)


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

@app.get("/assets")
def list_assets():
    return _serialize_rows(asset_model.get_all())


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    row = asset_model.get_by_id(asset_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return _serialize_row(row)


@app.post("/assets", status_code=201)
def create_asset(body: AssetIn):
    data = body.model_dump()
    # Map Condition key to match the model expectation
    data["Condition"] = data.pop("Condition", None)
    asset_model.create(data)
    return asset_model.get_by_id(body.Asset_id)


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, body: AssetUpdate):
    asset_model.update(asset_id, body.model_dump())
    return asset_model.get_by_id(asset_id)


@app.delete("/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int):
    asset_model.delete(asset_id)


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------

@app.get("/transactions")
def list_transactions():
    return _serialize_rows(transaction_model.get_all())


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    row = transaction_model.get_by_id(transaction_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return _serialize_row(row)


@app.post("/transactions", status_code=201)
def create_transaction(body: TransactionIn):
    transaction_model.create(body.model_dump())
    return transaction_model.get_by_id(body.Transaction_id)


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, body: TransactionUpdate):
    transaction_model.update(transaction_id, body.model_dump())
    return transaction_model.get_by_id(transaction_id)


@app.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int):
    transaction_model.delete(transaction_id)


# ---------------------------------------------------------------------------
# Inspections
# ---------------------------------------------------------------------------

@app.get("/inspections")
def list_inspections():
    return _serialize_rows(inspection_model.get_all())


@app.get("/inspections/{inspection_id}")
def get_inspection(inspection_id: int):
    row = inspection_model.get_by_id(inspection_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return _serialize_row(row)


@app.post("/inspections", status_code=201)
def create_inspection(body: InspectionIn):
    inspection_model.create(body.model_dump())
    return inspection_model.get_by_id(body.Inspection_id)


@app.put("/inspections/{inspection_id}")
def update_inspection(inspection_id: int, body: InspectionUpdate):
    inspection_model.update(inspection_id, body.model_dump())
    return inspection_model.get_by_id(inspection_id)


@app.delete("/inspections/{inspection_id}", status_code=204)
def delete_inspection(inspection_id: int):
    inspection_model.delete(inspection_id)


# ---------------------------------------------------------------------------
# Dashboard summary
# ---------------------------------------------------------------------------

@app.get("/dashboard/summary")
def dashboard_summary():
    total_aircraft = aircraft_model.get_total_count()
    active_units = unit_model.get_active_count()
    available_assets = asset_model.get_available_count()
    overdue_inspections = inspection_model.get_overdue_count()
    recent_transactions = _serialize_rows(transaction_model.get_recent(5))
    upcoming_inspections = _serialize_rows(inspection_model.get_upcoming(30))

    return {
        "total_aircraft": total_aircraft,
        "active_units": active_units,
        "available_assets": available_assets,
        "overdue_inspections": overdue_inspections,
        "recent_transactions": recent_transactions,
        "upcoming_inspections": upcoming_inspections,
    }
