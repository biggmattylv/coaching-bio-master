#!/usr/bin/env python3
"""CoachingBio Card Generator — Creates coach bio pages from form data."""

import json
import os
from datetime import datetime

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | CoachingBio.com</title>
    <meta property="og:title" content="{name} | CoachingBio">
    <meta property="og:description" content="{bio_short}">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #002244; --accent: #FF5E5E; --white: #FFFFFF; --bg: #f8f9fa; }}
        body {{ font-family: 'Roboto', sans-serif; background: var(--bg); color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: var(--white); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; padding: 60px 20px; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=1200'); background-size: cover; background-position: center; color: white; }}
        h1 {{ margin: 10px 0; font-size: 2em; }}
        .title {{ text-transform: uppercase; letter-spacing: 2px; font-size: 0.9em; font-weight: bold; opacity: 0.8; }}
        .content {{ padding: 30px; }}
        .card {{ background: #fff; border: 1px solid #eee; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
        h2 {{ color: var(--primary); font-size: 1.2em; border-left: 4px solid var(--primary); padding-left: 10px; margin-top: 0; }}
        .contact-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }}
        .icon-btn {{ display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f0f0f0; padding: 12px; border-radius: 8px; text-decoration: none; color: #333; font-size: 0.75em; font-weight: bold; }}
        .icon-btn svg {{ width: 24px; height: 24px; margin-bottom: 5px; fill: var(--primary); }}
        .social-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
        .social-btn {{ display: flex; align-items: center; justify-content: center; background: var(--primary); color: white; padding: 10px; border-radius: 8px; text-decoration: none; font-size: 0.8em; font-weight: bold; }}
        .btn {{ display: block; background: var(--accent); color: white; padding: 12px; border-radius: 8px; text-align: center; text-decoration: none; font-weight: bold; font-size: 0.9em; margin-top: 10px; }}
        .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: center; }}
        .stat {{ background: #f0f0f0; padding: 15px; border-radius: 8px; }}
        .stat-num {{ font-size: 2em; font-weight: 900; color: var(--primary); }}
        .stat-label {{ font-size: 0.8em; color: #666; }}
        .footer {{ text-align: center; padding: 20px; font-size: 0.8em; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{name}</h1>
            <p class="title">{specialty} | {team} | {city}</p>
        </header>
        <main class="content">
            <div class="card">
                <h2>Direct Line</h2>
                <div class="contact-grid">
                    <a href="tel:{phone_raw}" class="icon-btn">
                        <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.15 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                        Call
                    </a>
                    <a href="sms:{phone_raw}" class="icon-btn">
                        <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 11H7V9h2v2zm4 0h-2V9h2v2zm4 0h-2V9h2v2z"/></svg>
                        Text
                    </a>
                    <a href="mailto:{email}" class="icon-btn">
                        <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                        Email
                    </a>
                </div>
            </div>

            {stats_section}

            <div class="card">
                <h2>About the Coach</h2>
                <p>{bio}</p>
            </div>

            {social_section}

            {booking_section}

            {payment_section}
        </main>
        <div class="footer">
            Powered by CoachingBio.com
        </div>
    </div>
</body>
</html>'''

def generate_card(form_data):
    """Generate a coach bio card HTML from form data."""
    name = form_data.get("name", "Coach")
    email = form_data.get("email", "")
    sport = form_data.get("sport", "")
    specialty = form_data.get("specialty", f"{sport} Coach")
    team = form_data.get("team", "")
    city = form_data.get("city", "Las Vegas")
    phone = form_data.get("phone", "")
    booking = form_data.get("booking", "")
    payment = form_data.get("payment", "")
    bio = form_data.get("bio", "")
    years = form_data.get("years", "")
    team_colors = form_data.get("team_colors", "")
    
    # Social links
    fb = form_data.get("fb", "")
    insta = form_data.get("insta", "")
    tiktok = form_data.get("tiktok", "")
    twitter = form_data.get("twitter", "")
    youtube = form_data.get("youtube", "")
    
    phone_raw = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    
    bio_short = bio[:100] if bio else f"{specialty} in {city}. Book your session today."
    
    # Stats section
    stats_section = ""
    if years:
        stats_section = f'''
            <div class="card">
                <h2>By The Numbers</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-num">{years}</div>
                        <div class="stat-label">Years Coaching</div>
                    </div>
                    <div class="stat">
                        <div class="stat-num">{sport}</div>
                        <div class="stat-label">Sport</div>
                    </div>
                </div>
            </div>'''
    
    # Social section
    social_links = []
    if fb: social_links.append(f'<a href="{fb}" class="social-btn">Facebook</a>')
    if insta: social_links.append(f'<a href="{insta}" class="social-btn">Instagram</a>')
    if tiktok: social_links.append(f'<a href="{tiktok}" class="social-btn">TikTok</a>')
    if twitter: social_links.append(f'<a href="{twitter}" class="social-btn">Twitter/X</a>')
    if youtube: social_links.append(f'<a href="{youtube}" class="social-btn">YouTube</a>')
    
    social_section = ""
    if social_links:
        social_section = f'''
            <div class="card">
                <h2>Follow the Coach</h2>
                <div class="social-grid">{"".join(social_links)}</div>
            </div>'''
    
    # Booking section
    booking_section = ""
    if booking:
        booking_section = f'''
            <div class="card">
                <h2>Book a Session</h2>
                <a href="{booking}" class="btn">Schedule Now</a>
            </div>'''
    
    # Payment section
    payment_section = ""
    if payment:
        payment_section = f'''
            <div class="card">
                <h2>Payment</h2>
                <p>Venmo/Zelle: <strong>{payment}</strong></p>
            </div>'''
    
    html = TEMPLATE.format(
        name=name,
        specialty=specialty,
        team=team,
        city=city,
        phone_raw=phone_raw,
        email=email,
        bio=bio or f"{specialty} with {years} years of experience." if years else f"{specialty} based in {city}.",
        bio_short=bio_short,
        stats_section=stats_section,
        social_section=social_section,
        booking_section=booking_section,
        payment_section=payment_section
    )
    
    return html

def save_card(html, coach_slug, dist_dir="/home/sophie-msvegas/coaching-bio-master/dist"):
    """Save the generated card to the dist directory."""
    os.makedirs(dist_dir, exist_ok=True)
    filepath = os.path.join(dist_dir, f"{coach_slug}.html")
    with open(filepath, "w") as f:
        f.write(html)
    return filepath

def update_coaches_json(name, slug, city="", state="", sport="", dist_dir="/home/sophie-msvegas/coaching-bio-master/dist"):
    """Add coach to the directory JSON."""
    json_path = os.path.join(dist_dir, "coaches.json")
    
    coaches = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            coaches = json.load(f)
    
    # Check if already exists
    if any(c.get("link") == f"{slug}.html" for c in coaches):
        return
    
    coaches.append({
        "name": name,
        "city": city,
        "state": state,
        "sport": sport,
        "link": f"{slug}.html"
    })
    
    with open(json_path, "w") as f:
        json.dump(coaches, f, indent=2)

def generate_welcome_email(name, card_url, sport):
    """Generate the welcome email text."""
    return f"""Hi {name},

Your CoachingBio Digital Authority Card is LIVE!

View your card: {card_url}

YOUR FREE CARD INCLUDES:
• Professional bio page with your photo and contact info
• Direct call, text, and email buttons
• Social media links
• Listing in the "Find My Coach" directory

WHAT YOU CAN DO WITH IT:
• Share the link in your Instagram bio
• Send it to parents before tryouts
• Add it to your email signature
• Use it as your digital business card

NEED CHANGES? Just reply to this email with what you want to update (colors, bio text, links) and we'll handle it.

WANT MORE? Upgrade options:
• All-Star ($19.99/mo): Add scheduling + payment collection
• Hall of Fame ($199/mo): Full social media management

Welcome to the Inner Circle.

— Sophie
CoachingBio.com"""

if __name__ == "__main__":
    # Test with sample data
    sample = {
        "name": "Coach Mike Johnson",
        "email": "mike@example.com",
        "sport": "Baseball",
        "specialty": "Pitching Coach",
        "team": "LV Lightning",
        "city": "Las Vegas",
        "phone": "702-555-0123",
        "bio": "Former minor league pitcher with 12 years of coaching experience. Specializing in mechanics and mental game for competitive travel ball players.",
        "years": "12",
        "insta": "https://instagram.com/coachmike",
        "payment": "@mike-johnson"
    }
    
    html = generate_card(sample)
    slug = "coach-mike-johnson"
    save_card(html, slug)
    update_coaches_json(sample["name"], slug, sample["city"], "NV", sample["sport"])
    print(f"Generated: {slug}.html")
    print(f"Welcome email:")
    print(generate_welcome_email(sample["name"], f"https://coachingbio.com/{slug}.html", sample["sport"]))
