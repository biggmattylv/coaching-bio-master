#!/usr/bin/env python3
"""CoachingBio Form Intake — Processes Netlify form submissions and generates cards."""

import json
import os
import sys
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Add parent to path for card generator
sys.path.insert(0, os.path.dirname(__file__))
from card_generator import generate_card, save_card, update_coaches_json, generate_welcome_email

SUBMISSIONS_LOG = "/home/sophie-msvegas/coaching-bio-master/data/submissions.json"
CARDS_DIR = "/home/sophie-msvegas/coaching-bio-master/dist"
DATA_DIR = "/home/sophie-msvegas/coaching-bio-master/data"

def slugify(name):
    """Convert name to URL-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = slug.strip('-')
    return slug

def load_submissions():
    """Load existing submissions."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(SUBMISSIONS_LOG):
        with open(SUBMISSIONS_LOG) as f:
            return json.load(f)
    return []

def save_submissions(submissions):
    """Save submissions."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SUBMISSIONS_LOG, "w") as f:
        json.dump(submissions, f, indent=2)

def process_submission(form_data):
    """Process a single form submission."""
    submissions = load_submissions()
    
    name = form_data.get("name", "").strip()
    email = form_data.get("email", "").strip()
    
    if not name or not email:
        return {"error": "Name and email required"}
    
    slug = slugify(name)
    
    # Check for duplicate
    if any(s.get("email") == email and s.get("name") == name for s in submissions):
        return {"error": "Already processed", "slug": slug}
    
    # Generate card
    html = generate_card(form_data)
    filepath = save_card(html, slug)
    
    # Update directory
    city = form_data.get("city", "")
    sport = form_data.get("sport", "")
    update_coaches_json(name, slug, city, "NV", sport)
    
    # Log submission
    record = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "sport": sport,
        "city": city,
        "slug": slug,
        "card_url": f"https://coachingbio.com/{slug}.html",
        "status": "card_generated",
        "email_sent": False
    }
    submissions.append(record)
    save_submissions(submissions)
    
    return record

def get_pending_customizations():
    """Get submissions that need customization follow-up."""
    submissions = load_submissions()
    return [s for s in submissions if s.get("status") == "card_generated"]

def get_dashboard_data():
    """Get data for the coaching dashboard."""
    submissions = load_submissions()
    
    total = len(submissions)
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = sum(1 for s in submissions if s.get("timestamp", "").startswith(today))
    
    sports = {}
    cities = {}
    for s in submissions:
        sport = s.get("sport", "Unknown")
        city = s.get("city", "Unknown")
        sports[sport] = sports.get(sport, 0) + 1
        cities[city] = cities.get(city, 0) + 1
    
    return {
        "total_signups": total,
        "today_signups": today_count,
        "by_sport": sports,
        "by_city": cities,
        "recent": submissions[-10:] if submissions else [],
        "pending_customization": len(get_pending_customizations())
    }

if __name__ == "__main__":
    # Test
    dashboard = get_dashboard_data()
    print(json.dumps(dashboard, indent=2))
