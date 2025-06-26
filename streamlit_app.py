import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from datetime import datetime

# Sample data
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

# Order generator
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

# Streamlit UI
st.title("📦 Live Order Simulation Map")
st.markdown("Real-time orders mapped with Pydeck!")

orders = [generate_order() for _ in range(50)]
df = pd.DataFrame(orders)

st.dataframe(df)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=39.5,
        longitude=-98.35,
        zoom=3,
        pitch=40,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_fill_color='[180, 0, 200, 160]',
            get_radius=40000,
        ),
    ],
))

