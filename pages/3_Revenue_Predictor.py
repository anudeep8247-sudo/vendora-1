import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data import MARKETS, CATEGORIES, REVENUE_DATA, apply_css, require_login, show_back_button
 
st.set_page_config(page_title="Earnings Calculator — Vendora", page_icon="💰", layout="wide")
apply_css()
require_login()
show_back_button()
 
st.markdown("""
<div style="margin-bottom:6px;">
  <span style="font-size:2rem; font-weight:900; color:#0F172A;">💰 Earnings Calculator</span>
</div>
<div style="color:#64748B; font-size:1rem; margin-bottom:1.5rem;">
  Pick a market and food type — we'll tell you <strong>how much you could earn</strong>,
  whether you'll make a profit, and <strong>how many items you need to sell</strong> to cover your costs.
</div>
""", unsafe_allow_html=True)
 
# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("🍽️ Your Food Type", CATEGORIES)
with col2:
    market = st.selectbox("📍 Select Market", MARKETS['Market Name'].tolist())
 
market_row  = MARKETS[MARKETS['Market Name'] == market].iloc[0]
market_type = market_row['Type']
stall_price = int(market_row['Stall Price'])
footfall    = int(market_row['Expected Footfall'])
rev         = REVENUE_DATA[category][market_type]
profit_avg  = rev['avg'] - stall_price
profit_low  = rev['low'] - stall_price
profit_high = rev['high'] - stall_price
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ── Big earnings display ──────────────────────────────────────────────────────
if profit_avg > 800:
    profit_label = "🟢 Strong profit"
    profit_color = "#43A047"
elif profit_avg > 0:
    profit_label = "🟡 Moderate profit"
    profit_color = "#F9A825"
else:
    profit_label = "🔴 May not cover costs"
    profit_color = "#E53935"
 
st.markdown(f"""
<div class="earn-main">
    <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase;
                letter-spacing:0.1em; opacity:0.8; margin-bottom:10px;">
        On a normal day at {market}
    </div>
    <div style="font-size:3.8rem; font-weight:900; letter-spacing:-2px; margin-bottom:4px;">
        ₹{rev['avg']:,}
    </div>
    <div style="font-size:1rem; opacity:0.85; margin-bottom:14px;">
        estimated earnings
    </div>
    <div style="display:inline-block; background:rgba(255,255,255,0.2); border-radius:30px;
                padding:6px 20px; font-size:0.9rem; font-weight:700; margin-bottom:10px;">
        After ₹{stall_price:,} stall rent → <strong>₹{profit_avg:,} profit</strong>
    </div>
    <br>
    <div style="display:inline-block; background:{profit_color}; border-radius:12px;
                padding:6px 16px; font-size:0.9rem; font-weight:800; color:white;">
        {profit_label}
    </div>
</div>
""", unsafe_allow_html=True)
 
# ── 3 scenario cards ──────────────────────────────────────────────────────────
st.markdown("""
<div style="font-weight:700; color:#0F172A; font-size:1rem; margin:16px 0 10px;">
    📊 Three Possible Outcomes
</div>
""", unsafe_allow_html=True)
 
sc1, sc2, sc3 = st.columns(3)
sc1.markdown(f"""
<div class="sc-bad">
    <div style="font-size:1.4rem; margin-bottom:4px;">😕</div>
    <div style="font-size:0.75rem; font-weight:700; color:#B71C1C;
                text-transform:uppercase; margin-bottom:6px;">Slow Day</div>
    <div style="font-size:1.6rem; font-weight:900; color:#C62828;">₹{rev['low']:,}</div>
    <div style="font-size:0.8rem; color:#78909C; margin-top:4px;">
        Profit: ₹{profit_low:,}
    </div>
</div>
""", unsafe_allow_html=True)
 
sc2.markdown(f"""
<div class="sc-normal">
    <div style="font-size:1.4rem; margin-bottom:4px;">😊</div>
    <div style="font-size:0.75rem; font-weight:700; color:#1B5E20;
                text-transform:uppercase; margin-bottom:6px;">Normal Day</div>
    <div style="font-size:1.6rem; font-weight:900; color:#2E7D32;">₹{rev['avg']:,}</div>
    <div style="font-size:0.8rem; color:#78909C; margin-top:4px;">
        Profit: ₹{profit_avg:,}
    </div>
</div>
""", unsafe_allow_html=True)
 
