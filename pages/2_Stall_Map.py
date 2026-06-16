import streamlit as st
import plotly.express as px
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data import (
    MARKETS, CATEGORIES, generate_stall_map, apply_css, require_login,
    get_market_bookings, add_booking, cancel_booking,
    get_waitlist_for_market_zone, promote_waitlist_entry,
    get_vendor_reliability, adjust_vendor_reliability,
)

st.set_page_config(page_title="Stall Map — Vendora", page_icon="📍", layout="wide")
apply_css()
require_login()
st.title("📍 Stall Map & Booking")
st.caption("See the full stall layout and book your spot based on footfall scores")

# ── Market selector ───────────────────────────────────────────────────────────
market_name = st.selectbox("Select Market", MARKETS['Market Name'].tolist())
market_row  = MARKETS[MARKETS['Market Name'] == market_name].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Expected Footfall", f"{market_row['Expected Footfall']:,}")
c2.metric("Market Type", market_row['Type'])
c3.metric("Day", market_row['Day'])
c4.metric("Rating", f"⭐ {market_row['Rating']}")

# Load underlying stall layout and overwrite status from session-state bookings.
stalls_df = generate_stall_map(market_name, total_stalls=int(market_row['Total Stalls']))
market_bookings = get_market_bookings(market_name)
for stall_id, booking in market_bookings.items():
    if stall_id in stalls_df['Stall ID'].values:
        if booking['status'] == 'Booked':
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Status'] = 'Booked'
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Vendor Category'] = booking['category']
        elif booking['status'] == 'Cancelled':
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Status'] = 'Available'
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Vendor Category'] = '—'
        elif booking['status'] == 'Waitlisted':
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Status'] = 'Waitlisted'
            stalls_df.loc[stalls_df['Stall ID'] == stall_id, 'Vendor Category'] = booking['category']

st.divider()

# ── Zone Summary ──────────────────────────────────────────────────────────────
st.subheader("Zone Overview")
zone_cols = st.columns(4)
zone_labels = {
    'A - Entrance Zone': ('🔴 High Traffic', 'success'),
    'B - Main Walkway':  ('🟠 Medium-High',  'info'),
    'C - Inner Area':    ('🟡 Medium',        'warning'),
    'D - Back Area':     ('🟢 Low Traffic',   'error'),
}
for col, (zone, (label, _)) in zip(zone_cols, zone_labels.items()):
    sub = stalls_df[stalls_df['Zone'] == zone]
    avail = (sub['Status'] == 'Available').sum()
    booked = (sub['Status'] == 'Booked').sum()
    avg_fp = sub['Footfall Score'].mean()
    col.metric(zone.split(' - ')[1], f"Avg Score: {avg_fp:.0f}/100",
               f"{avail} available · {booked} booked")

st.divider()

# ── Visual Stall Grid ─────────────────────────────────────────────────────────
st.subheader("Stall Map")
color_map = {'Booked': '#E53935', 'Available': '#43A047', 'Waitlisted': '#FB8C00'}

fig = px.scatter(
    stalls_df,
    x='X', y='Y',
    color='Status',
    color_discrete_map=color_map,
    hover_data={
        'Stall ID': True, 'Zone': True,
        'Footfall Score': True, 'Price (₹)': True,
        'Vendor Category': True, 'X': False, 'Y': False
    },
    title="Click on a stall to see details  |  🟢 Available   🔴 Booked   🟠 Waitlisted",
    height=460,
)
fig.update_traces(marker=dict(size=22, symbol='square', line=dict(width=1, color='white')))
fig.update_layout(
    yaxis_autorange='reversed',
    xaxis_title='', yaxis_title='',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='#f8f9fa',
    legend_title_text='Status',
)
st.plotly_chart(fig, use_container_width=True)

# Zone labels on the side
for zone, (label, _) in zone_labels.items():
    st.caption(f"**{zone}** — {label}")

st.divider()

# ── Booking Panel ─────────────────────────────────────────────────────────────
st.subheader("Book a Stall")
available_stalls = stalls_df[stalls_df['Status'] == 'Available']

