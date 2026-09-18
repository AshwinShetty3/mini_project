"""
FacultyFlow - Initial Seed Data
Represents the exact initial data visible in the project UI collage.
"""

INITIAL_USERS = [
    {
        "id": "usr_ananya",
        "name": "Dr. Ananya",
        "email": "ananya@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "CSE(AIML)",
        "designation": "Faculty",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43210"
    },
    {
        "id": "usr_rahul",
        "name": "Dr. Rahul",
        "email": "rahul@klsvdit.ac.in",
        "password": "password123",
        "role": "hod",
        "department": "CSE(AIML)",
        "designation": "HOD",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43211"
    },
    {
        "id": "usr_kumar",
        "name": "Dr. Kumar",
        "email": "kumar@klsvdit.ac.in",
        "password": "password123",
        "role": "dean",
        "department": "Academic",
        "designation": "Dean",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43212"
    },
    {
        "id": "usr_reddy",
        "name": "Dr. Reddy",
        "email": "reddy@klsvdit.ac.in",
        "password": "password123",
        "role": "principal",
        "department": "Administration",
        "designation": "Principal",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43213"
    },
    {
        "id": "usr_admin",
        "name": "Admin",
        "email": "admin@klsvdit.ac.in",
        "password": "password123",
        "role": "admin",
        "department": "Administration",
        "designation": "Administrator",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43214"
    },
    {
        "id": "usr_student",
        "name": "Rohit Sharma",
        "email": "student@klsvdit.ac.in",
        "password": "password123",
        "role": "student",
        "department": "CSE(AIML)",
        "designation": "Student (5th Sem A)",
        "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80",
        "phone": "+91 98765 43215"
    },
    {
        "id": "usr_dr_b",
        "name": "Dr. B",
        "email": "b@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "CSE(AIML)",
        "designation": "Assistant Professor",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150&auto=format&fit=crop&q=80"
    },
    {
        "id": "usr_dr_c",
        "name": "Dr. C",
        "email": "c@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "ECE",
        "designation": "Associate Professor",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80"
    },
    {
        "id": "usr_dr_d",
        "name": "Dr. D",
        "email": "d@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "ME",
        "designation": "Assistant Professor",
        "avatar": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=150&auto=format&fit=crop&q=80"
    },
    {
        "id": "usr_dr_e",
        "name": "Dr. E",
        "email": "e@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "ECE",
        "designation": "Assistant Professor",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80"
    },
    {
        "id": "usr_dr_f",
        "name": "Dr. F",
        "email": "f@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "ME",
        "designation": "Associate Professor",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80"
    },
    {
        "id": "usr_dr_g",
        "name": "Dr. G",
        "email": "g@klsvdit.ac.in",
        "password": "password123",
        "role": "faculty",
        "department": "CSE",
        "designation": "Professor",
        "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80"
    }
]

