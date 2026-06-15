import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data import MARKETS, CATEGORIES, generate_stall_map, apply_css, require_login
 
st.set_page_config(page_title="Zone Picker — Vendora", page_icon="🔥", layout="wide")
apply_css()
require_login()
 
st.markdown("""
<div style="margin-bottom:6px;">
  <span style="font-size:2rem; font-weight:900; color:#0F172A;">🔥 Zone Picker</span>
</div>
<div style="color:#64748B; font-size:1rem; margin-bottom:1.5rem;">
  Which zone is <strong>best for your food type</strong>? We check how crowded each zone is so
  you can avoid rivals and grab the highest-traffic spot.
</div>
""", unsafe_allow_html=True)
 
# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    market = st.selectbox("📍 Select Market", MARKETS['Market Name'].tolist())
with col2:
    my_category = st.selectbox("🍽️ Your Food Type", CATEGORIES)
 
market_row = MARKETS[MARKETS['Market Name'] == market].iloc[0]
stalls_df  = generate_stall_map(market, total_stalls=int(market_row['Total Stalls']))
booked     = stalls_df[stalls_df['Status'] == 'Booked'].copy()
 
cat_map = {
    'Street Food': 'Street Food & Snacks',
    'Bakery':      'Bakery Items',
    'Beverages':   'Beverages & Desserts',
    'Homemade':    'Homemade Food Products',
    'Festival Food': 'Festival Food',
}
booked.loc[:, 'Category Full'] = booked['Vendor Category'].map(cat_map).fillna('')
 
zones_config = [
    ('A - Entrance Zone', '🏁 Entrance',  'Highest footfall — first thing customers see'),
    ('B - Main Walkway',  '🚶 Walkway',   'Great footfall — busy central path'),
    ('C - Inner Area',    '🏠 Inner Area', 'Moderate footfall — away from main path'),
    ('D - Back Area',     '🔙 Back Area',  'Lower footfall — last section'),
]
 
# ── Score each zone ───────────────────────────────────────────────────────────
zone_data = []
for zone_id, zone_label, zone_desc in zones_config:
    sub        = stalls_df[stalls_df['Zone'] == zone_id]
    booked_sub = booked[booked['Zone'] == zone_id]
    rivals     = int((booked_sub['Category Full'] == my_category).sum())
    avg_fp     = round(float(sub['Footfall Score'].mean()), 0)
    avail      = int((sub['Status'] == 'Available').sum())
    score      = avg_fp - (rivals * 10)
 
    zone_data.append({
        'id':      zone_id,
        'label':   zone_label,
        'desc':    zone_desc,
        'rivals':  rivals,
        'fp':      avg_fp,
        'avail':   avail,
        'score':   score,
    })
 
zone_data.sort(key=lambda x: x['score'], reverse=True)
best_zone = zone_data[0]
 
# ── Best zone banner ──────────────────────────────────────────────────────────
if best_zone['avail'] > 0:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#43A047,#1B5E20); border-radius:18px;
                padding:22px 24px; margin-bottom:1.4rem; color:white;">
        <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.1em; opacity:0.8; margin-bottom:6px;">
            🏆 OUR PICK FOR YOU
        </div>
        <div style="font-size:1.5rem; font-weight:900; margin-bottom:4px;">
            {best_zone['label']} — {best_zone['id'].split(' - ')[1]}
        </div>
        <div style="opacity:0.88; font-size:0.95rem;">
            Footfall score {best_zone['fp']:.0f}/100 &nbsp;·&nbsp;
            Only {best_zone['rivals']} rival(s) from your food type &nbsp;·&nbsp;
            {best_zone['avail']} stall(s) free
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning(f"⚠️ Best scored zone ({best_zone['label']}) has no available stalls. Check the next option below.")
 
# ── Zone cards grid ───────────────────────────────────────────────────────────
st.markdown("""
<div style="font-weight:700; color:#0F172A; font-size:1rem; margin-bottom:12px;">
    All 4 Zones at a Glance
</div>
""", unsafe_allow_html=True)
 
