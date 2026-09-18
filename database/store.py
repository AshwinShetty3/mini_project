import json
import os
import copy
from pathlib import Path
from datetime import datetime
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

DATA_FILE = Path(__file__).resolve().parent.parent / "data.json"

class JsonDataStore:
    def __init__(self):
        self._load()

    def _load(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                return
            except Exception:
                pass
        # Fallback / Initial Seed
        self.reset_to_seed()

    def _save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data to {DATA_FILE}: {e}")

    def reset_to_seed(self):
        all_initial = copy.deepcopy(INITIAL_USERS)
        admin_users = [u for u in all_initial if u.get("role") == "admin"]
        regular_users = [u for u in all_initial if u.get("role") != "admin"]

        self.data = {
            "admin": admin_users,
            "users": regular_users,
            "leaves": copy.deepcopy(INITIAL_LEAVES),
            "slots": copy.deepcopy(INITIAL_SLOTS),
            "notifications": copy.deepcopy(INITIAL_NOTIFICATIONS),
            "timetable": copy.deepcopy(INITIAL_TIMETABLE),
            "substitutes": copy.deepcopy(INITIAL_SUBSTITUTES),
            "leave_balance": copy.deepcopy(INITIAL_LEAVE_BALANCE),
            "principal_metrics": copy.deepcopy(PRINCIPAL_METRICS),
            "calendar_events": copy.deepcopy(CALENDAR_EVENTS)
        }
        self._save()

    # --- Admin & Users ---
    def get_admins(self):
        return self.data.get("admin", [])

    def get_users(self):
        return [u for u in self.data.get("users", []) if u.get("role") != "admin"]

    def get_all_accounts(self):
        return self.get_admins() + self.get_users()

    def get_user_by_id(self, user_id):
        for u in self.get_all_accounts():
            if u["id"] == user_id:
                return u
        return None

    def add_user(self, user_data):
        user_id = f"usr_{int(datetime.now().timestamp()*1000)}"
        user_data["id"] = user_id
        if (user_data.get("role") or "").lower() == "admin":
            self.data.setdefault("admin", []).append(user_data)
        else:
            self.data.setdefault("users", []).append(user_data)
        self._save()
        return user_data

    def update_user(self, user_id, update_data):
        for pool in ["admin", "users"]:
            for u in self.data.get(pool, []):
                if u["id"] == user_id:
                    u.update(update_data)
                    self._save()
                    return u
        return None

    def delete_user(self, user_id):
        self.data["admin"] = [u for u in self.data.get("admin", []) if u["id"] != user_id]
        self.data["users"] = [u for u in self.data.get("users", []) if u["id"] != user_id]
        self._save()
        return True

    # --- Leaves ---
    def get_leaves(self, role=None, user_id=None, department=None, status=None):
        leaves = self.data.get("leaves", [])
        result = []
        for lv in leaves:
            # User filtering
            if user_id and role == "faculty" and lv.get("faculty_id") != user_id:
                continue
            # Department filtering
            if department and department != "All" and lv.get("department") != department:
                continue
            # Status filtering
            if status and status != "All":
                if status == "Pending":
                    if "Pending" not in lv.get("status", "") and "Waiting" not in lv.get("status", ""):
                        continue
                elif status.lower() not in lv.get("status", "").lower():
                    continue
            result.append(lv)
        return result

    def get_leave_by_id(self, leave_id):
        for lv in self.data.get("leaves", []):
            if lv["id"] == leave_id:
                return lv
        return None

    def create_leave(self, leave_data):
        # Generate new ID
        leaves = self.data.get("leaves", [])
        new_num = 1000 + len(leaves) + 1
        leave_id = f"LV{new_num}"
        leave_data["id"] = leave_id
        leave_data["submitted_on"] = datetime.now().strftime("%d %b %Y")
        
        # Check slot quota
        slots = self.data.get("slots", {})
        total = slots.get("total_slots", 3)
        occupied = slots.get("occupied", 3)
        
        if occupied >= total:
            # Put into queue
            leave_data["status"] = "Waiting for Slot"
            queue = slots.setdefault("queue", [])
            queue_pos = len(queue) + 1
            leave_data["queue_position"] = queue_pos
            leave_data["approval_stage"] = "waiting_slot"
            queue.append({
                "id": queue_pos,
                "faculty_name": leave_data.get("faculty_name", "Dr. Ananya"),
                "leave_date": leave_data.get("date_display", "21 Sep 2026"),
                "status": "Waiting"
            })
            slots["available"] = max(0, total - occupied)
        else:
            # Direct HOD Pending
            leave_data["status"] = "HOD Pending"
            leave_data["queue_position"] = None
            leave_data["approval_stage"] = "hod_pending"
            slots["occupied"] = occupied + 1
            slots["available"] = max(0, total - slots["occupied"])

        # Construct approval history
        leave_data["approval_history"] = [
            {"stage": "Submitted", "completed": True, "date": leave_data["submitted_on"], "by": leave_data.get("faculty_name", "")},
            {"stage": "Waiting for Slot", "completed": leave_data["status"] == "Waiting for Slot", "info": f"Queue #{leave_data.get('queue_position', '-')}" if leave_data.get('queue_position') else "Slot Allocated"},
            {"stage": "HOD Pending", "completed": False, "approver": "Dr. Rahul"},
            {"stage": "Dean Pending", "completed": False, "approver": "Dr. Kumar"},
            {"stage": "Principal Approved", "completed": False, "approver": "Dr. Reddy"}
        ]

        # Insert at top
        leaves.insert(0, leave_data)
        
        # Deduct balance if faculty_id has balance
        fac_id = leave_data.get("faculty_id", "usr_ananya")
        ltype = leave_data.get("type", "CL")
        bal = self.data.get("leave_balance", {}).get(fac_id, {}).get(ltype)
        if bal and bal["remaining"] > 0:
            bal["used"] += 1
            bal["remaining"] -= 1

        # Add notification
        self.add_notification(
            user_id=fac_id,
            title="Leave request submitted",
            message=f"Your leave request (#{leave_id}) has been submitted successfully.",
            ntype="submit"
        )

        self._save()
        return leave_data

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

        if action == "approve":
            if actor_role == "hod":
                lv["status"] = "Dean Pending"
                lv["hod_status"] = "Approved"
                lv["approval_stage"] = "dean_pending"
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="HOD approved your leave",
                    message=f"Your leave request ({leave_id}) was approved by HOD and sent to Dean.",
                    ntype="approved"
                )
            elif actor_role == "dean":
                lv["status"] = "Principal Pending"
                lv["dean_status"] = "Approved"
                lv["approval_stage"] = "principal_pending"
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="Dean reviewed your leave",
                    message=f"Your leave request ({leave_id}) was endorsed by Dean and sent to Principal.",
                    ntype="approved"
                )
            elif actor_role == "principal":
                lv["status"] = "Approved"
                lv["principal_status"] = "Approved"
                lv["approval_stage"] = "approved"
                self.add_notification(
                    user_id=lv.get("faculty_id", "usr_ananya"),
                    title="Leave Approved by Principal",
                    message=f"Congratulations! Your leave request ({leave_id}) has received final approval.",
                    ntype="approved"
                )
                # Update principal metrics
                pm = self.data.setdefault("principal_metrics", {})
                pm["approved_today"] = pm.get("approved_today", 12) + 1
                pm.setdefault("recent_approvals", []).insert(0, {
                    "faculty": lv.get("faculty_name", "Faculty"),
                    "date": lv.get("date_display", datetime.now().strftime("%d %b %Y")),
                    "status": "Approved"
                })
        elif action == "reject":
            lv["status"] = "Rejected"
            lv["approval_stage"] = "rejected"
            lv["rejection_reason"] = comment or f"Rejected by {actor_name}"
            self.add_notification(
                user_id=lv.get("faculty_id", "usr_ananya"),
                title=f"{actor_role.upper()} rejected your leave",
                message=f"Your leave request ({leave_id}) was rejected by {actor_name}. Reason: {comment or 'Short notice / academic clash'}",
                ntype="rejected"
            )
            # Restore leave balance
            fac_id = lv.get("faculty_id", "usr_ananya")
            ltype = lv.get("type", "CL")
            bal = self.data.get("leave_balance", {}).get(fac_id, {}).get(ltype)
            if bal:
                bal["used"] = max(0, bal["used"] - 1)
                bal["remaining"] = min(bal["total"], bal["remaining"] + 1)
        elif action == "cancel":
            lv["status"] = "Canceled"
            lv["approval_stage"] = "canceled"
        
        self._save()
        return lv

    # --- Slots ---
    def get_slots(self):
        return self.data.get("slots", INITIAL_SLOTS)

    def update_slots(self, total_slots=None, occupied=None):
        slots = self.data.setdefault("slots", INITIAL_SLOTS)
        if total_slots is not None:
            slots["total_slots"] = int(total_slots)
        if occupied is not None:
            slots["occupied"] = int(occupied)
        slots["available"] = max(0, slots["total_slots"] - slots["occupied"])
        self._save()
        return slots

    # --- Notifications ---
    def get_notifications(self, user_id=None, filter_tab="all"):
        notifs = self.data.get("notifications", [])
        if user_id:
            notifs = [n for n in notifs if n.get("user_id") == user_id]
        if filter_tab == "unread":
            notifs = [n for n in notifs if not n.get("read", False)]
        elif filter_tab == "read":
            notifs = [n for n in notifs if n.get("read", False)]
        return notifs

    def add_notification(self, user_id, title, message, ntype="info"):
        notifs = self.data.setdefault("notifications", [])
        new_id = f"notif_{int(datetime.now().timestamp()*1000)}"
        item = {
            "id": new_id,
            "user_id": user_id,
            "title": title,
            "message": message,
            "time": "Just now",
            "read": False,
            "type": ntype
        }
        notifs.insert(0, item)
        self._save()
        return item

    def mark_notifications_read(self, notif_id=None, user_id=None):
        notifs = self.data.get("notifications", [])
        for n in notifs:
            if notif_id and n["id"] == notif_id:
                n["read"] = True
            elif not notif_id and user_id and n.get("user_id") == user_id:
                n["read"] = True
        self._save()
        return True

    # --- Timetable & Substitutes ---
    def get_timetable(self, day="Mon"):
        tt = self.data.get("timetable", INITIAL_TIMETABLE)
        return tt.get(day, [])

    def get_all_timetable(self):
        return self.data.get("timetable", INITIAL_TIMETABLE)

    def get_substitutes(self):
        return self.data.get("substitutes", INITIAL_SUBSTITUTES)

    def assign_substitute(self, sub_id, substitute_faculty_name):
        subs = self.data.get("substitutes", [])
        for s in subs:
            if s["id"] == sub_id:
                s["status"] = "Assigned"
                s["substitute_assigned"] = substitute_faculty_name
                self._save()
                return s
        return None

    # --- Balance & Metrics ---
    def get_leave_balance(self, user_id="usr_ananya"):
        bals = self.data.get("leave_balance", {})
        return bals.get(user_id, INITIAL_LEAVE_BALANCE["usr_ananya"])

    def get_principal_metrics(self):
        return self.data.get("principal_metrics", PRINCIPAL_METRICS)

    def get_calendar_events(self):
        return self.data.get("calendar_events", CALENDAR_EVENTS)