# Show vendor reliability score from session state.
vendor_name_input = st.session_state.get('vendor_name', '')
current_reliability = get_vendor_reliability(vendor_name_input) if vendor_name_input else 80
st.markdown(f"**Your Reliability Score:** {current_reliability}/100")

if len(available_stalls) == 0:
    st.error("No stalls available right now. You can join the waitlist via the organizer.")
else:
    col1, col2 = st.columns([1, 1])

    with col1:
        selected_id = st.selectbox(
            "Choose an Available Stall",
            available_stalls['Stall ID'].tolist(),
            format_func=lambda sid: (
                f"Stall {sid}  —  Score "
                f"{available_stalls.loc[available_stalls['Stall ID'] == sid, 'Footfall Score'].values[0]}/100"
                f"  —  ₹{available_stalls.loc[available_stalls['Stall ID'] == sid, 'Price (₹)'].values[0]}"
            )
        )
        info = available_stalls[available_stalls['Stall ID'] == selected_id].iloc[0]

        sc = info['Footfall Score']
        if sc >= 80:
            st.success(f"🔥 **Prime spot** — footfall score {sc}/100. High traffic, high potential.")
        elif sc >= 60:
            st.info(f"👍 **Good spot** — footfall score {sc}/100. Decent traffic expected.")
        elif sc >= 40:
            st.warning(f"⚠️ **Average spot** — footfall score {sc}/100. Moderate traffic.")
        else:
            st.error(f"📉 **Low traffic zone** — footfall score {sc}/100. Consider a different stall.")

    with col2:
        vendor_name = st.text_input("Your Name / Business Name", value=vendor_name_input)
        category    = st.selectbox("Food Category", CATEGORIES)
        phone       = st.text_input("Phone Number", value=st.session_state.get('vendor_phone', ''))

        st.caption(f"Zone: {info['Zone']}  |  Price: ₹{info['Price (₹)']}  |  Score: {sc}/100")

        if st.button("✅ Confirm Booking", type="primary", use_container_width=True):
            if vendor_name and phone:
                add_booking(
                    market_name=market_name,
                    stall_id=selected_id,
                    vendor_name=vendor_name,
                    phone=phone,
                    category=category,
                    zone=info['Zone'],
                    price=int(info['Price (₹)']),
                )
                adjust_vendor_reliability(vendor_name, 2)
                st.success(
                    f"**Booking Confirmed!**\n\n"
                    f"Stall **{selected_id}** at **{market_name}** is reserved for **{vendor_name}**."
                )
                st.info(
                    "📋 Cancellations allowed up to 24 hours before market day. "
                    "Late cancellations reduce your Reliability Score."
                )
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill in your name and phone number to confirm.")

# ── Active Booking & Cancellation Panel ──────────────────────────────────────
st.divider()
st.subheader("My Active Bookings")
current_vendor = st.session_state.get('vendor_name', '')
vendor_bookings = [
    (stall_id, booking)
    for stall_id, booking in get_market_bookings(market_name).items()
    if booking['vendor_name'] == current_vendor and booking['status'] == 'Booked'
]

if current_vendor and vendor_bookings:
    for stall_id, booking in vendor_bookings:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"**{stall_id}** • {booking['zone']} • ₹{booking['price']} — "
                f"Booked on {booking['timestamp'].split('T')[0]}"
            )
        with col2:
            if st.button(f"Cancel {stall_id}", key=f"cancel_{stall_id}", use_container_width=True):
                cancelled = cancel_booking(market_name, stall_id)
                if cancelled:
                    adjust_vendor_reliability(current_vendor, -5)
                    waitlist = get_waitlist_for_market_zone(market_name, booking['zone'])
                    if waitlist:
                        wait_id, wait_booking = waitlist[0]
                        promoted = promote_waitlist_entry(market_name, stall_id, wait_id)
                        if promoted:
                            st.success(
                                f"Booking {stall_id} cancelled. {promoted['vendor_name']} has been promoted from the waitlist to this stall."
                            )
                    else:
                        st.success(f"Booking {stall_id} cancelled and the stall is now available again.")
                    st.rerun()
else:
    st.info("You have no active bookings in this market right now.")
