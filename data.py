import pandas as pd
import numpy as np
import hashlib
import streamlit as st # pyright: ignore[reportMissingImports]
from datetime import datetime

# ── Shared CSS applied across all pages ───────────────────────────────────────
def apply_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, sans-serif !important;
    }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
    .stDeployButton { display: none !important; }

    /* ── Sidebar dark ── */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #0F172A !important;
    }
    [data-testid="stSidebarNav"] a {
        color: #94A3B8 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,107,53,0.15) !important;
        color: #FF6B35 !important;
    }
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: rgba(255,107,53,0.2) !important;
        color: #FF6B35 !important;
        font-weight: 700 !important;
        border-left: 3px solid #FF6B35 !important;
    }

    /* ── Main layout ── */
    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1350px !important;
    }

    /* ── Stat cards ── */
    .stat-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 22px 16px !important;
        text-align: center !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important, 0 4px 20px rgba(0,0,0,0.07) !important;
        border-top: 4px solid #FF6B35 !important;
    }
    .stat-num   { font-size: 2.4rem !important; font-weight: 900 !important; color: #FF6B35 !important; letter-spacing: -1px !important; line-height: 1.1 !important; }
    .stat-sub   { font-size: 0.72rem !important; color: #43A047 !important; font-weight: 600 !important; margin-top: 4px !important; }
    .stat-label { font-size: 0.73rem !important; color: #9CA3AF !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; margin-top: 6px !important; }

    /* ── Problem / Solution cards ── */
    .problem-card {
        background: #FFF5F0 !important;
        border: 1.5px solid #FF6B35 !important;
        border-radius: 16px !important;
        padding: 28px 26px !important;
        height: 100% !important;
    }
    .solution-card {
        background: #F0FFF4 !important;
        border: 1.5px solid #43A047 !important;
        border-radius: 16px !important;
        padding: 28px 26px !important;
        height: 100% !important;
    }

    /* ── Step cards ── */
    .step-card {
        background: white !important;
        border-radius: 14px !important;
        padding: 22px 18px !important;
        text-align: center !important;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06) !important;
        border-bottom: 3px solid #FF6B35 !important;
        height: 100% !important;
    }
    .step-icon {
        width: 46px !important; height: 46px !important;
        background: linear-gradient(135deg, #FF6B35, #FF8C61) !important;
        border-radius: 50% !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        margin: 0 auto 12px !important;
        font-size: 1.3rem !important;
        color: white !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 12px rgba(255,107,53,0.35) !important;
    }

    /* ── Recommendation cards ── */
    .rec-gold  { background: linear-gradient(135deg,#FFFDE7,#FFF9C4) !important; border: 2px solid #F9A825 !important; border-radius: 16px !important; padding: 24px !important; margin-bottom: 14px !important; }
    .rec-green { background: linear-gradient(135deg,#E8F5E9,#F1F8E9) !important; border: 2px solid #43A047 !important; border-radius: 16px !important; padding: 24px !important; margin-bottom: 14px !important; }
    .rec-blue  { background: linear-gradient(135deg,#E3F2FD,#EDE7F6) !important; border: 2px solid #1E88E5 !important; border-radius: 16px !important; padding: 24px !important; margin-bottom: 14px !important; }

    /* ── Tags ── */
    .tag {
        display: inline-block !important;
        padding: 3px 11px !important;
        border-radius: 20px !important;
        font-size: 0.73rem !important;
        font-weight: 600 !important;
        margin-right: 5px !important;
        margin-bottom: 4px !important;
    }
    .tag-orange { background:#FFF3E0 !important; color:#E65100 !important; }
    .tag-green  { background:#E8F5E9 !important; color:#2E7D32 !important; }
    .tag-blue   { background:#E3F2FD !important; color:#1565C0 !important; }
    .tag-gray   { background:#F1F5F9 !important; color:#475569 !important; }

    /* ── Nav cards on Home ── */
    .nav-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 18px 16px !important;
        border-left: 4px solid #FF6B35 !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px !important;
        font-size: 0.9rem !important;
    }

    /* ── Zone cards and recommendation wrappers ── */
    .zone-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 22px 22px 18px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        min-height: 180px !important;
    }
    .zone-best { border-color: #2E7D32 !important; }
    .zone-good { border-color: #1565C0 !important; }
    .zone-okay { border-color: #E65100 !important; }
    .zone-avoid { border-color: #C62828 !important; }

    .earn-main {
        background: white !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 2px 18px rgba(0,0,0,0.07) !important;
        border: 1px solid rgba(15,23,42,0.08) !important;
    }
    .sc-bad, .sc-normal, .sc-great {
        background: white !important;
        border-radius: 18px !important;
        padding: 18px !important;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06) !important;
        border: 1px solid rgba(15,23,42,0.08) !important;
    }

    @media only screen and (max-width: 600px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .stat-card, .problem-card, .solution-card, .step-card,
        .rec-gold, .rec-green, .rec-blue, .nav-card,
        .zone-card, .earn-main, .sc-bad, .sc-normal, .sc-great {
            width: 100% !important;
            min-width: auto !important;
            box-sizing: border-box !important;
        }
        .zone-card {
            padding: 18px !important;
        }
        .sc-bad, .sc-normal, .sc-great {
            margin-bottom: 14px !important;
        }
        .stPlotlyChart, .stChart, figure {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────
MARKETS = pd.DataFrame({
    'Market Name': [
        'Malakpet Sunday Market', 'Kukatpally Weekly Bazaar', 'HITEC City Food Fest',
        'Jubilee Hills Exhibition', 'Madhapur Night Market', 'Secunderabad Grand Fair',
        'Banjara Hills Farmers Market', 'LB Nagar Weekend Market',
        'Ameerpet Food Street', 'Gachibowli Tech Park Fair'
    ],
    'Area': [
        'Malakpet', 'Kukatpally', 'HITEC City', 'Jubilee Hills', 'Madhapur',
        'Secunderabad', 'Banjara Hills', 'LB Nagar', 'Ameerpet', 'Gachibowli'
    ],
    'Day': [
        'Sunday', 'Saturday', 'Friday', 'Sat-Sun', 'Thu-Fri',
        'Sunday', 'Saturday', 'Sat-Sun', 'Wednesday', 'Saturday'
    ],
    'Expected Footfall': [4200, 3800, 5500, 6200, 4800, 3500, 2900, 3200, 2600, 4100],
    'Stall Price': [800, 750, 1200, 1500, 1000, 700, 900, 800, 650, 1100],
    'Total Stalls': [44, 36, 60, 72, 52, 36, 28, 40, 32, 48],
    'Available Stalls': [12, 8, 24, 18, 10, 15, 9, 20, 7, 22],
    'Type': [
        'Weekly Market', 'Weekly Market', 'Food Festival', 'Exhibition', 'Night Market',
        'Fair', 'Farmers Market', 'Weekly Market', 'Food Street', 'Tech Park Fair'
    ],
    'Lat': [17.3616, 17.4849, 17.4435, 17.4239, 17.4478, 17.4415, 17.4145, 17.3483, 17.4375, 17.4401],
    'Lon': [78.4747, 78.4007, 78.3772, 78.4072, 78.3762, 78.4978, 78.4378, 78.5390, 78.4485, 78.3489],
    'Rating': [4.2, 3.9, 4.6, 4.5, 4.3, 3.7, 4.1, 3.8, 3.5, 4.4],
})

CATEGORIES = [
    'Street Food & Snacks', 'Bakery Items',
    'Homemade Food Products', 'Beverages & Desserts', 'Festival Food'
]

REVENUE_DATA = {
    'Street Food & Snacks': {
        'Weekly Market':  {'low': 900,  'avg': 1800, 'high': 3200},
        'Food Festival':  {'low': 1500, 'avg': 3200, 'high': 5500},
        'Exhibition':     {'low': 1200, 'avg': 2800, 'high': 4800},
        'Night Market':   {'low': 1100, 'avg': 2400, 'high': 4200},
        'Fair':           {'low': 800,  'avg': 1600, 'high': 2800},
        'Farmers Market': {'low': 700,  'avg': 1400, 'high': 2400},
        'Food Street':    {'low': 600,  'avg': 1200, 'high': 2000},
        'Tech Park Fair': {'low': 1300, 'avg': 2600, 'high': 4500},
    },
    'Bakery Items': {
        'Weekly Market':  {'low': 800,  'avg': 1600, 'high': 2800},
        'Food Festival':  {'low': 1400, 'avg': 2900, 'high': 5000},
        'Exhibition':     {'low': 1100, 'avg': 2500, 'high': 4200},
        'Night Market':   {'low': 900,  'avg': 2000, 'high': 3500},
        'Fair':           {'low': 700,  'avg': 1500, 'high': 2500},
        'Farmers Market': {'low': 900,  'avg': 1800, 'high': 3200},
        'Food Street':    {'low': 500,  'avg': 1100, 'high': 1900},
        'Tech Park Fair': {'low': 1200, 'avg': 2400, 'high': 4000},
    },
    'Homemade Food Products': {
        'Weekly Market':  {'low': 600,  'avg': 1300, 'high': 2400},
        'Food Festival':  {'low': 1000, 'avg': 2400, 'high': 4200},
        'Exhibition':     {'low': 900,  'avg': 2100, 'high': 3800},
        'Night Market':   {'low': 700,  'avg': 1700, 'high': 3000},
        'Fair':           {'low': 600,  'avg': 1300, 'high': 2200},
        'Farmers Market': {'low': 1100, 'avg': 2200, 'high': 4000},
        'Food Street':    {'low': 400,  'avg': 900,  'high': 1600},
        'Tech Park Fair': {'low': 1000, 'avg': 2000, 'high': 3500},
    },
    'Beverages & Desserts': {
        'Weekly Market':  {'low': 1000, 'avg': 2000, 'high': 3600},
        'Food Festival':  {'low': 1800, 'avg': 3600, 'high': 6000},
        'Exhibition':     {'low': 1400, 'avg': 3000, 'high': 5200},
        'Night Market':   {'low': 1300, 'avg': 2800, 'high': 4800},
        'Fair':           {'low': 900,  'avg': 1800, 'high': 3200},
        'Farmers Market': {'low': 800,  'avg': 1600, 'high': 2800},
        'Food Street':    {'low': 700,  'avg': 1400, 'high': 2400},
        'Tech Park Fair': {'low': 1500, 'avg': 3000, 'high': 5000},
    },
    'Festival Food': {
        'Weekly Market':  {'low': 700,  'avg': 1500, 'high': 2600},
        'Food Festival':  {'low': 2000, 'avg': 4000, 'high': 7000},
        'Exhibition':     {'low': 1500, 'avg': 3200, 'high': 5500},
        'Night Market':   {'low': 1200, 'avg': 2500, 'high': 4500},
        'Fair':           {'low': 1000, 'avg': 2000, 'high': 3500},
        'Farmers Market': {'low': 600,  'avg': 1300, 'high': 2200},
        'Food Street':    {'low': 500,  'avg': 1000, 'high': 1800},
        'Tech Park Fair': {'low': 1100, 'avg': 2200, 'high': 3800},
    },
}

VENDORS = pd.DataFrame({
    'Vendor Name': [
        'Priya Snacks', 'Raju Bakery', 'Meena Home Foods', 'Chai Corner',
        'Festival Eats', 'Biryani Point', 'Sweet Tooth', 'Spice Hub'
    ],
    'Category': [
        'Street Food & Snacks', 'Bakery Items', 'Homemade Food Products',
        'Beverages & Desserts', 'Festival Food', 'Street Food & Snacks',
        'Beverages & Desserts', 'Street Food & Snacks'
    ],
    'Reliability Score': [92, 88, 95, 79, 85, 91, 76, 83],
    'Total Bookings': [47, 38, 62, 29, 41, 55, 22, 36],
    'Cancellations': [2, 3, 0, 4, 3, 2, 5, 3],
    'Avg Daily Revenue (₹)': [2400, 1900, 2100, 2800, 3200, 2600, 2200, 2050],
    'Markets Visited': [8, 6, 9, 5, 7, 8, 4, 6],
})


def generate_stall_map(market_name, total_stalls=40):
    seed = int(hashlib.md5(market_name.encode()).hexdigest(), 16) % (2 ** 31)
    rng  = np.random.RandomState(seed)

    zones_config = [
        ('A - Entrance Zone', 80, 95),
        ('B - Main Walkway',  60, 79),
        ('C - Inner Area',    40, 59),
        ('D - Back Area',     20, 39),
    ]

    stalls   = []
    per_zone = max(1, total_stalls // 4)
    cols     = 7

    for zone_idx, (zone_name, fp_min, fp_max) in enumerate(zones_config):
        rows_in_zone = max(1, (per_zone - 1) // cols + 1)
        y_base       = zone_idx * (rows_in_zone + 2)

        for i in range(per_zone):
            r = rng.random()
            if r < 0.58:
                status   = 'Booked'
                category = rng.choice(['Street Food', 'Bakery', 'Beverages', 'Homemade', 'Festival Food'])
            elif r < 0.85:
                status   = 'Available'
                category = '—'
            else:
                status   = 'Waitlisted'
                category = '—'

            zone_prefix = zone_name[0]
            stalls.append({
                'Stall ID':       f'{zone_prefix}{i + 1:02d}',
                'Zone':           zone_name,
                'Footfall Score': int(rng.randint(fp_min, fp_max + 1)),
                'Status':         status,
                'Vendor Category': category,
                'Price (₹)':      900 if zone_prefix in ['A', 'B'] else 650,
                'X':              i % cols,
                'Y':              y_base + i // cols,
            })

    return pd.DataFrame(stalls)


def require_login():
    """Call at top of every page (right after set_page_config) to gate access."""
    if not st.session_state.get('logged_in', False):
        apply_css()
        st.markdown("""
        <style>
        [data-testid="stSidebar"]        { display:none !important; }
        [data-testid="stSidebarNav"]     { display:none !important; }
        [data-testid="collapsedControl"] { display:none !important; }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:70px 20px 24px;">
            <div style="font-size:4rem; margin-bottom:10px;">🔒</div>
            <div style="font-size:1.7rem; font-weight:900; color:#0F172A; margin-bottom:8px;">
                Please log in first
            </div>
            <div style="color:#64748B; font-size:1rem;">
                You need to be logged in to use Vendora
            </div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.page_link("Home.py", label="🔑  Go to Login →")
        st.stop()


def _init_booking_store():
    if 'booking_store' not in st.session_state:
        st.session_state['booking_store'] = {}
        # In a real production app, this would be backed by a database
        # such as SQLite or Postgres. This demo stores bookings only within
        # the browser session and resets on app restart.


def _init_reliability_scores():
    if 'reliability_scores' not in st.session_state:
        st.session_state['reliability_scores'] = {
            row['Vendor Name']: int(row['Reliability Score'])
            for _, row in VENDORS.iterrows()
        }


def get_vendor_name():
    return st.session_state.get('vendor_name', 'Vendor')


def get_user_role():
    return st.session_state.get('role', 'vendor')


def get_vendor_reliability(vendor_name: str):
    _init_reliability_scores()
    return st.session_state['reliability_scores'].get(vendor_name, 80)


def adjust_vendor_reliability(vendor_name: str, delta: int):
    _init_reliability_scores()
    current = st.session_state['reliability_scores'].get(vendor_name, 80)
    updated = max(0, min(100, current + delta))
    st.session_state['reliability_scores'][vendor_name] = updated
    return updated


def get_booking_store():
    _init_booking_store()
    return st.session_state['booking_store']


def get_market_bookings(market_name: str):
    store = get_booking_store()
    return store.setdefault(market_name, {})


def get_bookings_for_vendor(vendor_name: str):
    active = []
    for market, stalls in get_booking_store().items():
        for stall_id, booking in stalls.items():
            if booking['vendor_name'] == vendor_name:
                active.append((market, stall_id, booking))
    return active


def add_booking(market_name: str, stall_id: str, vendor_name: str, phone: str, category: str, zone: str, price: int):
    market = get_market_bookings(market_name)
    market[stall_id] = {
        'vendor_name': vendor_name,
        'phone': phone,
        'category': category,
        'zone': zone,
        'price': price,
        'status': 'Booked',
        'timestamp': datetime.now().isoformat(),
    }


def add_waitlist_entry(market_name: str, vendor_name: str, phone: str, category: str, zone: str):
    market = get_market_bookings(market_name)
    zone_key = zone[0] if zone else 'X'
    existing = [key for key in market.keys() if key.startswith(f"WL-{zone_key}-")]
    stall_id = f"WL-{zone_key}-{len(existing) + 1:02d}"
    market[stall_id] = {
        'vendor_name': vendor_name,
        'phone': phone,
        'category': category,
        'zone': zone,
        'price': 0,
        'status': 'Waitlisted',
        'timestamp': datetime.now().isoformat(),
    }
    return stall_id


def cancel_booking(market_name: str, stall_id: str):
    market = get_market_bookings(market_name)
    if stall_id in market:
        market[stall_id]['status'] = 'Cancelled'
        market[stall_id]['timestamp'] = datetime.now().isoformat()
        return market[stall_id]
    return None


def get_waitlist_for_market_zone(market_name: str, zone: str):
    waitlisted = []
    for stall_id, booking in get_market_bookings(market_name).items():
        if booking['status'] == 'Waitlisted' and booking['zone'] == zone:
            waitlisted.append((stall_id, booking))
    waitlisted.sort(key=lambda item: item[1]['timestamp'])
    return waitlisted


def promote_waitlist_entry(market_name: str, stall_id: str, waitlist_stall_id: str):
    market = get_market_bookings(market_name)
    if waitlist_stall_id in market and market[waitlist_stall_id]['status'] == 'Waitlisted':
        market[stall_id] = market.pop(waitlist_stall_id)
        market[stall_id]['status'] = 'Booked'
        market[stall_id]['timestamp'] = datetime.now().isoformat()
        return market[stall_id]
    return None
