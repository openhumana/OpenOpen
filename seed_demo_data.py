"""Seed demo data for taking dashboard screenshots."""
import os
import sys
import json
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from storage import _save_call_history, save_voicemail_url, add_contacts, _user_logs_dir

DEMO_USER_ID = 1  # admin user

def seed():
    d = _user_logs_dir(DEMO_USER_ID)
    os.makedirs(d, exist_ok=True)

    # --- Call History (last 7 days, ~150 calls) ---
    statuses = ["completed", "no_answer", "busy", "voicemail_dropped", "transferred", "failed"]
    status_weights = [25, 15, 5, 35, 15, 5]
    names = ["John Smith", "Maria Garcia", "James Wilson", "Sarah Johnson", "Michael Brown",
             "Emily Davis", "Robert Martinez", "Lisa Anderson", "David Thomas", "Jennifer Lee",
             "William Taylor", "Amanda White", "Christopher Harris", "Jessica Clark", "Daniel Lewis"]
    area_codes = ["212", "310", "415", "305", "512", "720", "404", "617", "206", "702", "503", "312"]

    history = []
    now = datetime.utcnow()
    for i in range(180):
        ts = now - timedelta(hours=random.randint(1, 168), minutes=random.randint(0, 59))
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        ac = random.choice(area_codes)
        num = f"+1{ac}{random.randint(1000000, 9999999)}"
        machine = status in ("voicemail_dropped",)
        transferred = status == "transferred"
        vm_dropped = status == "voicemail_dropped"
        ring_dur = round(random.uniform(2, 25), 1) if status != "failed" else 0

        hangup_map = {
            "completed": "NORMAL_CLEARING",
            "no_answer": "NO_ANSWER",
            "busy": "USER_BUSY",
            "voicemail_dropped": "NORMAL_CLEARING",
            "transferred": "NORMAL_CLEARING",
            "failed": "CALL_REJECTED"
        }

        color_map = {
            "completed": "green",
            "no_answer": "orange",
            "busy": "red",
            "voicemail_dropped": "blue",
            "transferred": "purple",
            "failed": "red"
        }

        desc_map = {
            "completed": "Call completed successfully",
            "no_answer": "No answer after ringing",
            "busy": "Line busy",
            "voicemail_dropped": "Voicemail message dropped",
            "transferred": "Transferred to agent - Hot Lead!",
            "failed": "Call rejected by carrier"
        }

        entry = {
            "call_control_id": f"demo_{i}",
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "number": num,
            "from_number": "+18005551234",
            "status": status,
            "machine_detected": machine,
            "transferred": transferred,
            "voicemail_dropped": vm_dropped,
            "ring_duration": ring_dur,
            "status_description": desc_map[status],
            "status_color": color_map[status],
            "amd_result": "machine_end_beep" if machine else ("human" if transferred else None),
            "hangup_cause": hangup_map[status],
            "transcript": [],
            "recording_url": None,
        }
        history.append(entry)

    history.sort(key=lambda x: x["timestamp"], reverse=True)
    _save_call_history(history, user_id=DEMO_USER_ID)

    # --- Campaigns ---
    campaigns = [
        {"name": "Q1 Lead Outreach", "created": (now - timedelta(days=5)).isoformat(), "status": "completed",
         "total": 250, "dialed": 250, "voicemails": 87, "transfers": 38, "no_answer": 45},
        {"name": "Insurance Renewal", "created": (now - timedelta(days=3)).isoformat(), "status": "completed",
         "total": 180, "dialed": 180, "voicemails": 63, "transfers": 27, "no_answer": 32},
        {"name": "March Follow-ups", "created": (now - timedelta(days=1)).isoformat(), "status": "active",
         "total": 120, "dialed": 84, "voicemails": 29, "transfers": 12, "no_answer": 18},
        {"name": "VIP Client Check-in", "created": (now - timedelta(hours=6)).isoformat(), "status": "paused",
         "total": 45, "dialed": 22, "voicemails": 8, "transfers": 5, "no_answer": 3},
    ]
    camp_file = os.path.join(d, "campaigns.json")
    with open(camp_file, "w") as f:
        json.dump(campaigns, f, indent=2)

    # --- Voicemails ---
    voicemails = [
        {"name": "Default Greeting", "url": "https://example.com/audio/default.wav", "created": (now - timedelta(days=14)).isoformat(), "type": "default"},
        {"name": "Insurance Renewal Notice", "url": "https://example.com/audio/insurance.wav", "created": (now - timedelta(days=7)).isoformat(), "type": "custom"},
        {"name": "Appointment Reminder", "url": "https://example.com/audio/appt.wav", "created": (now - timedelta(days=3)).isoformat(), "type": "custom"},
        {"name": "Follow-up Message", "url": "https://example.com/audio/followup.wav", "created": (now - timedelta(days=1)).isoformat(), "type": "personalized"},
    ]
    vm_file = os.path.join(d, "voicemails.json")
    with open(vm_file, "w") as f:
        json.dump(voicemails, f, indent=2)

    # --- Contacts ---
    contacts = []
    for i, name in enumerate(names):
        ac = random.choice(area_codes)
        contacts.append({
            "id": f"c_{i}",
            "name": name,
            "phone": f"+1{ac}{random.randint(1000000, 9999999)}",
            "email": f"{name.lower().replace(' ', '.')}@example.com",
            "group": random.choice(["Leads", "Clients", "Prospects", "VIP"]),
            "tags": random.sample(["insurance", "renewal", "follow-up", "hot-lead", "callback"], k=random.randint(1, 3)),
            "created": (now - timedelta(days=random.randint(1, 30))).isoformat(),
        })
    contacts_file = os.path.join(d, "contacts.json")
    with open(contacts_file, "w") as f:
        json.dump(contacts, f, indent=2)

    # --- Phone Numbers (owned) ---
    owned_numbers = [
        {"number": "+18005551234", "label": "Main Line", "status": "active", "health_score": 92},
        {"number": "+18005551235", "label": "Sales Line 1", "status": "active", "health_score": 78},
        {"number": "+18005551236", "label": "Sales Line 2", "status": "active", "health_score": 85},
        {"number": "+18005551237", "label": "Support Line", "status": "active", "health_score": 45},
    ]
    nums_file = os.path.join(d, "owned_numbers.json")
    with open(nums_file, "w") as f:
        json.dump(owned_numbers, f, indent=2)

    print(f"Demo data seeded for user {DEMO_USER_ID}")
    print(f"  - {len(history)} call history entries")
    print(f"  - {len(campaigns)} campaigns")
    print(f"  - {len(voicemails)} voicemails")
    print(f"  - {len(contacts)} contacts")
    print(f"  - {len(owned_numbers)} phone numbers")

if __name__ == "__main__":
    seed()
