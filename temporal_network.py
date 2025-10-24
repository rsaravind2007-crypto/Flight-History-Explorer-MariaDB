import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date


# -------------------------------
#   Database Connection
# -------------------------------



# Optional: Use Streamlit Secrets for security
db_user = st.secrets["db_user"]          # dbpgf10986516
db_password = st.secrets["db_password"]  # Your SkySQL password
db_host = st.secrets["db_host"]          # serverless-europe-west2.sysp0000.db2.skysql.com
db_port = int(st.secrets["db_port"])     # 4053

def create_connection():
    """
    Create a connection to the remote MariaDB (SkySQL) database using SSL.
    Reads credentials from Streamlit secrets.
    """
    try:
        conn = mysql.connector.connect(
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            host=st.secrets["db_host"],
            port=st.secrets["db_port"],
            database="openflights",  # your database name
            #ssl_ca="certs/skysql_chain.pem",       # path to SSL chain file
            #ssl_cert="certs/client-cert.pem",      # path to client certificate
            #ssl_key="certs/client-key.pem"         # path to client key
        )
        return conn

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
# -----------------------------------
# Create routes table if doesn't exists
# -----------------------------------
def create_routes_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS routes (
        route_id INT AUTO_INCREMENT PRIMARY KEY,
        Airline VARCHAR(10),
        Airline_ID INT,
        Source_airport VARCHAR(10),
        Source_airport_ID INT,
        Destination_airport VARCHAR(10),
        Destination_airport_ID INT,
        Codeshare VARCHAR(10),
        Stops INT,
        Equipment VARCHAR(100),
        row_start TIMESTAMP(6) GENERATED ALWAYS AS ROW START,
        row_end TIMESTAMP(6) GENERATED ALWAYS AS ROW END,
        PERIOD FOR SYSTEM_TIME (row_start, row_end)
    ) WITH SYSTEM VERSIONING;
    """
    
    try:
        cursor.execute(create_table_query)
        conn.commit()
        st.success("Table 'routes' exists or has been created successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error creating table: {err}")
    finally:
        cursor.close()
        conn.close()

create_routes_table()

# -------------------------------
#    Add a new route
# -------------------------------
def add_route(airline, airline_id, source_airport, dest_airport):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO routes (Airline, Airline_ID, Source_airport, Destination_airport) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (airline.upper(), airline_id, source_airport.upper(), dest_airport.upper()))
        conn.commit()
        st.success(f"Route added successfully with route_id {cursor.lastrowid}")
    except mysql.connector.Error as err:
        st.error(f"Failed to add route: {err}")
    finally:
        cursor.close()
        conn.close()

# -------------------------------
#   Update an existing route
# -------------------------------
def update_route(route_id, field, value):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        query = f"UPDATE routes SET {field} = %s WHERE route_id = %s"
        cursor.execute(query, (value, route_id))
        conn.commit()
        st.success(f"Route {route_id} updated: {field} → {value}")
    except mysql.connector.Error as err:
        st.error(f"Update failed: {err}")
    finally:
        cursor.close()
        conn.close()

# -------------------------------
#    Fetch historical data
# -------------------------------
def fetch_history(route_id, start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    start_date_str = f"{start_date} 00:00:00"
    end_date_str = f"{end_date} 23:59:59"
    
    try:
        query = f"""
        SELECT route_id, Airline, Airline_ID, Source_airport, Source_airport_ID,
               Destination_airport, Destination_airport_ID, Codeshare, Stops, Equipment,
               row_start, row_end
        FROM routes
        FOR SYSTEM_TIME BETWEEN '{start_date_str}' AND '{end_date_str}'
        WHERE route_id = {route_id};
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return pd.DataFrame(data)
    except mysql.connector.Error as err:
        st.error(f"Failed to fetch history: {err}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()

# -------------------------------
#    Streamlit UI
# -------------------------------
st.set_page_config(page_title="Flight History Explorer Powered By MariaDB", page_icon="✈️", layout="wide")
st.title("✈️ Flight History Explorer")
st.write("Add, update, and track changes to flight routes over time.")

tab1, tab2, tab3 = st.tabs(["Add Route", "Update Route", "View History"])

# -------------------------------
# Tab 1: Add Route
# -------------------------------
with tab1:
    st.subheader("Add a New Route")
    airline = st.text_input("Airline Code:")
    airline_id = st.number_input("Airline ID:", min_value=1, step=1)
    source_airport = st.text_input("Source Airport Code:")
    dest_airport = st.text_input("Destination Airport Code:")
    if st.button("Add Route"):
        if airline and source_airport and dest_airport:
            add_route(airline, airline_id, source_airport, dest_airport)
        else:
            st.warning("Please enter Airline, Source, and Destination airport codes.")

# -------------------------------
# Tab 2: Update Route
# -------------------------------
with tab2:
    st.subheader("Update Existing Route")
    route_id = st.number_input("Route ID to Update:", min_value=1, step=1)
    field = st.selectbox("Select Field to Update:", ["Airline_ID", "Source_airport", "Destination_airport"])
    value = st.text_input("New Value:")
    if st.button("Update Route"):
        if value:
            if field == "Airline_ID":
                try:
                    value = int(value)
                except:
                    st.error("Airline ID must be a number.")
                    st.stop()
            update_route(route_id, field, value.upper() if field != "Airline_ID" else value)
        else:
            st.warning("Please enter a new value.")

# -------------------------------
# Tab 3: View History
# -------------------------------
with tab3:
    st.subheader("View Flight History")
    route_id_hist = st.number_input("Route ID:", min_value=1, step=1, key="hist_id")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", value=date(2025,1,1))
    with col2:
        end_date = st.date_input("End Date:", value=date.today())
    
    if st.button("Show History"):
        df = fetch_history(route_id_hist, start_date, end_date)
        if df.empty:
            st.warning("No historical records found for this route.")
        else:
            st.success(f"Found {len(df)} historical records.")
            st.dataframe(df)
            