INITIAL_LEAVES = [
    {
        "id": "LV1026",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-09-21",
        "to_date": "2026-09-21",
        "date_display": "21 Sep 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Personal work",
        "status": "Waiting for Slot",
        "queue_position": 2,
        "submitted_on": "15 Sep 2026",
        "supporting_doc": "medical_doc_optional.pdf",
        "classes_affected": [
            {"subject": "CN", "name": "Computer Networks", "time": "09:00 - 10:00", "class": "5th Sem A", "room": "204", "status": "Affected"},
            {"subject": "TOC", "name": "Theory of Computation", "time": "10:00 - 11:00", "class": "5th Sem B", "room": "204", "status": "Affected"},
            {"subject": "UNIX", "name": "UNIX System Programming", "time": "11:00 - 12:00", "class": "5th Sem A", "room": "301", "status": "Affected"}
        ],
        "approval_stage": "waiting_slot",
        "approval_history": [
            {"stage": "Submitted", "completed": True, "date": "15 Sep 2026", "by": "Dr. Ananya"},
            {"stage": "Waiting for Slot", "completed": True, "date": "15 Sep 2026", "info": "Queue #2"},
            {"stage": "HOD Pending", "completed": False, "approver": "Dr. Rahul"},
            {"stage": "Dean Pending", "completed": False, "approver": "Dr. Kumar"},
            {"stage": "Principal Approved", "completed": False, "approver": "Dr. Reddy"}
        ]
    },
    {
        "id": "LV1018",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-09-12",
        "to_date": "2026-09-12",
        "date_display": "12 Sep 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Medical checkup",
        "status": "Waiting for Slot",
        "queue_position": 1,
        "submitted_on": "10 Sep 2026",
        "classes_affected": [
            {"subject": "TOC", "time": "10:00 - 11:00", "class": "5th Sem B", "room": "204"}
        ],
        "approval_stage": "waiting_slot"
    },
    {
        "id": "LV1007",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-09-05",
        "to_date": "2026-09-05",
        "date_display": "05 Sep 2026",
        "type": "ML",
        "type_full": "Medical Leave (ML)",
        "reason": "Viral fever - short notice",
        "status": "Rejected",
        "submitted_on": "04 Sep 2026",
        "classes_affected": [],
        "approval_stage": "rejected"
    },
    {
        "id": "LV1013",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-08-28",
        "to_date": "2026-08-28",
        "date_display": "28 Aug 2026",
        "type": "OD",
        "type_full": "On Duty (OD)",
        "reason": "FDP Conference on AI",
        "status": "Approved",
        "submitted_on": "20 Aug 2026",
        "classes_affected": [],
        "approval_stage": "approved"
    },
    {
        "id": "LV1009",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-08-20",
        "to_date": "2026-08-20",
        "date_display": "20 Aug 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Family function",
        "status": "Approved",
        "submitted_on": "12 Aug 2026",
        "classes_affected": [],
        "approval_stage": "approved"
    },
    {
        "id": "LV1005",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-07-15",
        "to_date": "2026-07-15",
        "date_display": "15 Jul 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Personal work",
        "status": "Approved",
        "submitted_on": "10 Jul 2026",
        "classes_affected": [],
        "approval_stage": "approved"
    },
    {
        "id": "LV1004",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-06-02",
        "to_date": "2026-06-02",
        "date_display": "02 Jun 2026",
        "type": "EL",
        "type_full": "Earned Leave (EL)",
        "reason": "Family vacation",
        "status": "Approved",
        "submitted_on": "25 May 2026",
        "classes_affected": [],
        "approval_stage": "approved"
    },
    {
        "id": "LV1002",
        "faculty_id": "usr_ananya",
        "faculty_name": "Dr. Ananya",
        "department": "CSE(AIML)",
        "from_date": "2026-04-18",
        "to_date": "2026-04-18",
        "date_display": "18 Apr 2026",
        "type": "OD",
        "type_full": "On Duty (OD)",
        "reason": "University workshop",
        "status": "Approved",
        "submitted_on": "12 Apr 2026",
        "classes_affected": [],
        "approval_stage": "approved"
    },
    {
        "id": "LV1027",
        "faculty_id": "usr_dr_b",
        "faculty_name": "Dr. B",
        "department": "CSE(AIML)",
        "from_date": "2026-09-21",
        "to_date": "2026-09-21",
        "date_display": "21 Sep 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Personal",
        "status": "HOD Pending",
        "submitted_on": "16 Sep 2026",
        "classes_affected": [{"subject": "CN", "time": "09:00 - 10:00", "class": "5th Sem A"}],
        "approval_stage": "hod_pending"
    },
    {
        "id": "LV1028",
        "faculty_id": "usr_dr_c",
        "faculty_name": "Dr. C",
        "department": "ECE",
        "from_date": "2026-09-21",
        "to_date": "2026-09-21",
        "date_display": "21 Sep 2026",
        "type": "ML",
        "type_full": "Medical Leave (ML)",
        "reason": "Medical",
        "status": "HOD Pending",
        "submitted_on": "17 Sep 2026",
        "classes_affected": [{"subject": "VLSI", "time": "11:00 - 12:00", "class": "7th Sem"}],
        "approval_stage": "hod_pending"
    },
    {
        "id": "LV1029",
        "faculty_id": "usr_dr_d",
        "faculty_name": "Dr. D",
        "department": "ME",
        "from_date": "2026-09-25",
        "to_date": "2026-09-25",
        "date_display": "25 Sep 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Family function",
        "status": "HOD Pending",
        "submitted_on": "18 Sep 2026",
        "classes_affected": [],
        "approval_stage": "hod_pending"
    },
    {
        "id": "LV1030",
        "faculty_id": "usr_dr_a_alt",
        "faculty_name": "Dr. A",
        "department": "CSE(AIML)",
        "from_date": "2026-09-21",
        "to_date": "2026-09-21",
        "date_display": "21 Sep 2026",
        "type": "CL",
        "type_full": "Casual Leave (CL)",
        "reason": "Academic delegation",
        "status": "Dean Pending",
        "hod_status": "Approved",
        "submitted_on": "14 Sep 2026",
        "classes_affected": [],
        "approval_stage": "dean_pending"
    },
    {
        "id": "LV1031",
        "faculty_id": "usr_dr_e",
        "faculty_name": "Dr. E",
        "department": "ECE",
        "from_date": "2026-09-22",
        "to_date": "2026-09-22",
        "date_display": "22 Sep 2026",
        "type": "ML",
        "type_full": "Medical Leave (ML)",
        "reason": "Dental surgery",
        "status": "Dean Pending",
        "hod_status": "Approved",
        "submitted_on": "15 Sep 2026",
        "classes_affected": [],
        "approval_stage": "dean_pending"
    },
    {
        "id": "LV1032",
        "faculty_id": "usr_dr_f",
        "department": "ME",
        "faculty_name": "Dr. F",
        "from_date": "2026-09-25",
        "to_date": "2026-09-25",
        "date_display": "25 Sep 2026",
        "type": "OD",
        "type_full": "On Duty (OD)",
        "reason": "Conference paper",
        "status": "Dean Pending",
        "hod_status": "Approved",
        "submitted_on": "16 Sep 2026",
        "classes_affected": [],
        "approval_stage": "dean_pending"
    }
]

