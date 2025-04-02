DATA VISUALIZATION DASHBOARD

A Data Visualization Dashboard built using Flask (backend) and JavaScript (D3.js) (frontend). It loads data from a JSON file into
an SQLite database and provides an API to fetch and visualize insights dynamically.

TECH
- Backend: Flask (Python), SQLite
- Frontend: HTML, CSS, JavaScript(D3.js)
- Styling (Extra): styles.css

FEATURES
- BAR CHART for Intensity by Topic
- SCATTER PLOT for Likelihood vs Relevance
- Users can filter data by end year, topic, sector, region, country, city, PEST, SWOT, source
- REST API: /api/data endpoint fetches data from the database

RUN
- Install flask
- Run flask app
- Open browser link: http://127.0.0.1:5000/

NOTES
- dashboard.db automatically created upon running app.py
- Ensure jsondata.json is present before running the app