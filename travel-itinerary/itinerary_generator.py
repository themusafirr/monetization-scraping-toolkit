#!/usr/bin/env python3
"""
Travel Itinerary & Budget Guide Generator
by @the.musafirrr__

Generates sellable 3-Day Travel Itinerary PDFs/HTML for any Indian city.
Includes UPI payment info and Instagram branding.
"""
import sys
import json
from datetime import datetime

# ============================
# CITY DATABASE (expandable)
# ============================
CITY_DATA = {
    "pushkar": {
        "name": "Pushkar",
        "state": "Rajasthan",
        "tagline": "The Sacred Lake Town",
        "best_season": "Oct - Mar",
        "distance_from_delhi": "400 km",
        "days_needed": "2-3 days",
        "image_url": "https://source.unsplash.com/800x600/?pushkar,rajasthan",
        "highlights": [
            "Brahma Temple - one of few in world",
            "Sacred Pushkar Lake & 52 Ghats",
            "Sunset from Savitri Mata Temple",
            "Camel Safari in Thar Desert",
            "Colorful Rajasthani Bazaar"
        ],
        "day_wise": {
            "Day 1": {
                "morning": "Arrival & check-in at Pushkar Palace or Zostel",
                "afternoon": "Brahma Temple + Pushkar Lake parikrama",
                "evening": "Savitri Mata Temple ropeway sunset + Street food (Malpua, Kachori)"
            },
            "Day 2": {
                "morning": "Camel Safari to Sand Dunes (3 hrs)",
                "afternoon": "Lunch at Sunset Café + Shopping at Sadar Bazaar",
                "evening": "Lake aarti + Rajasthani cultural show"
            },
            "Day 3": {
                "morning": "Visit Ajmer Sharif Dargah (15 km)",
                "afternoon": "Ana Sagar Lake + Lunch at Honey & Spice",
                "evening": "Departure"
            }
        },
        "budget": {
            "Stay (budget)": "₹800-1500/night",
            "Stay (mid)": "₹2000-3500/night",
            "Food/day": "₹500-800",
            "Transport": "₹1500-2500 (Delhi-Pushkar bus/train)",
            "Activities": "₹1500 (Camel safari + temple entry)",
            "Total 3D/2N (budget)": "₹5,000-7,000",
            "Total 3D/2N (mid)": "₹12,000-18,000"
        },
        "food": ["Malpua", "Dal Baati Churma", "Pyaaz Kachori", "Lassi at Shri Vasant", "Café Nachiketa"],
        "stay": ["Zostel Pushkar (Hostel)", "Pushkar Palace (Heritage)", "Hotel Green Park Resort"],
        "tips": [
            "Camel safari book morning 7 AM se pehle karein",
            "Baaazar Friday ko closed rahta hai",
            "Leather goods + jewelry sasta milta hai Pushkar mein",
            "Pushkar Lake mein swim mat karein - scared"
        ]
    },
    "udaipur": {
        "name": "Udaipur",
        "state": "Rajasthan",
        "tagline": "City of Lakes",
        "best_season": "Sep - Mar",
        "distance_from_delhi": "660 km",
        "days_needed": "3-4 days",
        "image_url": "https://source.unsplash.com/800x600/?udaipur,rajasthan",
        "highlights": [
            "City Palace - largest in Rajasthan",
            "Lake Pichola boat ride",
            "Jagdish Temple",
            "Sajjangarh Monsoon Palace sunset",
            "Bagore Ki Haveli cultural show"
        ],
        "day_wise": {
            "Day 1": {
                "morning": "Arrival + check-in at Lake Pichola facing hotel",
                "afternoon": "City Palace tour (2-3 hrs)",
                "evening": "Lake Pichola boat ride sunset + Jagdish Temple"
            },
            "Day 2": {
                "morning": "Sajjangarh Monsoon Palace (early morning)",
                "afternoon": "Saheliyon Ki Bari + Lunch at Ambrai",
                "evening": "Bagore Ki Haveli cultural show"
            },
            "Day 3": {
                "morning": "Visit Kumbhalgarh Fort (Day trip, 85 km)",
                "afternoon": "Return + shopping at Hathi Pol Bazaar",
                "evening": "Rooftop dinner at Jaiwana Haveli"
            }
        },
        "budget": {
            "Stay (budget)": "₹1000-1800/night",
            "Stay (mid)": "₹2500-5000/night",
            "Food/day": "₹600-1000",
            "Transport": "₹2000-3500 (Train/Bus)",
            "Activities": "₹2000 (Palace + boat + show)",
            "Total 3D/2N (budget)": "₹7,000-9,000",
            "Total 3D/2N (mid)": "₹15,000-22,000"
        },
        "food": ["Dal Baati", "Gatte ki Sabzi", "Mawa Kachori", "Ambrai restaurant", "Café Edelweiss"],
        "stay": ["Zostel Udaipur (Hostel)", "Hotel Lake Pichola", "Jagat Niwas Palace"],
        "tips": [
            "Boat ride sunset time 5:30 PM ko book karein",
            "Monsoon Palace jaane ke liye auto full day rent lo",
            "City Palace combo ticket lein (sasta padta hai)",
            "Rooftop lake-facing restaurants mein dinner karo"
        ]
    },
    "jaipur": {
        "name": "Jaipur",
        "state": "Rajasthan",
        "tagline": "The Pink City",
        "best_season": "Oct - Mar",
        "distance_from_delhi": "280 km",
        "days_needed": "2-3 days",
        "image_url": "https://source.unsplash.com/800x600/?jaipur,pink,rajasthan",
        "highlights": [
            "Hawa Mahal - icon of Jaipur",
            "Amber Fort & Nahargarh",
            "City Palace & Jantar Mantar",
            "Albert Hall Museum",
            "Johari Bazaar & Bapu Bazaar shopping"
        ],
        "day_wise": {
            "Day 1": {
                "morning": "Arrival + Amber Fort (early morning)",
                "afternoon": "Jal Mahal + Nahargarh sunset",
                "evening": "Hawa Mahal + local dinner"
            },
            "Day 2": {
                "morning": "City Palace + Jantar Mantar",
                "afternoon": "Albert Hall Museum + Lunch at Chokhi Dhani",
                "evening": "Shopping at Johari Bazaar (jewelry + textiles)"
            },
            "Day 3": {
                "morning": "Local breakfast at Laxmi Mishtan Bhandar",
                "afternoon": "Monkey Temple (Galta Ji) + stepwell visit",
                "evening": "Departure"
            }
        },
        "budget": {
            "Stay (budget)": "₹800-1500/night",
            "Stay (mid)": "₹2000-4000/night",
            "Food/day": "₹500-900",
            "Transport": "₹1000-2000 (Train/Bus)",
            "Activities": "₹1800 (Forts + palace + museum)",
            "Total 3D/2N (budget)": "₹5,500-8,000",
            "Total 3D/2N (mid)": "₹13,000-18,000"
        },
        "food": ["Pyaaz Kachori at Rawat Mishthan", "Dal Baati Churma at Chokhi Dhani", "Lassi at Lassiwala", "Laal Maas"],
        "stay": ["Zostel Jaipur", "Hotel Pearl Palace", "Samode Haveli (Heritage)"],
        "tips": [
            "Amber Fort early morning 8 AM jaao (cooler + fewer crowds)",
            "Rickshaw poora day rent lo - sasta padta hai",
            "Johari Bazaar closed on Sundays",
            "Chokhi Dhani dinner advance book karein"
        ]
    }
}