INITIAL_SLOTS = {
    "total_slots": 3,
    "occupied": 2,
    "available": 1,
    "department": "CSE(AIML)",
    "queue": [
        {"id": 1, "faculty_name": "Dr. B", "leave_date": "21 Sep 2026", "status": "On Approval"},
        {"id": 2, "faculty_name": "Dr. C", "leave_date": "22 Sep 2026", "status": "Waiting"},
        {"id": 3, "faculty_name": "Dr. D", "leave_date": "23 Sep 2026", "status": "Waiting"},
        {"id": 4, "faculty_name": "Dr. E", "leave_date": "25 Sep 2026", "status": "Waiting"}
    ]
}

INITIAL_NOTIFICATIONS = [
    {
        "id": "notif_1",
        "user_id": "usr_ananya",
        "title": "A leave slot has become available!",
        "message": "Your request can now proceed for approval.",
        "time": "10:24 AM",
        "read": False,
        "type": "slot"
    },
    {
        "id": "notif_2",
        "user_id": "usr_ananya",
        "title": "Your queue position changed",
        "message": "You are now #2 in the leave request queue.",
        "time": "09:42 AM",
        "read": False,
        "type": "queue"
    },
    {
        "id": "notif_3",
        "user_id": "usr_ananya",
        "title": "Leave request submitted",
        "message": "Your leave request (#LV1026) has been submitted successfully.",
        "time": "Yesterday",
        "read": True,
        "type": "submit"
    },
    {
        "id": "notif_4",
        "user_id": "usr_ananya",
        "title": "HOD approved your leave",
        "message": "Your leave request (LV1013) has been approved by HOD.",
        "time": "3 days ago",
        "read": True,
        "type": "approved"
    },
    {
        "id": "notif_5",
        "user_id": "usr_ananya",
        "title": "Dean rejected your leave",
        "message": "Your leave request (LV1007) has been rejected by Dean.",
        "time": "5 days ago",
        "read": True,
        "type": "rejected"
    },
    {
        "id": "notif_6",
        "user_id": "usr_ananya",
        "title": "New substitute assigned",
        "message": "Prof. Patil will handle your Computer Networks lecture on 21 Sep.",
        "time": "6 days ago",
        "read": True,
        "type": "substitute"
    },
    {
        "id": "notif_7",
        "user_id": "usr_ananya",
        "title": "Academic calendar updated",
        "message": "Internal Assessment dates for Odd Semester 2026 published.",
        "time": "1 week ago",
        "read": True,
        "type": "info"
    },
    {
        "id": "notif_8",
        "user_id": "usr_ananya",
        "title": "Biometric discrepancy resolved",
        "message": "Attendance record updated for August 15.",
        "time": "2 weeks ago",
        "read": True,
        "type": "info"
    }
]

