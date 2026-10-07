import pickle
import streamlit as st
import pandas as pd

model = pickle.load(open('Swiggy prediction.pkl', 'rb'))
df = pd.read_csv('swiggy_demographic.csv')

st.title("Swiggy Delivery Time Prediction")
st.image('Swiggy.jpg',width=700)
st.markdown("Predict the estimated delivery time of a Swiggy order .")

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "prediction" not in st.session_state:
    st.session_state.prediction = None


if st.button('Click here to predict the delivery time '):
    st.session_state.show_form = True


if st.session_state.show_form:

    st.sidebar.title('Enter the details')

    st.sidebar.markdown("Enter the details below to predict delivery time.")


    st.sidebar.header("Rider Details")

    age = st.sidebar.number_input("Age",min_value=df["age"].min(),max_value=df["age"].max(),value=df["age"].min(),step = 0.9+0.1)

    ratings = st.sidebar.number_input("Ratings",min_value=df["ratings"].min(),max_value=df["ratings"].max(),value=df["ratings"].min(),step=0.1)

    vehicle_condition = st.sidebar.number_input("Vehicle Condition",min_value=df["vehicle_condition"].min(),max_value=df["vehicle_condition"].max(),value=df["vehicle_condition"].min())

    multiple_deliveries = st.sidebar.selectbox("Multiple Deliveries",df['multiple_deliveries'].unique())

    # festival = st.sidebar.selectbox("Is Festival",df["festival"].unique())


    st.sidebar.header("Order Details")

    type_of_order = st.sidebar.selectbox("Type of Order",df["type_of_order"].unique())

    type_of_vehicle = st.sidebar.selectbox("Type of Vehicle",df["type_of_vehicle"].unique())

    weather = st.sidebar.selectbox("Weather",df["weather"].unique())

    traffic = st.sidebar.selectbox("Traffic",df["traffic"].unique())

    city_type = st.sidebar.selectbox("City Type",df["city_type"].unique())


    st.sidebar.header("Location Details")

    # city_name = st.sidebar.selectbox("City Name",df["city_name"].unique())

    restaurant_latitude = st.sidebar.number_input("Restaurant Latitude",value=df["restaurant_latitude"].min(),format="%.6f")

    restaurant_longitude = st.sidebar.number_input("Restaurant Longitude",value=df["restaurant_longitude"].min(),format="%.6f")

    delivery_latitude = st.sidebar.number_input("Delivery Latitude",value=df["delivery_latitude"].min(),format="%.6f")

    delivery_longitude = st.sidebar.number_input("Delivery Longitude",value=df["delivery_longitude"].min(),format="%.6f")

    distance = st.sidebar.number_input("Distance",min_value=df["distance"].min(),value=df["distance"].min(),step=0.1)

    st.sidebar.header("Time Details")

    # order_time_of_day = st.sidebar.selectbox("Order Time of Day",df["order_time_of_day"].unique())

    # order_day_of_week = st.sidebar.selectbox("Order Day of Week",df["order_day_of_week"].unique())

    order_day = st.sidebar.number_input("Order Day",min_value=df["order_day"].min(),max_value=df["order_day"].max(),value=df["order_day"].min())

    order_time_hour = st.sidebar.number_input("Order Time Hour",min_value=df["order_time_hour"].min(),max_value=df["order_time_hour"].max(),value=df["order_time_hour"].min(),step = 0.9 +0.1)

    is_weekend = st.sidebar.selectbox("Is Weekend",[0, 1])

    pickup_time_minutes = st.sidebar.number_input("Pickup Time (Minutes)",min_value=df["pickup_time_minutes"].min(),max_value=df["pickup_time_minutes"].max(),value=df["pickup_time_minutes"].min())

    predict_button = st.sidebar.button("Predict Delivery Time",use_container_width=True)

    if predict_button:

        input_data = pd.DataFrame({
        'age': [age],
        'ratings': [ratings],
        'restaurant_latitude': [restaurant_latitude],
        'restaurant_longitude': [restaurant_longitude],
        'delivery_latitude': [delivery_latitude],
        'delivery_longitude': [delivery_longitude],
        'weather': [weather],
        'traffic': [traffic],
        'vehicle_condition': [vehicle_condition],
        'type_of_order': [type_of_order],
        'type_of_vehicle': [type_of_vehicle],
        'multiple_deliveries': [multiple_deliveries],
        # 'festival' : [festival],
        'city_type': [city_type],
        # 'city_name': [city_name],
        # 'order_time_of_day': [order_time_of_day],
        # 'order_day_of_week': [order_day_of_week],
        'order_day': [order_day],
        'is_weekend': [is_weekend],
        'pickup_time_minutes': [pickup_time_minutes],
        'order_time_hour': [order_time_hour],
        'distance': [distance]
        })

        prediction = model.predict(input_data)

        prediction_value = float(prediction[0])

        st.markdown("Delivery Prediction")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estimated Time",
                f"{prediction_value:.2f} min"
            )

        with col2:
            st.metric(
                "Distance",
                f"{float(distance):.2f} km"
            )

        with col3:
            st.metric(
                "Rider Rating",
                f"{float(ratings):.1f}"
            )

        if prediction_value <= 30:
            category = "Fast Delivery"

        elif prediction_value <= 45:
            category = "Normal Delivery"

        elif prediction_value <= 60:
            category = "Slightly Longer Delivery"

        else:
            category = "Long Delivery Time"

        st.success(category)

        st.markdown("Estimated Delivery Time")

        progress = float(min(prediction_value / 90, 1.0))

        st.progress(progress)

        st.caption(
        f"Estimated delivery time: {prediction_value:.2f} minutes"
        )