sc3.markdown(f"""
<div class="sc-great">
    <div style="font-size:1.4rem; margin-bottom:4px;">🤩</div>
    <div style="font-size:0.75rem; font-weight:700; color:#4527A0;
                text-transform:uppercase; margin-bottom:6px;">Great Day</div>
    <div style="font-size:1.6rem; font-weight:900; color:#512DA8;">₹{rev['high']:,}</div>
    <div style="font-size:0.8rem; color:#78909C; margin-top:4px;">
        Profit: ₹{profit_high:,}
    </div>
</div>
""", unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
 
# ── Play with your numbers ────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0F172A; border-radius:18px; padding:24px 24px 18px; margin-bottom:1.2rem;">
    <div style="font-size:1.15rem; font-weight:800; color:white; margin-bottom:4px;">
        ⚡ Play With Your Numbers
    </div>
    <div style="color:#94A3B8; font-size:0.88rem;">
        Drag the sliders to see how your earnings change
    </div>
</div>
""", unsafe_allow_html=True)
 
col1, col2, col3 = st.columns(3)
with col1:
    est_customers = st.slider("👥 Expected Customers", 10, 400, 100, step=10)
with col2:
    items_per_cust = st.slider("🛍️ Items per Customer", 1, 6, 2)
with col3:
    item_price = st.number_input("💵 Price per Item (₹)", min_value=10, max_value=500, value=60, step=5)
 
sim_revenue = est_customers * items_per_cust * item_price
 
m1, m2, m3 = st.columns(3)
m1.metric("Your Estimated Revenue", f"₹{sim_revenue:,}")
m2.metric("Estimated Profit",       f"₹{sim_revenue - stall_price:,}", "after stall rent")
m3.metric("People visiting market", f"{footfall:,}", "expected footfall")
 
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
 
# ── Break-even (simplified) ───────────────────────────────────────────────────
st.markdown("""
<div style="font-size:1.1rem; font-weight:800; color:#0F172A; margin-bottom:12px;">
    🧮 How many items do you need to sell?
</div>
""", unsafe_allow_html=True)
 
col1, col2, col3 = st.columns(3)
with col1:
    ingredients = st.number_input("🥘 Daily Ingredients Cost (₹)", min_value=0, value=400, step=50)
with col2:
    selling_price = st.number_input("🏷️ You sell each item at (₹)", min_value=1, value=60, step=5)
with col3:
    transport = st.number_input("🚗 Transport & Other Costs (₹)", min_value=0, value=100, step=50)
 
total_cost    = stall_price + ingredients + transport
items_needed  = -(-total_cost // selling_price)
surplus       = rev['avg'] - total_cost
 
st.markdown(f"""
<div style="background:#F8FAFC; border-radius:18px; padding:24px; margin-top:8px;">
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:16px; text-align:center;">
        <div style="background:white; border-radius:14px; padding:18px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
            <div style="font-size:0.72rem; color:#64748B; text-transform:uppercase;
                        font-weight:700; margin-bottom:6px;">Your Total Daily Cost</div>
            <div style="font-size:1.8rem; font-weight:900; color:#E53935;">₹{total_cost:,}</div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:4px;">
                Rent ₹{stall_price:,} + Ingredients ₹{ingredients:,} + Travel ₹{transport:,}
            </div>
        </div>
        <div style="background:white; border-radius:14px; padding:18px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
            <div style="font-size:0.72rem; color:#64748B; text-transform:uppercase;
                        font-weight:700; margin-bottom:6px;">Items You Must Sell</div>
            <div style="font-size:1.8rem; font-weight:900; color:#FF6B35;">{items_needed}</div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:4px;">
                at ₹{selling_price}/item just to break even
            </div>
        </div>
        <div style="background:white; border-radius:14px; padding:18px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
            <div style="font-size:0.72rem; color:#64748B; text-transform:uppercase;
                        font-weight:700; margin-bottom:6px;">Expected Surplus</div>
            <div style="font-size:1.8rem; font-weight:900;
                        color:{'#43A047' if surplus > 0 else '#E53935'};">
                ₹{surplus:,}
            </div>
            <div style="font-size:0.75rem; color:#9CA3AF; margin-top:4px;">
                {'above costs on a normal day' if surplus > 0 else 'shortfall on a normal day'}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
 
if surplus > 0:
    st.success(f"✅ On a normal day at this market, you'd cover all costs and still pocket **₹{surplus:,}**.")
else:
    st.error(f"⚠️ Average earnings here may not fully cover your costs. Try a higher-footfall market — check **Best Markets** in the sidebar.")
 