INITIAL_TIMETABLE = {
    "Mon": [
        {"time": "09:00 - 10:00", "subject": "CN", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "10:00 - 11:00", "subject": "TOC", "class": "5th Sem B", "room": "204", "type": "Lecture"},
        {"time": "11:00 - 12:00", "subject": "UNIX", "class": "5th Sem A", "room": "301", "type": "Lecture"},
        {"time": "12:00 - 01:00", "subject": "LB", "class": "5th Sem B", "room": "204", "type": "Tutorial"},
        {"time": "02:00 - 03:00", "subject": "RMYK", "class": "5th Sem A", "room": "302", "type": "Lecture"},
        {"time": "03:00 - 04:00", "subject": "SOFT-WARE ENG", "class": "5th Sem A", "room": "204", "type": "Lab"}
    ],
    "Tue": [
        {"time": "09:00 - 10:00", "subject": "TOC", "class": "5th Sem B", "room": "204", "type": "Lecture"},
        {"time": "10:00 - 11:00", "subject": "CN", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "11:00 - 01:00", "subject": "NETWORK LAB", "class": "5th Sem A", "room": "Lab 3", "type": "Lab"},
        {"time": "02:00 - 03:00", "subject": "UNIX", "class": "5th Sem B", "room": "301", "type": "Lecture"},
        {"time": "03:00 - 04:00", "subject": "MENTORING", "class": "5th Sem A", "room": "204", "type": "Mentoring"}
    ],
    "Wed": [
        {"time": "09:00 - 10:00", "subject": "UNIX", "class": "5th Sem A", "room": "301", "type": "Lecture"},
        {"time": "10:00 - 11:00", "subject": "CN", "class": "5th Sem B", "room": "204", "type": "Lecture"},
        {"time": "11:00 - 12:00", "subject": "SOFT-WARE ENG", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "02:00 - 04:00", "subject": "PROJECT REVIEW", "class": "7th Sem AIML", "room": "Lab 1", "type": "Project"}
    ],
    "Thu": [
        {"time": "09:00 - 10:00", "subject": "CN", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "10:00 - 11:00", "subject": "TOC", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "11:00 - 01:00", "subject": "UNIX LAB", "class": "5th Sem B", "room": "Lab 2", "type": "Lab"},
        {"time": "02:00 - 03:00", "subject": "RESEARCH HOUR", "class": "Faculty", "room": "Seminar Hall", "type": "Research"}
    ],
    "Fri": [
        {"time": "09:00 - 10:00", "subject": "TOC", "class": "5th Sem B", "room": "204", "type": "Lecture"},
        {"time": "10:00 - 11:00", "subject": "UNIX", "class": "5th Sem A", "room": "301", "type": "Lecture"},
        {"time": "11:00 - 12:00", "subject": "SOFT-WARE ENG", "class": "5th Sem A", "room": "204", "type": "Lecture"},
        {"time": "02:00 - 04:00", "subject": "SEMINAR", "class": "5th Sem A", "room": "Auditorium", "type": "Seminar"}
    ]
}

