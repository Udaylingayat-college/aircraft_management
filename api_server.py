"""
api_server.py

FastAPI bridge for the Aircraft Fleet Management System.
Exposes REST endpoints for all entities and a dashboard summary.
CORS is enabled only for http://localhost:5173 (Vite dev server).

Run with:
    uvicorn api_server:app --reload --port 8000
"""

from datetime import date, datetime, timedelta
from typing import Any, Optional

import bcrypt
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel

from aircraft_management.db.connection import get_connection
from aircraft_management.models import (
    aircraft as aircraft_model,
    asset as asset_model,
    asset_transaction as transaction_model,
    hangar as hangar_model,
    inspection as inspection_model,
    unit as unit_model,
)

app = FastAPI(title="Aircraft Fleet Management API")

SECRET_KEY = "aircraft_fleet_secret_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

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


class SignupIn(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = "viewer"


class LoginIn(BaseModel):
    email: str
    password: str


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


def _fetch_all(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def _fetch_one(query: str, params: tuple = ()) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def _execute(query: str, params: tuple = ()) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def _create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _extract_bearer_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    return authorization.split(" ", 1)[1].strip()


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.post("/auth/signup")
def signup(body: SignupIn):
    existing = _fetch_one("SELECT id FROM users WHERE email = %s", (body.email,))
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    password_hash = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    role = body.role if body.role in {"admin", "engineer", "viewer"} else "viewer"

    _execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (body.full_name, body.email, password_hash, role),
    )
    return {"message": "User created"}


@app.post("/auth/login")
def login(body: LoginIn):
    user = _fetch_one(
        "SELECT id, full_name, email, password_hash, role FROM users WHERE email = %s",
        (body.email,),
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    valid = bcrypt.checkpw(body.password.encode("utf-8"), user["password_hash"].encode("utf-8"))
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = _create_access_token(user["id"])
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"],
        },
    }


@app.get("/auth/me")
def me(authorization: Optional[str] = Header(default=None)):
    token = _extract_bearer_token(authorization)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub", "0"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token") from None

    user = _fetch_one(
        "SELECT id, full_name, email, role FROM users WHERE id = %s",
        (user_id,),
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


# ---------------------------------------------------------------------------
# Units
# ---------------------------------------------------------------------------

@app.get("/units")
def list_units(status: Optional[str] = None):
    query = "SELECT * FROM Unit"
    params: list[Any] = []
    if status:
        query += " WHERE Status = %s"
        params.append(status)
    query += " ORDER BY Unit_id"
    return _serialize_rows(_fetch_all(query, tuple(params)))


@app.get("/units/statuses")
def list_unit_statuses():
    rows = _fetch_all(
        "SELECT DISTINCT Status AS status FROM Unit WHERE Status IS NOT NULL ORDER BY Status"
    )
    return [row["status"] for row in rows if row.get("status")]


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
def list_hangars(unit_id: Optional[int] = None):
    query = (
        "SELECT h.*, u.Unit_name "
        "FROM Hangar h "
        "LEFT JOIN Unit u ON h.Unit_id = u.Unit_id"
    )
    params: list[Any] = []
    if unit_id is not None:
        query += " WHERE h.Unit_id = %s"
        params.append(unit_id)
    query += " ORDER BY h.Hangar_id"
    return _serialize_rows(_fetch_all(query, tuple(params)))


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
def list_aircraft(unit_id: Optional[int] = None, status: Optional[str] = None):
    query = (
        "SELECT a.*, u.Unit_name, h.Hangar_name "
        "FROM Aircraft a "
        "LEFT JOIN Unit u ON a.Unit_id = u.Unit_id "
        "LEFT JOIN Hangar h ON a.Hangar_id = h.Hangar_id"
    )
    where_clauses = []
    params: list[Any] = []
    if unit_id is not None:
        where_clauses.append("a.Unit_id = %s")
        params.append(unit_id)
    if status:
        where_clauses.append("a.Status = %s")
        params.append(status)
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY a.Aircraft_id"
    return _serialize_rows(_fetch_all(query, tuple(params)))


@app.get("/aircraft/statuses")
def list_aircraft_statuses():
    rows = _fetch_all(
        "SELECT DISTINCT Status AS status FROM Aircraft WHERE Status IS NOT NULL ORDER BY Status"
    )
    return [row["status"] for row in rows if row.get("status")]


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
def list_assets(criticality: Optional[str] = None, aircraft_id: Optional[int] = None):
    query = "SELECT * FROM Asset"
    where_clauses = []
    params: list[Any] = []
    if criticality:
        where_clauses.append("Criticality = %s")
        params.append(criticality)
    if aircraft_id is not None:
        where_clauses.append("Aircraft_id = %s")
        params.append(aircraft_id)
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY Asset_id"
    return _serialize_rows(_fetch_all(query, tuple(params)))


@app.get("/assets/criticalities")
def list_asset_criticalities():
    rows = _fetch_all(
        "SELECT DISTINCT Criticality AS criticality "
        "FROM Asset WHERE Criticality IS NOT NULL ORDER BY Criticality"
    )
    return [row["criticality"] for row in rows if row.get("criticality")]


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
def list_transactions(aircraft_id: Optional[int] = None, status: Optional[str] = None):
    query = (
        "SELECT t.*, a.Asset_name, u.Unit_name "
        "FROM Asset_Transaction t "
        "LEFT JOIN Asset a ON t.Serial_id = a.Asset_id "
        "LEFT JOIN Unit u ON t.Unit_id = u.Unit_id"
    )
    where_clauses = []
    params: list[Any] = []
    if aircraft_id is not None:
        where_clauses.append("t.Aircraft_id = %s")
        params.append(aircraft_id)
    if status == "issued":
        where_clauses.append("t.Return_date IS NULL")
    elif status == "returned":
        where_clauses.append("t.Return_date IS NOT NULL")
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY t.Issue_date DESC"
    return _serialize_rows(_fetch_all(query, tuple(params)))


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
def list_inspections(aircraft_id: Optional[int] = None, status: Optional[str] = None):
    query = (
        "SELECT ir.*, a.Registration_no "
        "FROM Inspection_Record ir "
        "LEFT JOIN Aircraft a ON ir.Aircraft_id = a.Aircraft_id"
    )
    where_clauses = []
    params: list[Any] = []
    if aircraft_id is not None:
        where_clauses.append("ir.Aircraft_id = %s")
        params.append(aircraft_id)
    if status == "overdue":
        where_clauses.append("ir.Valid_till < CURDATE()")
    elif status == "expiring":
        where_clauses.append(
            "ir.Valid_till BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)"
        )
    elif status == "ok":
        where_clauses.append("ir.Valid_till > DATE_ADD(CURDATE(), INTERVAL 30 DAY)")
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY ir.Inspection_date DESC"
    return _serialize_rows(_fetch_all(query, tuple(params)))


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