col1, col2 = st.columns(2)
cols_cycle = [col1, col2, col1, col2]
 
# Sort back to original zone order for display
zone_data_display = sorted(zone_data, key=lambda x: x['id'])
 
for z, col in zip(zone_data_display, cols_cycle):
    # Determine card style based on score rank
    rank = next(i for i, zd in enumerate(zone_data) if zd['id'] == z['id'])
    zone_icon, zone_title = z['label'].split(' ', 1) if ' ' in z['label'] else (z['label'], '')
    if rank == 0 and z['avail'] > 0:
        css_cls   = 'zone-best'
        badge     = '✅ BEST PICK'
        badge_col = '#2E7D32'
    elif rank == 1 and z['avail'] > 0:
        css_cls   = 'zone-good'
        badge     = '👍 GOOD'
        badge_col = '#1565C0'
    elif z['avail'] == 0:
        css_cls   = 'zone-avoid'
        badge     = '❌ NO STALLS'
        badge_col = '#C62828'
    elif z['rivals'] >= 4:
        css_cls   = 'zone-avoid'
        badge     = '⚠️ VERY CROWDED'
        badge_col = '#C62828'
    else:
        css_cls   = 'zone-okay'
        badge     = '🟡 OKAY'
        badge_col = '#E65100'
 
    # Footfall bar (visual)
    fp_pct    = int(z['fp'])
    bar_width = fp_pct
 
    with col:
        st.markdown(f"""
        <div class="zone-card {css_cls}" style="margin-bottom:14px;">
 
            <div style="font-size:1.5rem; margin-bottom:4px;">{zone_icon}</div>
            <div style="font-size:1.05rem; font-weight:800; color:#0F172A; margin-bottom:2px;">
                {zone_title}
            </div>
            <div style="font-size:0.78rem; color:#64748B; margin-bottom:14px;">{z['desc']}</div>
 
            <div style="margin-bottom:10px;">
                <div style="font-size:0.72rem; color:#475569; font-weight:600;
                            text-transform:uppercase; margin-bottom:4px;">
                    Footfall Score
                </div>
                <div style="background:#E2E8F0; border-radius:8px; height:12px; margin-bottom:4px;">
                    <div style="background:#FF6B35; width:{bar_width}%; height:100%;
                                border-radius:8px; transition:width 0.4s;"></div>
                </div>
                <div style="font-size:0.85rem; font-weight:700; color:#0F172A;">
                    {z['fp']:.0f} / 100
                </div>
            </div>
 
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">
                <div style="background:rgba(255,255,255,0.65); border-radius:10px; padding:8px; text-align:center;">
                    <div style="font-size:1.3rem; font-weight:900; color:#0F172A;">{z['rivals']}</div>
                    <div style="font-size:0.7rem; color:#64748B; margin-top:2px;">Your rivals</div>
                </div>
                <div style="background:rgba(255,255,255,0.65); border-radius:10px; padding:8px; text-align:center;">
                    <div style="font-size:1.3rem; font-weight:900; color:#0F172A;">{z['avail']}</div>
                    <div style="font-size:0.7rem; color:#64748B; margin-top:2px;">Free stalls</div>
                </div>
            </div>
 
            <div style="background:{badge_col}; color:white; border-radius:10px;
                        padding:7px 14px; font-weight:800; font-size:0.85rem; text-align:center;">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
 
# ── Tip ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#F8FAFC; border-left:4px solid #FF6B35; border-radius:0 12px 12px 0;
            padding:14px 18px; margin-top:8px; font-size:0.9rem; color:#374151;">
    <strong>💡 Tip:</strong> Fewer rivals + higher footfall = more customers for you.
    Even a mid-footfall zone with zero competition often outperforms a prime zone that's packed.
</div>
""", unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Go to **Stall Map & Booking** in the sidebar to reserve a stall in your best zone.")
 
