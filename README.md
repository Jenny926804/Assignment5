# City Map Agent — Assignment 5

## Overview
This assignment implements an city navigation assistant that can find places, explore nearby points of interest, and compute optimal routes using two custom-built map servers:

1. **City POI Explorer Server (Nominatim-based)**  
   - Provides **Point-of-Interest search**, **category search**, and **Geocoding**.

2. **OSRM Routing Server**  
   - Provides **routing**, **distance estimation**, and **nearest road network snap**.

Together, these servers expose **three required mapping operations**:
- **POI Search** (City POI Explorer)  
- **Routing** (OSRM Routing Server)  
- **Geocoding / Nearest Routable Point** (OSRM Routing Server)  
---

## Project Structure

```
Assignment5/
│── agents/
│   ├── map_agent.py        # Main agent implementation
│── map_servers/
│   ├── city_poi_server.py  # Nominatim MCP server
│   ├── osrm_routing_server.py # OSRM MCP server
│── tests/
│   ├── test_city_poi_server.py
│   ├── test_osrm_routing_server.py
│── README.md
│── requirements.txt
```

---

## How It Works

### **1. City POI Explorer Server**
Runs a lightweight MCP server that wraps the **Nominatim** API.  
Exposed tools:
- `search_poi(city, query, limit)`
- `search_category(city, category, limit)`

Example:
```json
{
  "city": "Beirut",
  "query": "pharmacy",
  "results": [...]
}
```

---

### **2. OSRM Routing Server**
Uses an OSRM backend (HTTP API) to provide:
- `route(start_lat, start_lon, end_lat, end_lon, profile)`
- `nearest_routable(lat, lon, profile)`

Example:
```json
{
  "distance_m": 1423.2,
  "duration_s": 210.5
}
```

---

### **3. Map Agent**
The AI agent:
- Automatically chooses the correct MCP server  
- Executes routing + POI queries  
- Summarizes the final answer in human-friendly format  

---

## Running the Agent

### 1. Activate your virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
### 2. Install dependencies using:

```bash
pip install -r requirements.txt
```

### 3. Run the map servers:
```bash
python map_servers/city_poi_server.py
python map_servers/osrm_routing_server.py
```

### 4. Run the map agent:

```bash
python agents/map_agent.py
```

You will see:

```
Ask a mapping question:
```

Type something like:

```
Find me nearest Lebanese restaurants in Beirut and calculate driving distance from AUB
Find me Audi Banks in Beirut and generate directions to rach them from AUB
```

---


## Agent in Action
Sample input/output:
Ask a mapping question (or type exit): Find me nearest Lebanese restaurants in Beirut and calculate driving distance from AUB

=== Final Answer ===

Here are the nearest Lebanese restaurants to the American University of Beirut (AUB), with calculated driving distances:

1. **Rizk** (شارع عبد الحميد الزهراوي, البسطة التحتا)
   - Distance: 3.7 km
   - Estimated drive: ~4.5 minutes

2. **Khalife** (شارع البسطة, البسطة الفوقا)
   - Distance: 3.6 km
   - Estimated drive: ~4.5 minutes

3. **Em Sherif** (شارع فيكتور هوغو, مونو)
   - Distance: 4.5 km
   - Estimated drive: ~5.8 minutes

4. **عنبر مطعم** (طريق الشام, البسطة التحتا)
   - Distance: 4.3 km
   - Estimated drive: ~5.2 minutes

5. **لا بيازا** (طريق الشام, الناصرة)
   - Distance: 4.3 km
   - Estimated drive: ~5.2 minutes


## Running Tests
To run the unit tests:

```
pytest -v
```

Expected output:

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0 -- /home/saugo/Desktop/Jenny/Agentic/AssignmentC5/Assignment5/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/saugo/Desktop/Jenny/Agentic/AssignmentC5/Assignment5
plugins: anyio-4.11.0
collected 4 items                                                              

tests/test_city_poi_server.py::test_search_poi PASSED                    [ 25%]
tests/test_city_poi_server.py::test_find_restaurants PASSED              [ 50%]
tests/test_osrm_routing_server.py::test_route PASSED                     [ 75%]
tests/test_osrm_routing_server.py::test_nearest PASSED                   [100%]

============================== 4 passed in 7.24s ===============================

```

---
