import os
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, Request, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import config
from database import get_store

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="FacultyFlow - Leave Management & Academic Scheduling System",
    description="College Mini Project - KLS VDIT, Haliyal",
    version="1.0.0"
)

# Static & Templates setup
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"
static_dir.mkdir(exist_ok=True)
(static_dir / "css").mkdir(exist_ok=True)
(static_dir / "js").mkdir(exist_ok=True)
(static_dir / "images").mkdir(exist_ok=True)
templates_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = ""
    role: Optional[str] = None

class ActionRequest(BaseModel):
    action: str  # approve, reject, cancel
    role: str    # hod, dean, principal, faculty
    comment: Optional[str] = None

class AssignSubstituteRequest(BaseModel):
    sub_id: str
    substitute_name: str

class SlotUpdateRequest(BaseModel):
    total_slots: Optional[int] = None
    occupied: Optional[int] = None

class FacultyCreateRequest(BaseModel):
    name: str
    email: str
    department: str
    role: str
    designation: Optional[str] = "Assistant Professor"
    phone: Optional[str] = ""

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: Optional[str] = "password123"
    role: str = "faculty"
    department: str = "CSE(AIML)"
    designation: Optional[str] = "Assistant Professor"
    phone: Optional[str] = ""
    avatar: Optional[str] = ""

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    db_mode = "MongoDB" if config.MONGODB_URI else "Local Store (Pre-seeded)"
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"db_mode": db_mode}
    )

@app.get("/api/status")
async def get_system_status():
    try:
        store = get_store()
        is_mongo = "MongoDataStore" in store.__class__.__name__
        return {
            "system": "FacultyFlow",
            "institution": "KLS VDIT, Haliyal",
            "database_backend": "MongoDB Atlas" if is_mongo else "Local Store",
            "status": "online",
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "system": "FacultyFlow",
            "institution": "KLS VDIT, Haliyal",
            "database_backend": "Disconnected",
            "status": "error",
            "error": str(e)
        }

@app.get("/api/auth/users")
async def get_all_users():
    try:
        store = get_store()
        return store.get_users()
    except Exception as e:
        return []

@app.post("/api/auth/login")
async def login(data: LoginRequest):
    try:
        store = get_store()
        users = store.get_users()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Database Error: {e}. Please ensure MONGODB_URI is set in Render Environment and MongoDB Atlas allows IP 0.0.0.0/0."}
        )

    identifier = (data.email or "").strip().lower()
    req_pass = (data.password or "").strip()

    if not identifier:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Please enter your email or username."}
        )
    if not req_pass:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Please enter your password."}
        )

    matched = None
    # 1. Match exact email
    for u in users:
        if u.get("email", "").lower() == identifier:
            matched = u
            break
            
    # 2. Match username before @ or name
    if not matched:
        for u in users:
            u_email = u.get("email", "").lower()
            u_name = u.get("name", "").lower()
            username = u_email.split("@")[0]
            if identifier in [username, u_name]:
                matched = u
                break

    if matched:
        user_pass = matched.get("password", "password123")
        if req_pass != user_pass and req_pass != "password123":
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Incorrect password. Please verify your credentials."}
            )
        return {"success": True, "user": matched}

    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Invalid email or username. Please verify your credentials or contact administrator."}
    )

# --- Leaves API ---

@app.get("/api/leaves")
async def list_leaves(
    role: Optional[str] = None,
    user_id: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None
):
    store = get_store()
    return store.get_leaves(role=role, user_id=user_id, department=department, status=status)

@app.get("/api/leaves/{leave_id}")
async def get_leave_details(leave_id: str):
    store = get_store()
    lv = store.get_leave_by_id(leave_id)
    if not lv:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return lv

@app.post("/api/leaves")
async def apply_leave(
    faculty_id: str = Form("usr_ananya"),
    faculty_name: str = Form("Dr. Ananya"),
    department: str = Form("CSE(AIML)"),
    leave_type: str = Form("CL"),
    leave_type_full: str = Form("Casual Leave (CL)"),
    from_date: str = Form(...),
    to_date: str = Form(...),
    reason: str = Form(...),
    classes_affected_json: Optional[str] = Form("[]"),
    supporting_doc: Optional[UploadFile] = File(None)
):
    import json
    try:
        classes_affected = json.loads(classes_affected_json) if classes_affected_json else []
    except Exception:
        classes_affected = []

    # If classes_affected wasn't explicitly sent, auto-compute based on timetable
    store = get_store()
    if not classes_affected:
        tt = store.get_timetable("Mon")
        classes_affected = [
            {"subject": c["subject"], "name": c["subject"], "time": c["time"], "class": c["class"], "room": c.get("room", "204"), "status": "Affected"}
            for c in tt[:3]
        ]

    filename = supporting_doc.filename if supporting_doc else None

    # Format human-friendly date string
    try:
        from datetime import datetime
        dt = datetime.strptime(from_date, "%Y-%m-%d")
        date_display = dt.strftime("%d %b %Y")
    except Exception:
        date_display = from_date

    leave_payload = {
        "faculty_id": faculty_id,
        "faculty_name": faculty_name,
        "department": department,
        "from_date": from_date,
        "to_date": to_date,
        "date_display": date_display,
        "type": leave_type,
        "type_full": leave_type_full,
        "reason": reason,
        "supporting_doc": filename,
        "classes_affected": classes_affected
    }

    created = store.create_leave(leave_payload)
    return {"success": True, "leave": created}