INITIAL_SUBSTITUTES = [
    {
        "id": "sub_1",
        "faculty_name": "Dr. A",
        "faculty_id": "usr_dr_a_alt",
        "subject": "CN",
        "class": "5A",
        "time": "9:00 - 10:00",
        "date": "2026-09-21",
        "status": "Pending",
        "substitute_assigned": None
    },
    {
        "id": "sub_2",
        "faculty_name": "Dr. B",
        "faculty_id": "usr_dr_b",
        "subject": "TOC",
        "class": "5B",
        "time": "11:00 - 12:00",
        "date": "2026-09-21",
        "status": "Assigned",
        "substitute_assigned": "Dr. Sharma"
    },
    {
        "id": "sub_3",
        "faculty_name": "Dr. C",
        "faculty_id": "usr_dr_c",
        "subject": "UNIX",
        "class": "5A",
        "time": "2:00 - 3:00",
        "date": "2026-09-21",
        "status": "Pending",
        "substitute_assigned": None
    }
]

INITIAL_LEAVE_BALANCE = {
    "usr_ananya": {
        "CL": {"name": "Casual Leave (CL)", "used": 4, "remaining": 6, "total": 10},
        "EL": {"name": "Earned Leave (EL)", "used": 2, "remaining": 8, "total": 10},
        "ML": {"name": "Medical Leave (ML)", "used": 1, "remaining": 9, "total": 10},
        "OD": {"name": "On Duty (OD)", "used": 3, "remaining": 7, "total": 10}
    }
}

PRINCIPAL_METRICS = {
    "pending_final_approval": 7,
    "approved_today": 12,
    "rejected_today": 1,
    "faculty_on_leave": 8,
    "distribution": [
        {"type": "CL", "percent": 45, "count": 18, "color": "#3b82f6"},
        {"type": "ML", "percent": 25, "count": 10, "color": "#10b981"},
        {"type": "OD", "percent": 20, "count": 8, "color": "#f59e0b"},
        {"type": "Other", "percent": 10, "count": 4, "color": "#8b5cf6"}
    ],
    "recent_approvals": [
        {"faculty": "Dr. A", "date": "21 Sep 2026", "status": "Approved"},
        {"faculty": "Dr. E", "date": "21 Sep 2026", "status": "Approved"},
        {"faculty": "Dr. F", "date": "22 Sep 2026", "status": "Approved"},
        {"faculty": "Dr. G", "date": "23 Sep 2026", "status": "Approved"}
    ]
}

CALENDAR_EVENTS = {
    "2026-09-21": {
        "faculty_on_leave": 4,
        "classes_affected": 7,
        "substitutes_acquired": 3,
        "faculty_list": ["Dr. Ananya", "Dr. A", "Dr. B", "Dr. C"],
        "details": "High leave concentration in CSE & ECE."
    },
    "2026-09-22": {
        "faculty_on_leave": 2,
        "classes_affected": 3,
        "substitutes_acquired": 2,
        "faculty_list": ["Dr. E", "Dr. C"],
        "details": "Substitute teachers assigned for all morning slots."
    },
    "2026-09-23": {
        "faculty_on_leave": 1,
        "classes_affected": 2,
        "substitutes_acquired": 1,
        "faculty_list": ["Dr. G"],
        "details": "Normal scheduling flow."
    },
    "2026-09-25": {
        "faculty_on_leave": 3,
        "classes_affected": 5,
        "substitutes_acquired": 3,
        "faculty_list": ["Dr. D", "Dr. F", "Dr. E"],
        "details": "Mechanical & ECE inter-departmental coverage."
    }
}
