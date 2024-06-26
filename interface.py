import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Load the model and encoders
with open('flight_delay_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('encoders.pkl', 'rb') as encoders_file:
    encoders = pickle.load(encoders_file)

# Define functions to extract features from the date/time
def get_day_of_week(date):
    return date.weekday() + 1  # To code from 1 (Monday) to 7 (Sunday)

def get_month(date):
    return date.month

def get_dep_time_label(time):
    hour = time.hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

# Day and month mappings
days_of_week = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

# Streamlit app
st.title('Flight Delay Prediction')

# Input date and time
date = st.date_input('Flight Date')
time = st.time_input('Flight Time')

# Convert to datetime
date_time = datetime.combine(date, time)

# Extract features
day_of_week = get_day_of_week(date_time)
month = get_month(date_time)
dep_time_label = get_dep_time_label(time)

st.write(f'Day of the Week: {days_of_week[day_of_week]}, Month: {months[month]}, Departure Time Label: {dep_time_label}')

# User inputs for other features
airline = st.selectbox('Airline', ['Endeavor Air', 'American Airlines Inc.', 'Alaska Airlines Inc.', 'JetBlue Airways',
                                   'Delta Air Lines Inc', 'Frontier Airlines Inc.', 'Allegiant Air', 'Hawaiian Airlines Inc.',
                                   'American Eagle Airlines Inc.', 'Spirit Air Lines', 'Southwest Airlines Co.', 'Republic Airways',
                                   'PSA Airlines', 'Skywest Airlines Inc.', 'United Air Lines Inc.'])

dep_airport = st.text_input('Departure Airport')
arr_airport = st.text_input('Arrival Airport')
distance_type = st.selectbox('Distance Type', ['Short Haul >1500Mi', 'Medium Haul <3000Mi', 'Long Haul <6000Mi'])

# Encode the categorical variables using the same encoding as in the model
def encode_feature(feature, value):
    return encoders[feature].transform([value])[0]

# Prediction button
if st.button('Predict Delay Type'):
    dep_time_label_encoded = encode_feature('DepTime_label', dep_time_label)
    airline_encoded = encode_feature('Airline', airline)
    dep_airport_encoded = encode_feature('Dep_Airport', dep_airport)
    arr_airport_encoded = encode_feature('Arr_Airport', arr_airport)
    distance_type_encoded = encode_feature('Distance_type', distance_type)
    
    # Construct feature array
    features = np.array([day_of_week, month, airline_encoded, dep_airport_encoded, arr_airport_encoded, dep_time_label_encoded, distance_type_encoded]).reshape(1, -1)
    prediction = model.predict(features)
    st.write(f'Predicted Departure Delay Type: {prediction[0]}')
