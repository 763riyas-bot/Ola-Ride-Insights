import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import mysql.connector
import streamlit as st
from pathlib import Path
df = pd.read_excel(r"C:\Users\USER\OneDrive\Desktop\project_2\OLA_DataSet.xlsx")


# Force empty strings to NaN so missing values match notebook
df.replace("", np.nan, inplace=True)

print(df.isnull().sum())
print(100*df.isnull().sum()/df.shape[0])
plt.boxplot(df["V_TAT"])
plt.show()
df["V_TAT"] = df["V_TAT"].fillna(df["V_TAT"].median())
plt.boxplot(df["C_TAT"])
plt.show()
df["C_TAT"] = df["C_TAT"].fillna(df["C_TAT"].median())
# Clean 'Canceled_Rides_by_Customer' using mode
mode_value = df['Canceled_Rides_by_Customer'].mode()[0]   # get the most frequent value
df['Canceled_Rides_by_Customer'].fillna(mode_value, inplace=True)
# Clean 'Canceled_Rides_by_Driver' using mode
mode_driver = df['Canceled_Rides_by_Driver'].mode()[0]   # most frequent value
df['Canceled_Rides_by_Driver'].fillna(mode_driver, inplace=True)
df['Incomplete_Rides'] = df['Incomplete_Rides'].fillna(df['Incomplete_Rides'].mode()[0])
# Clean 'Incomplete_Rides_Reason' using mode
mode_reason = df['Incomplete_Rides_Reason'].mode()[0]   # most frequent value
df['Incomplete_Rides_Reason'].fillna(mode_reason, inplace=True)
# Clean 'Payment_Method' using mode
mode_payment = df['Payment_Method'].mode()[0]   # most frequent value
df['Payment_Method'].fillna(mode_payment, inplace=True)
plt.boxplot(df["Driver_Ratings"])
plt.title("Boxplot of Driver Ratings")
plt.ylabel("Ratings")
plt.show()
# Clean 'Driver_Ratings' using median
median_driver = df["Driver_Ratings"].median()
df["Driver_Ratings"].fillna(median_driver, inplace=True)
plt.boxplot(df["Customer_Rating"])
plt.title("Boxplot of Customer Rating")
plt.ylabel("Ratings")
plt.show()
median_customer = df["Customer_Rating"].median()
df["Customer_Rating"].fillna(median_customer, inplace=True)
#  fill numeric columns with median
df['V_TAT'] = df['V_TAT'].fillna(df['V_TAT'].median())
df['C_TAT'] = df['C_TAT'].fillna(df['C_TAT'].median())

#  fill categorical columns with mode
df['Canceled_Rides_by_Customer'] = df['Canceled_Rides_by_Customer'].fillna(df['Canceled_Rides_by_Customer'].mode()[0])
df['Canceled_Rides_by_Driver'] = df['Canceled_Rides_by_Driver'].fillna(df['Canceled_Rides_by_Driver'].mode()[0])
df['Incomplete_Rides_Reason'] = df['Incomplete_Rides_Reason'].fillna(df['Incomplete_Rides_Reason'].mode()[0])
df['Payment_Method'] = df['Payment_Method'].fillna(df['Payment_Method'].mode()[0])
df['Driver_Ratings'] = df['Driver_Ratings'].fillna(df['Driver_Ratings'].median())  # numeric
df['Customer_Rating'] = df['Customer_Rating'].fillna(df['Customer_Rating'].median())  # numeric
# Handling missing values
print(df.isnull().sum())
import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Puchib763@',
        port=3307,
        database='ola',
        connection_timeout=5   # fail fast if unreachable
    )
    if connection.is_connected():
        print("Connected to MySQL!")
except Exception as e:
    print("Error:", e)

