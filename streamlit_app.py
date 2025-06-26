import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random
from datetime import datetime

# Fake data config
parts = ['P-SSD01', 'P-RAM16', 'P-GPU3080', 'P-CPU12', 'P-MB550']
vehicles = ['Truck-01', 'Truck-02', 'Plane-1', 'Truck-03', 'Plane-2']
customers = [f'C{1000+i}' for i in range(5000)]
locations = [
    {'city': 'Memphis', 'lat': 35.1495, 'lon': -90.0490},
    {'city': 'Chicago', 'lat': 41.8781, 'lon': -87.6298},
    {'city': 'Dallas', 'lat': 32.7767, 'lon': -96.7970},
    {'city': 'Atlanta', 'lat': 33.7490, 'lon': -84.3880},
    {'city': 'Denver', 'lat': 39.7392, 'lon': -104.9903}
]

# Simulated data generator
def generate_order():
    loc = random.choice(locations)
    return {
        'order_id': f'O{random.randint(10000,99999)}',
        'customer_id': random.choice(customers),
        'part_id': random.choice(parts),
        'quantity': random.randint(1, 100),
        'ship_method': random.choice(['Ground', 'Air']),
        'vehicle': random.choice(vehicles),
        'city': loc['city'],
        'lat': loc['lat'],
        'lon': loc['lon'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# Generate sample orders
orders = [generate_order() for _ in range(50)]
df = pd.DataFrame(orders)

# Sidebar filters
st.sidebar.header("🔍 Filter Orders")
selected_cities = st.sidebar.multiselect("Filter by City", options=df['city'].unique(), default=df['city'].unique())
selected_vehicles = st.sidebar.multiselect("Filter by Vehicle", options=df['vehicle'].unique(), default=df['vehicle'].unique())

# Apply filters
filtered_df = df[(df['city'].isin(selected_cities)) & (df['vehicle'].isin(selected_vehicles))]

# KPIs
st.title("Logistics Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Quantity", int(filtered_df['quantity'].mean()))
col3.metric("Air vs Ground", f"{(filtered_df['ship_method'].value_counts().get('Air', 0))}  / {(filtered_df['ship_method'].value_counts().get('Ground', 0))}")

# Data table
st.subheader("Order Details")
st.dataframe(filtered_df, use_container_width=True)

# Map
m = folium.Map(location=[39.5, -98.35], zoom_start=4)
for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"""
            <b>Order:</b> {row['order_id']}<br>
            <b>Customer:</b> {row['customer_id']}<br>
            <b>Vehicle:</b> {row['vehicle']}<br>
            <b>Status:</b> In Transit
        """,
        tooltip=f"{row['city']} | {row['part_id']} | Qty: {row['quantity']}",
        icon=folium.Icon(color="purple", icon="info-sign")
    ).add_to(m)

st.subheader("Orders Map")
folium_static(m, width=700, height=500)
