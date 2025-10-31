# Flight History Explorer

Welcome to **Flight History Explorer**, a simple yet powerful web app built using **Python** and **MariaDB**. This project leverages MariaDB's **System Versioning** feature to track and analyze changes to flight routes over time.  

---

## Overview

Managing flight routes can be complex, especially when airlines frequently update schedules, destinations, or codeshares. This project provides a **user-friendly interface** to:  

- Add new flight routes  
- Update existing routes  
- Track changes over time with historical records  



---

## Features

1. **Add a New Route:**  
   Enter airline ID, source, and destination airport codes to add a route.

2. **Update Existing Route:**  
   Select a route and update its airline ID, source, or destination airport. All changes are recorded automatically.

3. **View Flight History:**  
   Pick a route and a date range to view historical changes. See who operated the route, when changes occurred, and the evolution of the route over time.

4. **Visualization:**  
   The app includes a simple chart to visualize changes in route details over time.  

---

## Technology Stack

- **Frontend:** Python (Streamlit)  
- **Database:** MariaDB (with System Versioning / Temporal Tables)  
- **Data:** OpenFlights routes dataset  

---

## Features Leveraging MariaDB

1. **System Versioning (Temporal Tables):**  
   - Every route update is automatically tracked and no additional tables or triggers required.  
   - `row_start` and `row_end` timestamps indicate when a record was active.  
   - Users can query changes for any date range to analyze past airline routes.


2. **Flexible Data Updates:**  
   - Add or modify routes without breaking historical tracking.  
   - Supports dynamic analysis of route evolution over time.
   - MariaDB efficiently handles large datasets and system-versioned queries. 

---

## Key Concepts

- **Airline Code:** Short code representing an airline.  
- **Airline ID:** Unique numeric ID corresponding to the airline in the database.  
- **Row Start & Row End:** Automatically generated timestamps indicating when a row became active and when it was replaced.  

MariaDB’s **system versioning** feature keeps track of all historical changes without extra manual effort.  

---
## How to Run / Implement This Project

### Install Dependencies

- Requires python 3.12+ version and Then install required packages:
- pip install -r requirements.txt

### Set Up MariaDB

#### If hosting in Locally ( LocalHost) :
- Install the latest version of MariaDB.
- Create a database, for example openflights : CREATE DATABASE openflights;
- Create the routes table using the structure defined in temporal.py.
- Download the openflights dataset from browser and load the data into the database or you can add data one by one.
- clone the repository and use the code ( temporal.py) ,update the database connection and run the file using the command "streamlit run <module_name>.py".

#### If hosting in skysql (Online) :
- Create a SkySQL account and set up a database service.
- Create the airports table with the structure as defined in source code and load the airport dataset. (or you can add data one by one)
- Create a Streamlit Cloud account to host the web app online.
- Use the spatial_GIS_network.py code and update the connection credentials to your SkySQL database.
- Deploy the Streamlit app via Streamlit Cloud for online access. 
---
### I have deployed the project using SkySQL’s free tier. The website is currently working fine as of October 31, 2025, but I am not certain whether it will remain active during the evaluation period.
### website link : https://flight-history-explorer-mariadb-k6kyfhw7ju22zzgwmzsoj7.streamlit.app/

## Author

Developed for the **MariaDB Hackathon** by ARAVIND R S

---