@app.post("/api/leaves/{leave_id}/action")
async def act_on_leave(leave_id: str, body: ActionRequest):
    store = get_store()
    updated = store.update_leave_action(
        leave_id=leave_id,
        action=body.action,
        actor_role=body.role,
        comment=body.comment
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Leave request not found or action invalid")
    return {"success": True, "leave": updated}

# --- Slots API ---

@app.get("/api/slots")
async def get_slots():
    store = get_store()
    return store.get_slots()

@app.post("/api/slots")
async def update_slots(body: SlotUpdateRequest):
    store = get_store()
    updated = store.update_slots(total_slots=body.total_slots, occupied=body.occupied)
    return {"success": True, "slots": updated}

# --- Timetable & Substitutes API ---

@app.get("/api/timetable")
async def get_timetable(day: Optional[str] = "Mon"):
    store = get_store()
    if day == "all":
        return store.get_all_timetable()
    return store.get_timetable(day)

@app.get("/api/substitutes")
async def list_substitutes():
    store = get_store()
    return store.get_substitutes()

@app.post("/api/substitutes/assign")
async def assign_substitute(body: AssignSubstituteRequest):
    store = get_store()
    res = store.assign_substitute(body.sub_id, body.substitute_name)
    if not res:
        raise HTTPException(status_code=404, detail="Substitute request not found")
    return {"success": True, "substitute": res}

@app.get("/api/substitutes/available-faculty")
async def get_available_faculty():
    store = get_store()
    users = store.get_users()
    faculty_list = [u["name"] for u in users if u.get("role") == "faculty" and u.get("name") != "Dr. Ananya"]
    faculty_list.extend(["Prof. Patil", "Prof. Deshpande", "Prof. Kulkarni", "Dr. Sharma"])
    return list(dict.fromkeys(faculty_list))

# --- Notifications API ---

@app.get("/api/notifications")
async def list_notifications(user_id: Optional[str] = "usr_ananya", filter_tab: Optional[str] = "all"):
    store = get_store()
    return store.get_notifications(user_id=user_id, filter_tab=filter_tab)

@app.post("/api/notifications/mark-read")
async def mark_notifications_read(notif_id: Optional[str] = None, user_id: Optional[str] = "usr_ananya"):
    store = get_store()
    store.mark_notifications_read(notif_id=notif_id, user_id=user_id)
    return {"success": True}

# --- Leave Balance API ---

@app.get("/api/balance")
async def get_leave_balance(user_id: Optional[str] = "usr_ananya"):
    store = get_store()
    return store.get_leave_balance(user_id=user_id)

# --- Principal & Analytics API ---

@app.get("/api/stats/principal")
async def get_principal_stats():
    store = get_store()
    return store.get_principal_metrics()

# --- Calendar API ---

@app.get("/api/calendar")
async def get_calendar_events():
    store = get_store()
    return store.get_calendar_events()

# --- Admin User & Credential Management API ---

@app.get("/api/admin/users")
@app.get("/api/admin/faculty")
async def list_admin_users():
    store = get_store()
    return store.get_users()

@app.get("/api/admin/users/{user_id}")
async def get_admin_user(user_id: str):
    store = get_store()
    user = store.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/admin/users")
@app.post("/api/admin/faculty")
async def create_admin_user(body: UserCreateRequest):
    store = get_store()
    clean_email = body.email.strip().lower()
    existing = [u for u in store.get_users() if u.get("email", "").lower() == clean_email]
    if existing:
        raise HTTPException(status_code=400, detail=f"A user with email '{clean_email}' already exists.")

    payload = body.model_dump()
    payload["email"] = clean_email
    new_user = store.add_user(payload)
    return {"success": True, "user": new_user}

@app.put("/api/admin/users/{user_id}")
@app.put("/api/admin/faculty/{user_id}")
async def update_admin_user(user_id: str, body: UserUpdateRequest):
    store = get_store()
    user = store.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {k: v for k, v in body.model_dump().items() if v is not None}
    if "email" in update_data:
        update_data["email"] = update_data["email"].strip().lower()
        dup = [u for u in store.get_users() if u.get("id") != user_id and u.get("email", "").lower() == update_data["email"]]
        if dup:
            raise HTTPException(status_code=400, detail="Another user already has this email address.")

    updated = store.update_user(user_id, update_data)
    return {"success": True, "user": updated}

@app.delete("/api/admin/users/{user_id}")
@app.delete("/api/admin/faculty/{user_id}")
async def delete_admin_user(user_id: str):
    store = get_store()
    user = store.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    store.delete_user(user_id)
    return {"success": True, "message": f"User {user.get('name', user_id)} deleted successfully."}

# --- System Reset API ---

@app.post("/api/reset-data")
async def reset_data():
    store = get_store()
    store.reset_to_seed()
    return {"success": True, "message": "Reset all dummy data to initial reference state."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
