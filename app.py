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
import streamlit as st

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Puchib763@',
        port=3306,
        database='ola',
        connection_timeout=5
    )
    if connection.is_connected():
        st.success("Connected to MySQL!")

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

except Exception as e:
    st.error(f"Error: {e}")

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

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Ride Booking Analytics Assistant",
    page_icon="🚖",
    layout="wide"
)

st.title("🚖 Interactive Ride Booking Assistant")

# 2. Sample Dataset matching your screenshot
@st.cache_data
def load_data():
    data = {
        'Ride ID': [
            'CNR7153255142', 'CNR2940424040', 'CNR2982357879', 'CNR2395710036',
            'CNR1797421769', 'CNR8787177882', 'CNR3612067560', 'CNR5374902489',
            'CNR5030602354', 'CNR6328453219', 'CNR4787583516', 'CNR7943634301',
            'CNR4524472111', 'CNR3914552212', 'CNR8181602032', 'CNR8090918544',
            'CNR3211335290', 'CNR3196156650', 'CNR9975925287', 'CNR1591113431'
        ],
        'Booking Value': [
            450, 160, 390, 385, 825, 175, 145, 345,
            840, 895, 165, 400, 330, 430, 380, 345,
            370, 405, 345, 1250
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Define the 10 Allowed Questions & Answers
ALLOWED_QUESTIONS = {
    1: "What is the highest booking value?",
    2: "Which Ride ID has the maximum booking value?",
    3: "What is the lowest booking value?",
    4: "What is the average booking value?",
    5: "What is the total booking value across all rides?",
    6: "How many total rides are in the dataset?",
    7: "Show the bar chart of booking values across Ride IDs.",
    8: "What is the median booking value?",
    9: "Which rides have a booking value over 800?",
    10: "Can I see the full dataset table?"
}

# 4. Sidebar listing allowed questions for easy reference
with st.sidebar:
    st.header("📋 Supported Questions")
    st.write("You can ask any of the following 10 questions:")
    for num, q in ALLOWED_QUESTIONS.items():
        st.markdown(f"**{num}.** {q}")

# 5. Question Handling Function
def answer_question(user_query: str):
    query = user_query.strip().lower()
    
    # Matching logic with allowed questions
    if "highest booking value" in query or "maximum booking value" in query and "which ride id" not in query:
        max_val = df['Booking Value'].max()
        st.success(f"**Highest Booking Value:** ₹{max_val}")
        
    elif "which ride id has the maximum" in query or "which ride id has the highest" in query:
        max_row = df.loc[df['Booking Value'].idxmax()]
        st.success(f"**Ride ID:** `{max_row['Ride ID']}` has the maximum booking value of **₹{max_row['Booking Value']}**.")
        
    elif "lowest booking value" in query or "minimum booking value" in query:
        min_val = df['Booking Value'].min()
        st.success(f"**Lowest Booking Value:** ₹{min_val}")
        
    elif "average booking value" in query or "mean booking value" in query:
        avg_val = df['Booking Value'].mean()
        st.info(f"**Average Booking Value:** ₹{avg_val:.2f}")
        
    elif "total booking value" in query or "sum of booking values" in query:
        total_val = df['Booking Value'].sum()
        st.info(f"**Total Booking Value:** ₹{total_val:,}")
        
    elif "how many total rides" in query or "total number of rides" in query or "number of rides" in query:
        total_rides = len(df)
        st.info(f"**Total Rides Count:** {total_rides} rides")
        
    elif "bar chart" in query or "chart" in query or "graph" in query or "plot" in query:
        fig = px.bar(
            df, x='Ride ID', y='Booking Value', 
            title='Booking Value by Ride ID',
            labels={'Booking Value': 'Booking Value', 'Ride ID': 'Ride ID'},
            color_discrete_sequence=['#2E8B57']
        )
        fig.update_xaxes(tickangle=-90)
        st.plotly_chart(fig, use_container_width=True)
        
    elif "median booking value" in query:
        median_val = df['Booking Value'].median()
        st.info(f"**Median Booking Value:** ₹{median_val:.2f}")
        
    elif "over 800" in query or "greater than 800" in query or "above 800" in query:
        filtered_df = df[df['Booking Value'] > 800]
        st.write("**Rides with Booking Value > 800:**")
        st.dataframe(filtered_df, use_container_width=True)
        
    elif "full dataset" in query or "table" in query or "raw data" in query or "show the dataset" in query:
        st.write("**Full Dataset Table:**")
        st.dataframe(df, use_container_width=True)
        
    else:
        # Fallback response for unlisted/out-of-scope questions
        st.error("Sorry, I am not in a position to answer the question.")

# 6. Interactive Interface Options
st.subheader("💬 Ask a Question")

tab1, tab2 = st.tabs([" Type Question", " Select Question from List"])

with tab1:
    user_input = st.text_input("Enter your question below:", placeholder="e.g., What is the highest booking value?")
    if st.button("Ask Question", key="btn_text"):
        if user_input:
            answer_question(user_input)
        else:
            st.warning("Please enter a question.")

with tab2:
    selected_q = st.selectbox("Choose one of the 10 questions:", list(ALLOWED_QUESTIONS.values()))
    if st.button("Get Answer", key="btn_select"):
        answer_question(selected_q)


















