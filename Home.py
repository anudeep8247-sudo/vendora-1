import streamlit as st
from html import escape
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import apply_css, get_vendor_name, get_user_role, MARKETS

st.set_page_config(
    page_title="Vendora — Smart Stall Booking",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_css()

# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    # Hide sidebar and collapse button on login screen
    st.markdown("""
    <style>
    [data-testid="stSidebar"]        { display:none !important; }
    [data-testid="stSidebarNav"]     { display:none !important; }
    [data-testid="collapsedControl"] { display:none !important; }
    .stApp { background: linear-gradient(135deg, #FF6B35 0%, #C62828 100%) !important; }
    </style>
    """, unsafe_allow_html=True)

    # Center the card
    _, mid, _ = st.columns([0.8, 2, 0.8])
    with mid:
        # Logo banner
        st.markdown("""
        <div style="text-align:center; padding:40px 0 28px;">
            <div style="font-size:4rem; margin-bottom:6px;">🏪</div>
            <div style="font-size:2.4rem; font-weight:900; color:white; letter-spacing:-2px;">
                VENDORA
            </div>
            <div style="color:rgba(255,255,255,0.82); font-size:1rem; margin-top:4px;">
                Smart Stall Booking for Hyderabad Vendors
            </div>
            <div style="margin-top:16px; display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                <span style="background:rgba(255,255,255,0.2); color:white; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:600;">📍 Hyderabad</span>
                <span style="background:rgba(255,255,255,0.2); color:white; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:600;">🏪 25,000+ Vendors</span>
                <span style="background:rgba(255,255,255,0.2); color:white; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:600;">💰 Up to 4x Revenue</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # White form card
        st.markdown("""
        <div style="background:white; border-radius:28px; padding:36px 32px 28px;
                    box-shadow:0 32px 80px rgba(0,0,0,0.25);">
            <div style="font-size:1.2rem; font-weight:800; color:#0F172A; margin-bottom:20px; text-align:center;">
                Welcome! Tell us who you are 👋
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Role toggle
        st.markdown("<div style='font-weight:700; color:#374151; font-size:0.95rem; margin-bottom:4px;'>I am a…</div>", unsafe_allow_html=True)
        role_choice = st.radio(
            "Role", ["🛒  Vendor (food seller)", "📊  Organizer (market owner)"],
            horizontal=True, label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Inputs
        name  = st.text_input("Your Name or Business Name", placeholder="e.g. Raju Bakery / Priya Snacks")
        phone = st.text_input("Phone Number", placeholder="10-digit number, e.g. 9876543210", max_chars=10)

        st.markdown("<br>", unsafe_allow_html=True)

        login_btn = st.button("🚀  Login / Sign Up", type="primary", width="stretch")

        if login_btn:
            if not name.strip():
                st.error("Please enter your name or business name.")
            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Please enter a valid 10-digit phone number.")
            else:
                st.session_state.logged_in   = True
                st.session_state.vendor_name = name.strip()
                st.session_state.vendor_phone = phone.strip()
                st.session_state.role = (
                    'organizer' if 'Organizer' in role_choice else 'vendor'
                )
                st.rerun()

        st.markdown("""
        <div style="text-align:center; color:#9CA3AF; font-size:0.8rem; margin-top:16px;">
            No password needed — just your name and phone 🎉<br>
            New here? The same form signs you up automatically.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD (after login)
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    vendor_name = get_vendor_name() # pyright: ignore[reportUndefinedVariable]
    display_name = escape(vendor_name)
    role        = get_user_role() # pyright: ignore[reportUndefinedVariable]

    # Greeting banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FF6B35 0%,#C62828 100%);
                border-radius:22px; padding:28px 28px 24px; margin-bottom:1.4rem;
                box-shadow:0 12px 40px rgba(255,107,53,0.3);">
        <div style="font-size:1.7rem; font-weight:900; color:white; margin-bottom:4px;">
            👋 Hi, {display_name}!
        </div>
        <div style="color:rgba(255,255,255,0.85); font-size:1rem;">
            Ready to find the perfect stall today? All tools are in the sidebar 👈
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats
    open_markets  = int((MARKETS['Available Stalls'] > 0).sum()) # pyright: ignore[reportUndefinedVariable]
    total_free    = int(MARKETS['Available Stalls'].sum()) # pyright: ignore[reportUndefinedVariable]
    stats = [
        ("🏪", str(open_markets),  "Markets with Open Stalls"),
        ("📍", str(total_free),    "Stalls Available Now"),
        ("💰", "68%",              "Avg Revenue Uplift"),
        ("⭐", "4.2",              "Platform Rating"),
    ]
    cols = st.columns(4)
    for col, (ico, num, label) in zip(cols, stats):
        col.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.6rem; margin-bottom:4px;">{ico}</div>
            <div class="stat-num">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature cards (colorful nav) ──────────────────────────────────────────
    st.markdown("""
    <div style="font-size:1.35rem; font-weight:900; color:#0F172A; margin-bottom:18px;">
        🚀 What do you want to do today?
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("explore", "🛒", "Explore Markets",      "Find markets & food events near you",    "pages/1_Market_Discovery.py"),
        ("book",    "📍", "Book a Stall",         "Pick your spot on a live stall map",     "pages/2_Stall_Map.py"),
        ("earn",    "💰", "Earnings Calculator",  "How much will you earn today?",          "pages/3_Revenue_Predictor.py"),
        ("best",    "⭐", "Best Markets",         "Most profitable markets for your food",   "pages/5_Best_Markets.py"),
        ("suggest", "🎯", "Smart Suggest",        "Get a personalised market match",        "pages/7_Smart_Suggest.py"),
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)
    all_cols = row1 + row2

    for col, (slug, icon, title, desc, page) in zip(all_cols, features):
        with col:
            with st.container(key=f"feature_{slug}"):
                if st.button(
                    f"{icon}\n\n**{title}**\n\n{desc}",
                    key=f"feature_btn_{slug}",
                    width="stretch",
                ):
                    st.switch_page(page)

    # Organizer panel (only for organizer role)
    if role == 'organizer':
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#0F172A; border-radius:16px; padding:20px 24px; margin-bottom:12px;">
            <div style="color:white; font-weight:800; font-size:1rem; margin-bottom:4px;">
                📊 Organizer Tools
            </div>
            <div style="color:#94A3B8; font-size:0.87rem;">
                Access your market dashboard, manage stalls, and track revenue.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/6_Organizer_Dashboard.py", label="📊 Open Organizer Dashboard →")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Logout
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚪 Logout", width="stretch"):
            for key in ['logged_in', 'vendor_name', 'vendor_phone', 'role']:
                st.session_state.pop(key, None)
            st.rerun()

    st.caption("Vendora · BBA Innovation Project 2025 · Mahindra University, Hyderabad")


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.get('logged_in', False):
    show_login()
else:
    show_dashboard()
