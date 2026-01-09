import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_engine
from queries import queries

# Page Config
st.set_page_config(
    page_title="Ola Ride Insights",
    layout="wide"
)

st.title("🚕 Ola Ride Insights Dashboard")
st.caption("SQL-driven analytics from CSV data")

engine = get_engine()

# Sidebar
option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Successful Bookings",
        "Avg Ride Distance by Vehicle",
        "Customer Cancellations",
        "Top 5 Customers",
        "Driver Cancellations",
        "Prime Sedan Ratings",
        "UPI Payments",
        "Avg Customer Rating",
        "Total Booking Value",
        "Incomplete Rides"
    ]
)

# Mapping UI → Query
query_map = {
    "Successful Bookings": "successful_bookings",
    "Avg Ride Distance by Vehicle": "avg_ride_distance_by_vehicle",
    "Customer Cancellations": "customer_cancellations",
    "Top 5 Customers": "top_5_customers",
    "Driver Cancellations": "driver_cancellations",
    "Prime Sedan Ratings": "prime_sedan_ratings",
    "UPI Payments": "upi_payments",
    "Avg Customer Rating": "avg_customer_rating",
    "Total Booking Value": "total_booking_value",
    "Incomplete Rides": "incomplete_rides"
}

# Execute Query
df = pd.read_sql(queries[query_map[option]], engine)

st.subheader(option)
st.dataframe(df, use_container_width=True)

# Charts (Auto where applicable)
if "avg" in query_map[option] or "total" in query_map[option]:
    fig = px.bar(df, x=df.columns[0], y=df.columns[1])
    st.plotly_chart(fig, use_container_width=True)


st.sidebar.header("Filters & Search")

# Load data for filter options
df_all = pd.read_sql("SELECT * FROM rides", engine)

# Vehicle Type Filter
vehicle_types = df_all['Vehicle_Type'].unique().tolist()
selected_vehicle = st.sidebar.multiselect("Select Vehicle Type", vehicle_types, default=vehicle_types)

# Booking Status Filter
statuses = df_all['Booking_Status'].unique().tolist()
selected_status = st.sidebar.multiselect("Select Booking Status", statuses, default=statuses)

# Payment Method Filter
payment_methods = df_all['Payment_Method'].unique().tolist()
selected_payment = st.sidebar.multiselect("Select Payment Method", payment_methods, default=payment_methods)

# Customer Search
customer_id_search = st.sidebar.text_input("Search by Customer ID")

# Date Range Filter (if booking_date exists)
if 'Booking_Date' in df_all.columns:
    df_all['Booking_Date'] = pd.to_datetime(df_all['Booking_Date'])
    min_date = df_all['Booking_Date'].min()
    max_date = df_all['Booking_Date'].max()
    selected_dates = st.sidebar.date_input("Booking Date Range", [min_date, max_date])
else:
    selected_dates = [None, None]

# -------------------------------
# Filtered SQL Query
# -------------------------------
query = "SELECT * FROM rides WHERE 1=1"

# Dynamic filters
if selected_vehicle:
    query += f" AND Vehicle_Type IN ({','.join(['\''+v+'\'' for v in selected_vehicle])})"
if selected_status:
    query += f" AND Booking_Status IN ({','.join(['\''+s+'\'' for s in selected_status])})"
if selected_payment:
    # query += f" AND Payment_Method IN ({','.join(['\''+p+'\'' for p in selected_payment])})"

    query += f" AND Payment_Method IN ({','.join([f'\'{p}\'' for p in selected_payment if p is not None])})"

if customer_id_search:
    query += f" AND Customer_Id LIKE '%{customer_id_search}%'"
if selected_dates[0] and selected_dates[1] and 'Booking_Date' in df_all.columns:
    start = selected_dates[0].strftime('%Y-%m-%d')
    end = selected_dates[1].strftime('%Y-%m-%d')
    query += f" AND booking_date BETWEEN '{start}' AND '{end}'"

# Execute query
filtered_df = pd.read_sql(query, engine)

# -------------------------------
# Display Filtered Data
# -------------------------------
st.subheader("📄 Filtered Ride Data")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# Optional Charts
# -------------------------------
if not filtered_df.empty:
    st.subheader("📊 Ride Insights Visuals")

    # Ride count by booking status
    ride_status_fig = px.bar(
        filtered_df.groupby("Booking_Status")["Booking_ID"].count().reset_index(name="Count"),
        x="Booking_Status",
        y="Count",
        title="Booking Status Distribution"
    )
    st.plotly_chart(ride_status_fig, use_container_width=True)

    # Average ride distance per vehicle
    avg_distance_fig = px.bar(
        filtered_df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index(name="Avg Ride Distance"),
        x="Vehicle_Type",
        y="Avg Ride Distance",
        title="Average Ride Distance by Vehicle Type"
    )
    st.plotly_chart(avg_distance_fig, use_container_width=True)

st.subheader("📊 Power BI – Ola Ride Insights")

powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=e446ef9b-c6d1-46cb-ac5b-275841c74400&autoAuth=true&ctid=45278b5c-6595-4247-92e9-16e4dc3ff223"

st.components.v1.iframe(
    src=powerbi_url,
    height=700,
    width=1200,
    scrolling=True
)