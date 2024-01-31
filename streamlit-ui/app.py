######################
#     LIBRARIES      #
######################
import joblib
import pandas as pd
import streamlit as st

######################

FEATURES = ["size", "rooms", "bathrooms", "numPhotos"]

st.title("House price prediction")

left_column, right_column = st.columns(2)
SIZE = left_column.slider("Size of the house", 0.0, 500.0, 150.0)
NUMBER_OF_ROOMS = right_column.slider("Number of rooms", 0, 10, 3)
NUMBER_OF_BATHROOMS = left_column.slider("Number of bathrooms", 0, 10, 2)
NUMBER_OF_PHOTOS = right_column.slider("Number of photos", 0, 100, 20)

# Cargar el pipeline desde el archivo
model = joblib.load("linear_regression.joblib")

df = pd.DataFrame(
    data=[[SIZE, NUMBER_OF_ROOMS, NUMBER_OF_BATHROOMS, NUMBER_OF_PHOTOS]],
    columns=FEATURES,
)
result = model.predict(df)

st.write(f"The estimated price is: {round(result[0][0], 2)}")