# ============================
# HTML TEMPLATE GENERATOR
# ============================
def generate_itinerary_html(city_key):
    city = CITY_DATA.get(city_key.lower())
    if not city:
        return None, f"City '{city_key}' not found. Available: {', '.join(CITY_DATA.keys())}"

    today = datetime.now().strftime("%d %b %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{city['name']} Travel Itinerary - 3 Day Guide by @the.musafirrr__</title>
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1e293b;
    background: #f8fafc;
    padding: 20px;
  }}
  .container {{ max-width: 800px; margin: 0 auto; background: white; }}

  /* HEADER */
  .header {{
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 40px 30px;
    text-align: center;
    position: relative;
  }}
  .brand {{
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
  }}
  .tagline {{
    font-size: 12px;
    letter-spacing: 3px;
    opacity: 0.9;
    margin-bottom: 10px;
  }}
  h1 {{
    font-size: 56px;
    font-weight: 900;
    margin: 10px 0;
    text-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }}
  .subtitle {{
    font-size: 18px;
    font-style: italic;
    opacity: 0.95;
  }}
  .meta {{
    display: flex;
    justify-content: space-around;
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.3);
    font-size: 13px;
  }}

  /* SECTIONS */
  .section {{ padding: 30px; }}
  .section h2 {{
    font-size: 28px;
    color: #0f172a;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 3px solid #f59e0b;
  }}

  /* HIGHLIGHTS */
  .highlights {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 15px;
  }}
  .highlight {{
    background: #fef3c7;
    padding: 12px 15px;
    border-left: 4px solid #f59e0b;
    border-radius: 4px;
    font-size: 14px;
  }}
  .highlight::before {{ content: "✈️ "; }}

  /* DAY CARDS */
  .day-card {{
    background: #f1f5f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    border-left: 5px solid #f59e0b;
  }}
  .day-title {{
    font-size: 20px;
    font-weight: 700;
    color: #d97706;
    margin-bottom: 12px;
  }}
  .slot {{
    margin: 8px 0;
    padding: 8px 0;
    border-bottom: 1px dashed #cbd5e1;
  }}
  .slot:last-child {{ border-bottom: none; }}
  .slot-label {{
    font-weight: 700;
    color: #0f172a;
    display: inline-block;
    width: 100px;
  }}

  /* BUDGET TABLE */
  .budget-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }}
  .budget-table td {{
    padding: 10px 12px;
    border-bottom: 1px solid #e2e8f0;
    font-size: 14px;
  }}
  .budget-table td:first-child {{ font-weight: 600; color: #475569; }}
  .budget-table td:last-child {{ text-align: right; font-weight: 700; color: #d97706; }}
  .budget-table tr.total {{
    background: #fef3c7;
    font-size: 15px;
  }}
  .budget-table tr.total td {{ font-weight: 800; font-size: 16px; }}

  /* INFO GRID */
  .info-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 15px 0;
  }}
  .info-card {{
    background: #f8fafc;
    padding: 15px;
    border-radius: 6px;
    border-top: 3px solid #f59e0b;
  }}
  .info-card h3 {{
    font-size: 13px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}
  .info-card ul {{ list-style: none; padding: 0; }}
  .info-card li {{
    font-size: 13px;
    padding: 4px 0;
    color: #334155;
  }}
  .info-card li::before {{ content: "• "; color: #f59e0b; font-weight: bold; }}

  /* TIPS */
  .tips {{
    background: #fff7ed;
    padding: 20px;
    border-radius: 6px;
    border-left: 4px solid #ea580c;
  }}
  .tips ul {{ list-style: none; padding: 0; margin-top: 10px; }}
  .tips li {{
    padding: 6px 0;
    font-size: 14px;
    color: #7c2d12;
  }}
  .tips li::before {{ content: "💡 "; }}

  /* PAYMENT SECTION */
  .payment {{
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    padding: 35px 30px;
    text-align: center;
  }}
  .payment h2 {{
    color: #f59e0b;
    font-size: 24px;
    margin-bottom: 15px;
  }}
  .upi-id {{
    background: rgba(245, 158, 11, 0.2);
    border: 2px dashed #f59e0b;
    padding: 15px 25px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #fbbf24;
    display: inline-block;
    margin: 15px 0;
  }}
  .price {{
    font-size: 36px;
    font-weight: 900;
    color: white;
    margin: 10px 0;
  }}
  .price-strike {{
    text-decoration: line-through;
    color: #94a3b8;
    font-size: 18px;
  }}

  /* FOOTER */
  .footer {{
    background: #f8fafc;
    padding: 25px 30px;
    text-align: center;
    border-top: 1px solid #e2e8f0;
  }}
  .footer .ig {{
    color: #f59e0b;
    font-weight: 700;
    font-size: 18px;
  }}
  .footer .small {{
    font-size: 12px;
    color: #64748b;
    margin-top: 8px;
  }}

  @media print {{
    body {{ padding: 0; }}
    .payment {{ page-break-before: always; }}
  }}
</style>
</head>
<body>
<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="brand">@the.musafirrr__</div>
    <div class="tagline">THE MUSAFIR • TRAVEL GUIDE</div>
    <h1>{city['name']}</h1>
    <div class="subtitle">{city['tagline']} • {city['state']}</div>
    <div class="meta">
      <div>📅 {city['best_season']}</div>
      <div>🚗 {city['distance_from_delhi']} from Delhi</div>
      <div>⏱️ {city['days_needed']}</div>
    </div>
  </div>

  <!-- HIGHLIGHTS -->
  <div class="section">
    <h2>Must-Do Highlights</h2>
    <div class="highlights">
"""

    for h in city['highlights']:
        html += f'      <div class="highlight">{h}</div>\n'

    html += """    </div>
  </div>

  <!-- 3-DAY PLAN -->
  <div class="section">
    <h2>3-Day Itinerary</h2>
"""

    for day, slots in city['day_wise'].items():
        html += f'    <div class="day-card">\n'
        html += f'      <div class="day-title">📍 {day}</div>\n'
        for time, activity in slots.items():
            html += f'      <div class="slot"><span class="slot-label">{time.upper()}:</span>{activity}</div>\n'
        html += '    </div>\n'

    html += """  </div>

  <!-- BUDGET -->
  <div class="section">
    <h2>Budget Breakdown</h2>
    <table class="budget-table">
"""
    for item, cost in city['budget'].items():
        is_total = 'Total' in item
        tr_class = ' class="total"' if is_total else ''
        html += f'      <tr{tr_class}><td>{item}</td><td>{cost}</td></tr>\n'

    html += """    </table>
  </div>

  <!-- FOOD & STAY -->
  <div class="section">
    <h2>Food & Stay Picks</h2>
    <div class="info-grid">
      <div class="info-card">
        <h3>🍽️ Must-Try Food</h3>
        <ul>
"""
    for f in city['food']:
        html += f'          <li>{f}</li>\n'

    html += """        </ul>
      </div>
      <div class="info-card">
        <h3>🏨 Stay Options</h3>
        <ul>
"""
    for s in city['stay']:
        html += f'          <li>{s}</li>\n'

    html += """        </ul>
      </div>
    </div>
  </div>

  <!-- PRO TIPS -->
  <div class="section">
    <h2>Pro Tips</h2>
    <div class="tips">
      <ul>
"""
    for tip in city['tips']:
        html += f'        <li>{tip}</li>\n'

    html += f"""      </ul>
    </div>
  </div>

  <!-- PAYMENT / SELL PAGE -->
  <div class="payment">
    <h2>🌍 Want a Custom Itinerary?</h2>
    <p style="margin-top:10px; opacity:0.9;">Apne budget aur dates ke hisaab se personalized plan</p>
    <div class="price">
      <span class="price-strike">₹999</span> ₹499
    </div>
    <p style="font-size:14px; opacity:0.85; margin-top:5px;">One-time payment • Instant PDF delivery</p>

    <div style="margin-top: 20px;">
      <p style="font-size:14px; opacity:0.85;">Pay via UPI:</p>
      <div class="upi-id">9649228281@yescred</div>
      <p style="font-size:13px; opacity:0.7;">Screenshot payment ka bhejo Instagram DM</p>
    </div>

    <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
      <p style="font-size:14px;">📩 Order on Instagram:</p>
      <div style="font-size:20px; font-weight:700; color:#fbbf24; margin-top:8px;">@the.musafirrr__</div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="ig">@the.musafirrr__</div>
    <div class="small">Follow for more city guides • Generated {today}</div>
    <div class="small" style="margin-top:5px;">Made with ❤️ by The Musafir</div>
  </div>

</div>
</body>
</html>"""

    return html, None


# ============================
# CLI ENTRY POINT
# ============================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n❌ Usage: python3 itinerary_generator.py <city>")
        print(f"\nAvailable cities: {', '.join(CITY_DATA.keys())}\n")
        sys.exit(1)

    city = sys.argv[1]
    html, error = generate_itinerary_html(city)

    if error:
        print(f"❌ {error}")
        sys.exit(1)

    output_file = f"/home/ubuntu/projects/09-monetization/travel-itinerary/previews/{city.lower()}_itinerary.html"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✅ Generated: {output_file}")
    print(f"📄 City: {CITY_DATA[city.lower()]['name']}")
    print(f"💰 Sell price: ₹499 (UPI: 9649228281@yescred)")