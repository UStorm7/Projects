# Importing required libraries/ flask
import json
import sqlite3
from flask import Flask, jsonify, request, render_template, send_from_directory

# Loading JSON data
with open('jsondata.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)

# Initializing database
conn = sqlite3.connect('dashboard.db')
cursor = conn.cursor()

# Creating table
cursor.execute('''
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    end_year TEXT,
    intensity INTEGER,
    sector TEXT,
    topic TEXT,
    insight TEXT,
    url TEXT,
    region TEXT,
    start_year TEXT,
    impact TEXT,
    added TEXT,
    published TEXT,
    country TEXT,
    relevance INTEGER,
    pestle TEXT,
    source TEXT,
    title TEXT,
    likelihood INTEGER
)
''')

# Inserting data
for entry in data:
    cursor.execute('''
    INSERT INTO insights (end_year, intensity, sector, topic, insight, url, region, start_year, impact, 
    added, published, country, relevance, pestle, source, title, likelihood)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (
        entry.get('end_year', ''), entry.get('intensity', 0), entry.get('sector', ''), entry.get('topic', ''),
        entry.get('insight', ''), entry.get('url', ''), entry.get('region', ''), entry.get('start_year', ''),
        entry.get('impact', ''), entry.get('added', ''), entry.get('published', ''), entry.get('country', ''),
        entry.get('relevance', 0), entry.get('pestle', ''), entry.get('source', ''), entry.get('title', ''),
        entry.get('likelihood', 0)
    ))

conn.commit()
conn.close()

# Initializing the Flask app
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('dashboard.db')
    cursor = conn.cursor()

    query = "SELECT end_year, intensity, likelihood, relevance, sector, topic, insight, region, city, country, pestle, source, swot FROM insights WHERE 1=1"
    params = []

    if 'topic' in request.args:
        query += " AND topic = ?"
        params.append(request.args['topic'])

    if 'country' in request.args:
        query += " AND country = ?"
        params.append(request.args['country'])

    if 'region' in request.args:
        query += " AND region = ?"
        params.append(request.args['region'])

    if 'city' in request.args:
        query += " AND city = ?"
        params.append(request.args['city'])

    if 'endyear' in request.args:
        query += " AND end_year = ?"
        params.append(request.args['endyear'])

    if 'sector' in request.args:
        query += " AND sector = ?"
        params.append(request.args['sector'])

    if 'pestle' in request.args:
        query += " AND pestle = ?"
        params.append(request.args['pestle'])

    if 'source' in request.args:
        query += " AND source = ?"
        params.append(request.args['source'])

    if 'swot' in request.args:
        query += " AND swot = ?"
        params.append(request.args['swot'])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    
    return jsonify([dict(zip(columns, row)) for row in rows])



@app.route('/')
def index():
    return render_template('index.html')

# Serve static folder files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
