#!/usr/bin/env python3
"""CoachingBio Google Sheets CRM — Tracks coaches until they upgrade to paid."""

import json
import os
from datetime import datetime

CRM_FILE = "/home/sophie-msvegas/coaching-bio-master/data/coach_crm.json"

def load_crm():
    """Load CRM data."""
    os.makedirs(os.path.dirname(CRM_FILE), exist_ok=True)
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE) as f:
            return json.load(f)
    return []

def save_crm(data):
    """Save CRM data."""
    os.makedirs(os.path.dirname(CRM_FILE), exist_ok=True)
    with open(CRM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_coach(name, email, sport, phone="", city="", status="free_card", notes=""):
    """Add a coach to the CRM."""
    crm = load_crm()
    
    # Check for duplicate
    if any(c.get("email") == email for c in crm):
        return {"error": "Already in CRM"}
    
    coach = {
        "id": len(crm) + 1,
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "sport": sport,
        "phone": phone,
        "city": city,
        "status": status,  # free_card, warm_lead, allstar, hof
        "card_url": f"https://coachingbio.com/{name.lower().replace(' ', '-')}.html",
        "notes": notes,
        "last_contact": datetime.now().isoformat(),
        "customizations_requested": [],
        "upgrade_offered": False,
        "upgrade_date": None
    }
    crm.append(coach)
    save_crm(crm)
    return coach

def update_status(coach_id, new_status):
    """Update coach status (e.g., from free_card to warm_lead)."""
    crm = load_crm()
    for c in crm:
        if c["id"] == coach_id:
            c["status"] = new_status
            c["last_contact"] = datetime.now().isoformat()
            save_crm(crm)
            return c
    return None

def add_note(coach_id, note):
    """Add a note to a coach."""
    crm = load_crm()
    for c in crm:
        if c["id"] == coach_id:
            c["notes"] = f"{c.get('notes', '')}\n[{datetime.now().strftime('%m/%d')}] {note}"
            c["last_contact"] = datetime.now().isoformat()
            save_crm(crm)
            return c
    return None

def request_customization(coach_id, request_text):
    """Log a customization request."""
    crm = load_crm()
    for c in crm:
        if c["id"] == coach_id:
            c["customizations_requested"].append({
                "date": datetime.now().isoformat(),
                "request": request_text,
                "status": "pending"
            })
            c["last_contact"] = datetime.now().isoformat()
            save_crm(crm)
            return c
    return None

def get_pipeline():
    """Get the revenue pipeline summary."""
    crm = load_crm()
    return {
        "total": len(crm),
        "free_card": sum(1 for c in crm if c["status"] == "free_card"),
        "warm_lead": sum(1 for c in crm if c["status"] == "warm_lead"),
        "allstar": sum(1 for c in crm if c["status"] == "allstar"),
        "hof": sum(1 for c in crm if c["status"] == "hof"),
        "pending_customizations": sum(
            1 for c in crm 
            for req in c.get("customizations_requested", []) 
            if req["status"] == "pending"
        ),
        "recent": sorted(crm, key=lambda x: x.get("last_contact", ""), reverse=True)[:10]
    }

def export_for_google_sheets():
    """Export CRM data in a format ready for Google Sheets."""
    crm = load_crm()
    headers = ["ID", "Name", "Email", "Sport", "Phone", "City", "Status", "Card URL", "Last Contact", "Notes"]
    rows = []
    for c in crm:
        rows.append([
            c["id"],
            c["name"],
            c["email"],
            c["sport"],
            c.get("phone", ""),
            c.get("city", ""),
            c["status"],
            c.get("card_url", ""),
            c.get("last_contact", "")[:10],
            c.get("notes", "")[:100]
        ])
    return {"headers": headers, "rows": rows}

if __name__ == "__main__":
    # Test: Add Charles Card
    coach = add_coach(
        name="Charles Card",
        email="charles@bombsquadbaseball.com",
        sport="Baseball",
        phone="702-XXX-1234",
        city="Las Vegas",
        status="free_card",
        notes="Guinea pig — doing everything free to show value. Owner of Bomb Squad 14-16U & Adult 18+."
    )
    print("Added:", coach["name"])
    print("\nPipeline:")
    print(json.dumps(get_pipeline(), indent=2))
