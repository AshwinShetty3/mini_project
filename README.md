# FacultyFlow — Leave Management & Academic Scheduling System

> **College Mini Project**  
> **Institution:** KLS Vishwanathrao Deshpande Institute of Technology (KLS VDIT), Haliyal  
> **Tagline:** *Simpler Approvals · Smarter Scheduling · Better Academic Flow*

---

## 🌟 Overview

**FacultyFlow** is an end-to-end academic leave management and scheduling system built with **Python (FastAPI)** and a modern, responsive web frontend. It is designed specifically to handle college department quotas, multi-stage approval workflows, lecture clash detection, substitute teacher allocation, and real-time waiting queues.

This project comes pre-configured with **rich, realistic dummy data** matching the institution's real structure (CSE-AIML, ECE, ME, Dean, Principal, etc.) and features an instant toggle/adapter for **MongoDB**.

---

## 📸 Complete 16-Screen System

1. **Login Page:** Institutional login with college photo hero side, FacultyFlow branding, and one-click demo login pills.
2. **Faculty Dashboard:** Stat cards (Pending, Approved, Rejected, Classes Affected), circular radial gauge for Leave Slot Availability (1/3 available), and active tracking for Request #LV1026.
3. **Apply Leave Page (Faculty):** Leave application form (CL, EL, ML, OD, dates, reasons, file upload) with automatic lecture conflict detection and slot availability indicator.
4. **Slot & Queue Status (Faculty):** Department quota alert, queue position tracker (`#2`), and 5-stage visual approval stepper (`Submitted` ➔ `Waiting for Slot` ➔ `HOD Pending` ➔ `Dean Pending` ➔ `Principal Approved`).
5. **Notification Panel (Faculty):** Categorized tabs (All, Unread, Read) with color-coded status badges and timestamps.
6. **My Leave Requests (Faculty):** Filterable table (All, Pending, Approved, Rejected, Canceled) with details modal.
7. **My Timetable (Faculty):** Day-by-day lecture schedule (Mon–Fri) with class, subject, and classroom room numbers.
8. **Leave Slot Queue (HOD View):** Department slot capacity monitor (Total Slots: 3, Occupied: 3, Available: 0) and live queue order.
9. **HOD Pending Approvals:** Department and status filtering with instant one-click **Approve** and **Reject** actions.
10. **Dean Approval Queue:** Academic dean level review of HOD-approved leave applications.
11. **Principal Dashboard:** High-level executive statistics, Leave Type Distribution donut chart (CL: 45%, ML: 25%, OD: 20%, Other: 10%), and recent approvals feed.
12. **College Calendar:** Interactive monthly calendar for September 2026 with leave density indicators and day inspection sidebar.
13. **Substitute Management (HOD):** Automated clash-free substitute teacher allocation for affected lectures.
14. **Leave History (Faculty):** Historical archive of leave applications with annual filtering.
15. **Leave Balance (Faculty):** Entitlement cards with used/remaining counters and capacity bars for CL, EL, ML, and OD.
16. **Admin Panel:** Complete faculty directory management with Add Faculty modal and role assignment.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Tested with Python 3.14)
- Pip

### 2. Run the Server
From the project root directory:

```bash
# Optional: Install dependencies if needed
pip install -r requirements.txt

# Start the application
python3 app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🗄️ Database: Local JSON vs MongoDB

The application uses an abstract storage repository layer (`DataStore`):

### Mode 1: Local Pre-seeded Data (Active by Default)
- Starts immediately with zero configuration.
- Automatically saves edits (new leaves, approvals, substitutes, faculty additions) into `data.json`.
- Click the **"↺ Reset Data"** button anytime in the top bar to restore pristine demo data.

### Mode 2: Connecting MongoDB (When Ready)
To connect your MongoDB database, create a `.env` file in the project root:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=facultyflow
```

*Or for MongoDB Atlas (Cloud):*
```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=facultyflow
```

Restart the app (`python3 app.py`). The system will:
1. Detect `MONGODB_URI`.
2. Connect to MongoDB using `pymongo`.
3. Automatically seed your MongoDB collections (`users`, `leaves`, `slots`, `notifications`, `substitutes`, etc.) if empty.
4. Display **"MongoDB"** in the top bar status badge!

---

## 👥 Demo Institutional Accounts

| Role | Name | Email | Default Dashboard |
|---|---|---|---|
| **Faculty** | Dr. Ananya | `ananya@klsvdit.ac.in` | Faculty Dashboard (#LV1026, Queue #2) |
| **HOD** | Dr. Rahul | `rahul@klsvdit.ac.in` | HOD Approvals & Slot Queue |
| **Dean** | Dr. Kumar | `kumar@klsvdit.ac.in` | Dean Approval Queue |
| **Principal** | Dr. Reddy | `reddy@klsvdit.ac.in` | Principal Executive Dashboard |
| **Admin** | System Admin | `admin@klsvdit.ac.in` | Faculty Management Directory |

*Tip: You can instantly switch roles using the **Role dropdown** in the top navigation bar or the **View Screen** showcase dropdown during project demos!*

---

## 📁 Project Structure

```
/
├── app.py                   # FastAPI application & REST endpoints
├── config.py                # Configuration and environment settings
├── data.json                # Local JSON persistence storage
├── requirements.txt         # Project dependencies
├── database/
│   ├── __init__.py          # Database factory (Auto-detects MongoDB or Local)
│   ├── store.py             # Local JSON DataStore implementation
│   ├── mongo_store.py       # PyMongo DataStore adapter
│   └── seed_data.py         # Institutional seed data
├── static/
│   ├── css/
│   │   └── style.css        # Complete custom styling matching reference design
│   └── js/
│       └── app.js           # Multi-screen router & reactive UI logic
├── templates/
│   └── index.html           # Single-page template for all 16 screens
└── README.md                # Project documentation
```