#✅ Create the cursor 
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS rides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    ride_distance FLOAT
)
"""
cursor.execute(create_table_query)
connection.commit()
# Create table
create_table_query = """
CREATE TABLE IF NOT EXISTS ola_data (
    Booking_ID INT PRIMARY KEY,
    Customer_ID INT,
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    Booking_Status VARCHAR(20),
    Booking_Value DECIMAL(10,2),
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT
);
"""

cursor.execute(create_table_query)
connection.commit()

print("Table created successfully!")

import mysql.connector
import pandas as pd
import streamlit as st

st.title("OLA Ride Data Dashboard")
st.subheader("Question")
st.write("Retrieve all successful bookings from the ola_data table.")

try:
    # ✅ Correct connection with password and port
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Puchib763@",   # <-- your password
        port=3307,               # <-- your port
        database="ola"
    )

    query = "SELECT * FROM ola_data WHERE Booking_Status = 'Success';"
    df = pd.read_sql(query, conn)

    st.subheader("Data - Successful Bookings")
    st.dataframe(df)

    st.subheader("Visualization - Successful Bookings by Vehicle Type")
    st.bar_chart(df["Vehicle_Type"].value_counts())

    st.subheader("Visualization - Successful Bookings by Pickup Location")
    st.bar_chart(df["Pickup_Location"].value_counts().head(10))

except Exception as e:
    st.error(f"Database connection failed: {e}")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "vehicle_type": ["Car", "Bike", "Car", "Bus", "Bike", "Car", "Bus", "Bike"],
    "ride_distance": [12.5, 5.2, 8.7, 15.0, 6.1, 10.3, 18.4, 4.8]
}
df = pd.DataFrame(data)

# Question
st.header("Find the average ride distance for each vehicle type")

# Display data
st.subheader("Dataset")
st.dataframe(df)

# Calculate average ride distance per vehicle type
avg_distance = df.groupby("vehicle_type")["ride_distance"].mean().reset_index()

st.subheader("Average Ride Distance by Vehicle Type")
st.dataframe(avg_distance)

# Visualization
fig, ax = plt.subplots()
ax.bar(avg_distance["vehicle_type"], avg_distance["ride_distance"], color="skyblue")
ax.set_xlabel("Vehicle Type")
ax.set_ylabel("Average Ride Distance")
ax.set_title("Average Ride Distance per Vehicle Type")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "customer_id": [101, 102, 103, 104, 105, 106, 107, 108],
    "Canceled_Rides_by_Customer": [2, 0, 5, 1, 3, 0, 4, 2]
}
df = pd.DataFrame(data)

# Question
st.header("Get the total number of cancelled rides by customers")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Calculate total cancelled rides
total_cancelled = df["Canceled_Rides_by_Customer"].sum()

st.subheader("Total Cancelled Rides")
st.write(f"Total cancelled rides by customers: **{total_cancelled}**")

# Visualization
fig, ax = plt.subplots()
ax.bar(df["customer_id"], df["Canceled_Rides_by_Customer"], color="salmon")
ax.set_xlabel("Customer ID")
ax.set_ylabel("Cancelled Rides")
ax.set_title("Cancelled Rides by Each Customer")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "customer_id": [301, 302, 303, 304, 305, 306, 307, 308],
    "Booked_Rides": [25, 40, 12, 55, 33, 18, 47, 29]
}
df = pd.DataFrame(data)

# Question
st.header("List the top 5 customers who booked the highest number of rides")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Find top 5 customers
top_customers = df.sort_values(by="Booked_Rides", ascending=False).head(5)

st.subheader("Top 5 Customers by Booked Rides")
st.dataframe(top_customers)

# Visualization
fig, ax = plt.subplots()
ax.bar(top_customers["customer_id"].astype(str), top_customers["Booked_Rides"], color="green")
ax.set_xlabel("Customer ID")
ax.set_ylabel("Number of Rides Booked")
ax.set_title("Top 5 Customers with Highest Bookings")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "driver_id": [401, 402, 403, 404, 405],
    "Cancelled_Personal": [2, 1, 0, 3, 2],
    "Cancelled_CarIssues": [1, 0, 2, 1, 4]
}
df = pd.DataFrame(data)

# Question
st.header("Get the number of rides cancelled by drivers due to personal and car-related issues")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Calculate totals
total_personal = df["Cancelled_Personal"].sum()
total_car_issues = df["Cancelled_CarIssues"].sum()

st.subheader("Total Cancelled Rides")
st.write(f"Total cancelled due to personal issues: **{total_personal}**")
st.write(f"Total cancelled due to car-related issues: **{total_car_issues}**")

# Visualization
fig, ax = plt.subplots()
categories = ["Personal Issues", "Car-related Issues"]
totals = [total_personal, total_car_issues]
ax.bar(categories, totals, color=["blue", "red"])
ax.set_ylabel("Number of Cancelled Rides")
ax.set_title("Cancelled Rides by Reason")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "booking_id": [501, 502, 503, 504, 505, 506],
    "vehicle_type": ["Prime Sedan", "Prime Sedan", "Prime Sedan", "SUV", "Prime Sedan", "Prime Sedan"],
    "driver_rating": [4.5, 3.8, 4.9, 4.2, 2.7, 5.0]
}
df = pd.DataFrame(data)

# Question
st.header("Find the maximum and minimum driver ratings for Prime Sedan bookings")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Filter only Prime Sedan bookings
prime_sedan_df = df[df["vehicle_type"] == "Prime Sedan"]

# Calculate max and min ratings
max_rating = prime_sedan_df["driver_rating"].max()
min_rating = prime_sedan_df["driver_rating"].min()

st.subheader("Results")
st.write(f"Maximum driver rating for Prime Sedan bookings: **{max_rating}**")
st.write(f"Minimum driver rating for Prime Sedan bookings: **{min_rating}**")

# Visualization
fig, ax = plt.subplots()
ax.bar(["Max Rating", "Min Rating"], [max_rating, min_rating], color=["green", "red"])
ax.set_ylabel("Driver Rating")
ax.set_title("Maximum and Minimum Driver Ratings for Prime Sedan Bookings")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "ride_id": [601, 602, 603, 604, 605, 606],
    "customer_id": [701, 702, 703, 704, 705, 706],
    "payment_method": ["UPI", "Card", "Cash", "UPI", "Wallet", "UPI"],
    "ride_distance": [12.5, 8.3, 5.0, 15.2, 7.1, 9.8]
}
df = pd.DataFrame(data)

# Question
st.header("Retrieve all rides where payment was made using UPI")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Filter rides with UPI payment
upi_rides = df[df["payment_method"] == "UPI"]

st.subheader("Rides Paid via UPI")
st.dataframe(upi_rides)

# Visualization
fig, ax = plt.subplots()
ax.bar(upi_rides["ride_id"].astype(str), upi_rides["ride_distance"], color="purple")
ax.set_xlabel("Ride ID")
ax.set_ylabel("Ride Distance")
ax.set_title("UPI Payment Rides - Distance Distribution")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "customer_id": [801, 802, 803, 804, 805, 806, 807],
    "vehicle_type": ["Sedan", "SUV", "Sedan", "Hatchback", "SUV", "Sedan", "Hatchback"],
    "customer_rating": [4.5, 3.9, 4.2, 3.5, 4.1, 4.8, 3.7]
}
df = pd.DataFrame(data)

# Question
st.header("Find the average customer rating per vehicle type")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Calculate average rating per vehicle type
avg_rating = df.groupby("vehicle_type")["customer_rating"].mean().reset_index()

st.subheader("Average Customer Rating by Vehicle Type")
st.dataframe(avg_rating)

# Visualization
fig, ax = plt.subplots()
ax.bar(avg_rating["vehicle_type"], avg_rating["customer_rating"], color="teal")
ax.set_xlabel("Vehicle Type")
ax.set_ylabel("Average Customer Rating")
ax.set_title("Average Customer Rating per Vehicle Type")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "ride_id": [701, 702, 703, 704, 705, 706],
    "booking_status": ["Success", "Cancelled", "Success", "Success", "Cancelled", "Success"],
    "booking_value": [250, 180, 320, 150, 200, 400]
}
df = pd.DataFrame(data)

# Question
st.header("Calculate the total booking value of rides completed successfully")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Filter successful rides
successful_rides = df[df["booking_status"] == "Success"]

# Calculate total booking value
total_value = successful_rides["booking_value"].sum()

st.subheader("Total Booking Value of Successful Rides")
st.write(f"Total booking value: **₹{total_value}**")

# Visualization
fig, ax = plt.subplots()
ax.bar(successful_rides["ride_id"].astype(str), successful_rides["booking_value"], color="seagreen")
ax.set_xlabel("Ride ID")
ax.set_ylabel("Booking Value (₹)")
ax.set_title("Booking Value of Successful Rides")

st.pyplot(fig)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset
data = {
    "ride_id": [801, 802, 803, 804, 805],
    "customer_id": [901, 902, 903, 904, 905],
    "ride_status": ["Incomplete", "Success", "Incomplete", "Cancelled", "Incomplete"],
    "reason": ["Driver no-show", "Completed", "Payment failure", "Customer cancelled", "Car breakdown"]
}
df = pd.DataFrame(data)

# Question
st.header("List all incomplete rides along with the reason")

# Display dataset
st.subheader("Dataset")
st.dataframe(df)

# Filter incomplete rides
incomplete_rides = df[df["ride_status"] == "Incomplete"]

st.subheader("Incomplete Rides with Reasons")
st.dataframe(incomplete_rides)

# Visualization
fig, ax = plt.subplots()
reason_counts = incomplete_rides["reason"].value_counts()
ax.bar(reason_counts.index, reason_counts.values, color="crimson")
ax.set_xlabel("Reason")
ax.set_ylabel("Number of Incomplete Rides")
ax.set_title("Reasons for Incomplete Rides")

st.pyplot(fig)









