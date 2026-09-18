"""
FacultyFlow - MongoDB Atlas Data Store Adapter
Stores all application data (users, leaves, slots, notifications, timetable, substitutes, balances, metrics)
directly in MongoDB Atlas.
"""
import copy
import json
import logging
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient

from database.seed_data import (
    INITIAL_USERS,
    INITIAL_LEAVES,
    INITIAL_SLOTS,
    INITIAL_NOTIFICATIONS,
    INITIAL_TIMETABLE,
    INITIAL_SUBSTITUTES,
    INITIAL_LEAVE_BALANCE,
    PRINCIPAL_METRICS,
    CALENDAR_EVENTS
)

logger = logging.getLogger("facultyflow.mongo")


class MongoDataStore:
    def __init__(self, uri: str, db_name: str = "facultyflow"):
        self.uri = uri
        self.db_name = db_name
        self.client = MongoClient(uri, serverSelectionTimeoutMS=8000)
        # Ping to test connectivity
        self.client.admin.command('ping')
        self.db = self.client[db_name]
        self._ensure_seed()

    def _ensure_seed(self):
        """
        If MongoDB collections are empty, populate them directly with initial
        reference state from seed_data.py into MongoDB Atlas.
        Keeps admin credentials in a dedicated 'admin' collection and all other
        institutional accounts in 'users'.
        """
        users = copy.deepcopy(INITIAL_USERS)
        leaves = copy.deepcopy(INITIAL_LEAVES)
        slots = copy.deepcopy(INITIAL_SLOTS)
        notifications = copy.deepcopy(INITIAL_NOTIFICATIONS)
        timetable = copy.deepcopy(INITIAL_TIMETABLE)
        substitutes = copy.deepcopy(INITIAL_SUBSTITUTES)
        leave_balance = copy.deepcopy(INITIAL_LEAVE_BALANCE)
        principal_metrics = copy.deepcopy(PRINCIPAL_METRICS)
        calendar_events = copy.deepcopy(CALENDAR_EVENTS)

        # 1. Dedicated 'admin' collection migration & seeding
        admins_in_users = list(self.db.users.find({"$or": [{"role": "admin"}, {"email": "admin@klsvdit.ac.in"}]}))
        if admins_in_users:
            logger.info(f"Moving {len(admins_in_users)} admin document(s) from 'users' to dedicated 'admin' collection...")
            for adm in admins_in_users:
                adm_copy = copy.deepcopy(adm)
                adm_copy.pop("_id", None)
                if not self.db.admin.find_one({"email": adm_copy.get("email")}):
                    self.db.admin.insert_one(adm_copy)
            # Remove from users collection
            self.db.users.delete_many({"$or": [{"role": "admin"}, {"email": "admin@klsvdit.ac.in"}]})

        if self.db.admin.count_documents({}) == 0:
            logger.info("Seeding dedicated 'admin' collection in MongoDB...")
            admin_user = next((u for u in users if u.get("role") == "admin"), None)
            if not admin_user:
                admin_user = {
                    "id": "usr_admin",
                    "name": "Admin",
                    "email": "admin@klsvdit.ac.in",
                    "role": "admin",
                    "department": "Administration",
                    "designation": "Administrator",
                    "avatar": "",
                    "phone": "+91 98765 43214",
                    "password": "password123"
                }
            admin_doc = copy.deepcopy(admin_user)
            if "password" not in admin_doc:
                admin_doc["password"] = "password123"
            self.db.admin.insert_one(admin_doc)

        # Ensure 'users' collection NEVER contains admin accounts
        self.db.users.delete_many({"$or": [{"role": "admin"}, {"email": "admin@klsvdit.ac.in"}]})

        # 2. 'users' collection (Non-Admin users only)
        if self.db.users.count_documents({}) == 0:
            logger.info("Seeding non-admin users collection in MongoDB...")
            non_admin_users = [u for u in users if u.get("role") != "admin"]
            for u in non_admin_users:
                if "password" not in u:
                    u["password"] = "password123"
            self.db.users.insert_many(copy.deepcopy(non_admin_users))

        # 3. Explicitly ensure EVERY document in 'admin' and 'users' has the 'password' field in MongoDB
        self.db.admin.update_many(
            {"$or": [{"password": {"$exists": False}}, {"password": None}, {"password": ""}]},
            {"$set": {"password": "password123"}}
        )
        self.db.users.update_many(
            {"$or": [{"password": {"$exists": False}}, {"password": None}, {"password": ""}]},
            {"$set": {"password": "password123"}}
        )

        if self.db.leaves.count_documents({}) == 0:
            logger.info("Seeding leaves collection in MongoDB...")
            self.db.leaves.insert_many(copy.deepcopy(leaves))

        if self.db.slots.count_documents({}) == 0:
            logger.info("Seeding slots collection in MongoDB...")
            self.db.slots.insert_one(copy.deepcopy(slots))

        if self.db.notifications.count_documents({}) == 0:
            logger.info("Seeding notifications collection in MongoDB...")
            self.db.notifications.insert_many(copy.deepcopy(notifications))

        if self.db.substitutes.count_documents({}) == 0:
            logger.info("Seeding substitutes collection in MongoDB...")
            self.db.substitutes.insert_many(copy.deepcopy(substitutes))

        # Meta collections for timetable, balances, metrics, calendar
        if self.db.meta.count_documents({"key": "timetable"}) == 0:
            self.db.meta.insert_one({"key": "timetable", "data": copy.deepcopy(timetable)})

        if self.db.meta.count_documents({"key": "leave_balance"}) == 0:
            self.db.meta.insert_one({"key": "leave_balance", "data": copy.deepcopy(leave_balance)})

        if self.db.meta.count_documents({"key": "principal_metrics"}) == 0:
            self.db.meta.insert_one({"key": "principal_metrics", "data": copy.deepcopy(principal_metrics)})

        if self.db.meta.count_documents({"key": "calendar_events"}) == 0:
            self.db.meta.insert_one({"key": "calendar_events", "data": copy.deepcopy(calendar_events)})

    # --- Admin Collection (Dedicated for Administrator Credentials) ---
    def get_admins(self):
        admins = list(self.db.admin.find({}, {"_id": 0}))
        for a in admins:
            if "password" not in a:
                a["password"] = "password123"
            a["role"] = "admin"
        return admins

    def get_admin_by_id(self, admin_id):
        a = self.db.admin.find_one({"id": admin_id}, {"_id": 0})
        if a and "password" not in a:
            a["password"] = "password123"
        return a

    def add_admin(self, admin_data):
        if not admin_data.get("id"):
            email_prefix = admin_data.get("email", "").split("@")[0].lower()
            clean_prefix = "".join(c for c in email_prefix if c.isalnum() or c == "_")
            ts = int(datetime.now().timestamp())
            admin_data["id"] = f"usr_{clean_prefix}" if clean_prefix and not self.db.admin.find_one({"id": f"usr_{clean_prefix}"}) else f"usr_{clean_prefix}_{ts}"
        if "password" not in admin_data or not admin_data["password"]:
            admin_data["password"] = "password123"
        admin_data["role"] = "admin"
        self.db.admin.insert_one(copy.deepcopy(admin_data))
        clean = copy.deepcopy(admin_data)
        clean.pop("_id", None)
        return clean

    def update_admin(self, admin_id, update_data):
        clean_update = copy.deepcopy(update_data)
        clean_update.pop("id", None)
        clean_update.pop("_id", None)
        clean_update["role"] = "admin"
        self.db.admin.update_one({"id": admin_id}, {"$set": clean_update})
        return self.get_admin_by_id(admin_id)

    def delete_admin(self, admin_id):
        self.db.admin.delete_one({"id": admin_id})
        return True

    # --- Users Collection (Non-Admin Accounts: Faculty, HOD, Dean, Principal, Student) ---
    def get_users(self):
        users = list(self.db.users.find({}, {"_id": 0}))
        for u in users:
            if "password" not in u:
                u["password"] = "password123"
        return users

    def get_all_accounts(self):
        """Returns unified list of all accounts (admins from 'admin' + users from 'users')"""
        admins = self.get_admins()
        users = self.get_users()
        return admins + users

    def get_user_by_id(self, user_id):
        # 1. Search in dedicated admin collection
        admin = self.get_admin_by_id(user_id)
        if admin:
            return admin
        # 2. Search in users collection
        u = self.db.users.find_one({"id": user_id}, {"_id": 0})
        if u and "password" not in u:
            u["password"] = "password123"
        return u

    def add_user(self, user_data):
        # Route admin to 'admin' collection
        if (user_data.get("role") or "").lower() == "admin":
            return self.add_admin(user_data)

        # Non-admin users go to 'users' collection
        if not user_data.get("id"):
            email_prefix = user_data.get("email", "").split("@")[0].lower()
            clean_prefix = "".join(c for c in email_prefix if c.isalnum() or c == "_")
            ts = int(datetime.now().timestamp())
            user_data["id"] = f"usr_{clean_prefix}" if clean_prefix and not self.db.users.find_one({"id": f"usr_{clean_prefix}"}) else f"usr_{clean_prefix}_{ts}"
        if "password" not in user_data or not user_data["password"]:
            user_data["password"] = "password123"
        self.db.users.insert_one(copy.deepcopy(user_data))
        clean = copy.deepcopy(user_data)
        clean.pop("_id", None)
        return clean

    def update_user(self, user_id, update_data):
        new_role = (update_data.get("role") or "").lower()

        # Case 1: Currently in 'admin' collection
        if self.db.admin.find_one({"id": user_id}):
            if new_role and new_role != "admin":
                # Demoted from admin -> move to 'users' collection
                current = self.get_admin_by_id(user_id)
                self.delete_admin(user_id)
                current.update(update_data)
                return self.add_user(current)
            else:
                return self.update_admin(user_id, update_data)

        # Case 2: Currently in 'users' collection
        if new_role == "admin":
            # Promoted to admin -> move to 'admin' collection
            current = self.get_user_by_id(user_id)
            self.delete_user(user_id)
            if current:
                current.update(update_data)
                return self.add_admin(current)
            else:
                return self.add_admin(update_data)

        # Standard non-admin update in 'users' collection
        clean_update = copy.deepcopy(update_data)
        clean_update.pop("id", None)
        clean_update.pop("_id", None)
        self.db.users.update_one({"id": user_id}, {"$set": clean_update})
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id):
        # Check admin collection first
        if self.db.admin.find_one({"id": user_id}):
            return self.delete_admin(user_id)
        # Otherwise delete from users collection
        self.db.users.delete_one({"id": user_id})
        return True

    # --- Leaves ---
    def get_leaves(self, role=None, user_id=None, department=None, status=None):
        query = {}
        if user_id and role == "faculty":
            query["faculty_id"] = user_id
        if department and department != "All":
            query["department"] = department

        leaves = list(self.db.leaves.find(query, {"_id": 0}))
        if status and status != "All":
            filtered = []
            for lv in leaves:
                if status == "Pending":
                    if "Pending" in lv.get("status", "") or "Waiting" in lv.get("status", ""):
                        filtered.append(lv)
                elif status.lower() in lv.get("status", "").lower():
                    filtered.append(lv)
            return filtered
        return leaves

    def get_leave_by_id(self, leave_id):
        return self.db.leaves.find_one({"id": leave_id}, {"_id": 0})

    def create_leave(self, leave_data):
        count = self.db.leaves.count_documents({})
        leave_id = f"LV{1000 + count + 1}"
        leave_data["id"] = leave_id
        leave_data["submitted_on"] = datetime.now().strftime("%d %b %Y")

        slots = self.get_slots()
        total = slots.get("total_slots", 3)
        occupied = slots.get("occupied", 3)

        if occupied >= total:
            leave_data["status"] = "Waiting for Slot"
            queue = slots.get("queue", [])
            queue_pos = len(queue) + 1
            leave_data["queue_position"] = queue_pos
            leave_data["approval_stage"] = "waiting_slot"
            queue.append({
                "id": queue_pos,
                "faculty_name": leave_data.get("faculty_name", "Dr. Ananya"),
                "leave_date": leave_data.get("date_display", "21 Sep 2026"),
                "status": "Waiting"
            })
            self.db.slots.update_one({}, {"$set": {"queue": queue, "available": max(0, total - occupied)}})
        else:
            leave_data["status"] = "HOD Pending"
            leave_data["queue_position"] = None
            leave_data["approval_stage"] = "hod_pending"
            new_occ = occupied + 1
            self.db.slots.update_one({}, {"$set": {"occupied": new_occ, "available": max(0, total - new_occ)}})

        leave_data["approval_history"] = [
            {"stage": "Submitted", "completed": True, "date": leave_data["submitted_on"], "by": leave_data.get("faculty_name", "")},
            {"stage": "Waiting for Slot", "completed": leave_data["status"] == "Waiting for Slot", "info": f"Queue #{leave_data.get('queue_position', '-')}" if leave_data.get('queue_position') else "Slot Allocated"},
            {"stage": "HOD Pending", "completed": False, "approver": "Dr. Rahul"},
            {"stage": "Dean Pending", "completed": False, "approver": "Dr. Kumar"},
            {"stage": "Principal Approved", "completed": False, "approver": "Dr. Reddy"}
        ]

        # Insert leave document
        doc = copy.deepcopy(leave_data)
        self.db.leaves.insert_one(doc)

        # Deduct leave balance in MongoDB
        fac_id = leave_data.get("faculty_id", "usr_ananya")
        ltype = leave_data.get("type", "CL")
        bal_doc = self.db.meta.find_one({"key": "leave_balance"})
        if bal_doc and "data" in bal_doc:
            bals = bal_doc["data"]
            if fac_id in bals and ltype in bals[fac_id]:
                target_bal = bals[fac_id][ltype]
                if target_bal.get("remaining", 0) > 0:
                    target_bal["used"] = target_bal.get("used", 0) + 1
                    target_bal["remaining"] = max(0, target_bal.get("remaining", 0) - 1)
                    self.db.meta.update_one({"key": "leave_balance"}, {"$set": {"data": bals}})

        # Create notification in MongoDB
        self.add_notification(
            user_id=fac_id,
            title="Leave request submitted",
            message=f"Your leave request (#{leave_id}) has been submitted successfully.",
            ntype="submit"
        )

        clean = copy.deepcopy(leave_data)
        clean.pop("_id", None)
        return clean

    def update_leave_action(self, leave_id, action, actor_role, comment=None):
        lv = self.get_leave_by_id(leave_id)
        if not lv:
            return None

        actor_names = {
            "hod": "Dr. Rahul (HOD)",
            "dean": "Dr. Kumar (Dean)",
            "principal": "Dr. Reddy (Principal)"
        }
        actor_name = actor_names.get(actor_role, actor_role.capitalize())

        updates = {}
        if action == "approve":
            if actor_role == "hod":
                updates = {"status": "Dean Pending", "hod_status": "Approved", "approval_stage": "dean_pending"}
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="HOD approved your leave",
                    message=f"Your leave request ({leave_id}) was approved by HOD and sent to Dean.",
                    ntype="approved"
                )
            elif actor_role == "dean":
                updates = {"status": "Principal Pending", "dean_status": "Approved", "approval_stage": "principal_pending"}
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="Dean reviewed your leave",
                    message=f"Your leave request ({leave_id}) was endorsed by Dean and sent to Principal.",
                    ntype="approved"
                )
            elif actor_role == "principal":
                updates = {"status": "Approved", "principal_status": "Approved", "approval_stage": "approved"}
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="Leave Approved by Principal",
                    message=f"Congratulations! Your leave request ({leave_id}) has received final approval.",
                    ntype="approved"
                )
                # Update principal metrics in MongoDB
                meta_metrics = self.db.meta.find_one({"key": "principal_metrics"})
                if meta_metrics and "data" in meta_metrics:
                    pm = meta_metrics["data"]
                    pm["approved_today"] = pm.get("approved_today", 12) + 1
                    recents = pm.setdefault("recent_approvals", [])
                    recents.insert(0, {
                        "faculty": lv.get("faculty_name", "Faculty"),
                        "date": lv.get("date_display", datetime.now().strftime("%d %b %Y")),
                        "status": "Approved"
                    })
                    self.db.meta.update_one({"key": "principal_metrics"}, {"$set": {"data": pm}})
        elif action == "reject":
            updates = {"status": "Rejected", "approval_stage": "rejected", "rejection_reason": comment or f"Rejected by {actor_name}"}
            self.add_notification(
                user_id=lv.get("faculty_id", "usr_ananya"),
                title=f"{actor_role.upper()} rejected your leave",
                message=f"Your leave request ({leave_id}) was rejected by {actor_name}. Reason: {comment or 'Short notice / academic clash'}",
                ntype="rejected"
            )
            # Restore balance in MongoDB
            fac_id = lv.get("faculty_id", "usr_ananya")
            ltype = lv.get("type", "CL")
            bal_doc = self.db.meta.find_one({"key": "leave_balance"})
            if bal_doc and "data" in bal_doc:
                bals = bal_doc["data"]
                if fac_id in bals and ltype in bals[fac_id]:
                    target_bal = bals[fac_id][ltype]
                    target_bal["used"] = max(0, target_bal.get("used", 0) - 1)
                    target_bal["remaining"] = min(target_bal.get("total", 12), target_bal.get("remaining", 0) + 1)
                    self.db.meta.update_one({"key": "leave_balance"}, {"$set": {"data": bals}})
        elif action == "cancel":
            updates = {"status": "Canceled", "approval_stage": "canceled"}

        self.db.leaves.update_one({"id": leave_id}, {"$set": updates})
        lv.update(updates)
        return lv

    # --- Slots ---
    def get_slots(self):
        doc = self.db.slots.find_one({}, {"_id": 0})
        return doc or copy.deepcopy(INITIAL_SLOTS)

    def update_slots(self, total_slots=None, occupied=None):
        doc = self.get_slots()
        if total_slots is not None:
            doc["total_slots"] = int(total_slots)
        if occupied is not None:
            doc["occupied"] = int(occupied)
        doc["available"] = max(0, doc["total_slots"] - doc["occupied"])
        self.db.slots.replace_one({}, doc, upsert=True)
        return doc

    # --- Notifications ---
    def get_notifications(self, user_id=None, filter_tab="all"):
        query = {}
        if user_id:
            query["user_id"] = user_id
        if filter_tab == "unread":
            query["read"] = False
        elif filter_tab == "read":
            query["read"] = True
        return list(self.db.notifications.find(query, {"_id": 0}).sort("_id", -1))

    def add_notification(self, user_id, title, message, ntype="info"):
        item = {
            "id": f"notif_{int(datetime.now().timestamp()*1000)}",
            "user_id": user_id,
            "title": title,
            "message": message,
            "time": "Just now",
            "read": False,
            "type": ntype
        }
        self.db.notifications.insert_one(copy.deepcopy(item))
        clean = copy.deepcopy(item)
        clean.pop("_id", None)
        return clean

    def mark_notifications_read(self, notif_id=None, user_id=None):
        if notif_id:
            self.db.notifications.update_one({"id": notif_id}, {"$set": {"read": True}})
        elif user_id:
            self.db.notifications.update_many({"user_id": user_id}, {"$set": {"read": True}})
        return True

    # --- Timetable & Substitutes ---
    def get_timetable(self, day="Mon"):
        meta = self.db.meta.find_one({"key": "timetable"})
        tt = meta.get("data", INITIAL_TIMETABLE) if meta else INITIAL_TIMETABLE
        return tt.get(day, [])

    def get_all_timetable(self):
        meta = self.db.meta.find_one({"key": "timetable"})
        return meta.get("data", INITIAL_TIMETABLE) if meta else INITIAL_TIMETABLE

    def get_substitutes(self):
        return list(self.db.substitutes.find({}, {"_id": 0}))

    def assign_substitute(self, sub_id, substitute_faculty_name):
        self.db.substitutes.update_one(
            {"id": sub_id},
            {"$set": {"status": "Assigned", "substitute_assigned": substitute_faculty_name}}
        )
        return self.db.substitutes.find_one({"id": sub_id}, {"_id": 0})

    # --- Balance & Metrics ---
    def get_leave_balance(self, user_id="usr_ananya"):
        meta = self.db.meta.find_one({"key": "leave_balance"})
        bals = meta.get("data", INITIAL_LEAVE_BALANCE) if meta else INITIAL_LEAVE_BALANCE
        return bals.get(user_id, INITIAL_LEAVE_BALANCE.get("usr_ananya", {}))

    def get_principal_metrics(self):
        meta = self.db.meta.find_one({"key": "principal_metrics"})
        return meta.get("data", PRINCIPAL_METRICS) if meta else PRINCIPAL_METRICS

    def get_calendar_events(self):
        meta = self.db.meta.find_one({"key": "calendar_events"})
        return meta.get("data", CALENDAR_EVENTS) if meta else CALENDAR_EVENTS

    def reset_to_seed(self):
        """Wipes and reseeds all collections in MongoDB"""
        self.db.users.delete_many({})
        self.db.leaves.delete_many({})
        self.db.slots.delete_many({})
        self.db.notifications.delete_many({})
        self.db.substitutes.delete_many({})
        self.db.meta.delete_many({})
        self._ensure_seed()
