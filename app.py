from multimethod import distance
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import math

new_title = '<p style="font-family:Snell Roundhand, fantasy; color: #a7a6ba; text-align: center; font-size: 42px;"> 😀 Calculate your Taxi Fare 🚕</p>'
st.markdown(new_title, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("📅 DATE")

with col2:
    time = st.time_input("🕞 TIME")

#date_and_time = f"{date} {time}"
date_time = datetime.combine(date, time)

col3, col4 = st.columns(2)
with col3:
    with st.expander("📍 Pickup coordinates"):
        lon1 = st.number_input("LONGITUDE", 32)
        lat1 = st.number_input("LATITUDE", 2)

with col4:
    with st.expander("📍 Dropoff coordinates"):
        lon2 = st.number_input("LONGITUDE", 4)
        lat2 = st.number_input("LATITUDE", 7)

col5, col6 = st.columns(2)
with col5:
    passenger_count = st.slider("🧍NUMBER OF PASSENGERS", 1, 5, step = 1)

# approximate radius of earth in km
def distance_func(lat1,lon1,lat2,lon2):
    R = 6373.0
    lat1 = lat1
    lon1 = lon1
    lat2 = lat2
    lon2 = lon2
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c  = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

url = 'https://taxifare.lewagon.ai/predict'

dictionary = {
    "pickup_datetime": date_time,
    "pickup_longitude": float(lon1),
    "pickup_latitude": float(lat1),
    "dropoff_longitude": float(lon2),
    "dropoff_latitude": float(lat2),
    "passenger_count": int(passenger_count)}

dictionary2 = {
    "longitude": [float(lon1), float(lon2)],
    "latitude": [float(lat1), float(lat2)]}


df = pd.DataFrame(dictionary2)

st.map(df, zoom = -1)
response = requests.get("https://taxifare.lewagon.ai/predict", dictionary).json()
fare = "$" + str(round(response['fare'], 2))
st.metric("ESTIMATED COSTS", fare)
st.metric("ESTIMATED DISTANCE", distance_func(lat1,lon1,lat2,lon2))
