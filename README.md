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

## 📊 Technology Stack

- **Frontend:** Streamlit (Python)  
- **Database:** MariaDB (with System Versioning / Temporal Tables)  
- **Data:** OpenFlights routes dataset  

---

## 🛠️ Features Leveraging MariaDB

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

- **Airline Code:** Short code representing an airline (e.g., "2B" for Air Moldova).  
- **Airline ID:** Unique numeric ID corresponding to the airline in the database.  
- **Row Start & Row End:** Automatically generated timestamps indicating when a row became active and when it was replaced.  

MariaDB’s **system versioning** feature keeps track of all historical changes without extra manual effort.  

---

## 👤 Author

Developed for the **MariaDB Hackathon** by ARAVIND R S

---
