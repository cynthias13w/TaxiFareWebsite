import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import math

# CONFIGURATING PAGE
st.set_page_config(page_title='Taxi Fare Predictions', page_icon='🚕', initial_sidebar_state="auto", menu_items=None)

new_title = '<p style="font-family:Snell Roundhand, fantasy; color: #000000; text-align: center; font-size: 42px;"> 😀 Calculate your Taxi Fare! 🚕</p>'
st.markdown(new_title, unsafe_allow_html=True)

#####

with st.form(key = 'columns_in_form'):
# GEOCODING
    url = "https://nominatim.openstreetmap.org"

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📅 DATE")

    with col2:
        time = st.time_input("🕞 TIME")

    #date_and_time = f"{date} {time}"
    date_time = datetime.combine(date, time)

    col3, col4 = st.columns(2)
    with col3:
        address1 = st.text_input("📍 Pickup Address", "Empire State Building")
        params = {
        'q': address1,
        'format': 'json'
    }
        response = requests.get(url, params=params).json() # TEXT -> [] / {}
        lat1 = response[0]['lat']
        lon1 = response[0]['lon']

        # with st.expander("📍 Pickup coordinates"):
        #     lon1 = st.number_input("LONGITUDE", 32)
        #     lat1 = st.number_input("LATITUDE", 2)

    with col4:
        address2 = st.text_input("📍 Dropoff Address", "Central Park")
        params2 = {
        'q': address2,
        'format': 'json'
    }
        response2 = requests.get(url, params=params2).json() # TEXT -> [] / {}
        lat2 = response2[0]['lat']
        lon2 = response2[0]['lon']
        # with st.expander("📍 Dropoff coordinates"):
        #     lon2 = st.number_input("LONGITUDE", 4)
        #     lat2 = st.number_input("LATITUDE", 7)

    col5, col6 = st.columns(2)
    with col5:
        passenger_count = st.slider("🧍NUMBER OF PASSENGERS", 1, 5, step = 1)

    dictionary2 = {
        "longitude": [float(-95.665), float(-73.94)],
        "latitude": [float(37.6), float(40.65)]}

    df = pd.DataFrame(dictionary2)

    st.map(df, zoom = 2)

    url = 'https://taxifare.lewagon.ai/predict'

    dictionary = {
        "pickup_datetime": date_time,
        "pickup_longitude": float(lon1),
        "pickup_latitude": float(lat1),
        "dropoff_longitude": float(lon2),
        "dropoff_latitude": float(lat2),
        "passenger_count": int(passenger_count)}

    response = requests.get("https://taxifare.lewagon.ai/predict", dictionary).json()
    fare = "$" + str(round(response['fare'], 2))
    #st.metric("ESTIMATED DISTANCE", distance_func(lat1,lon1,lat2,lon2))
    submit_button = st.form_submit_button(label='Calculate my taxi fare!')
    if submit_button:
        st.metric("ESTIMATED COSTS", fare)
