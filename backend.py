python -m pip install flask flask-cors "psycopg[binary]"
python -c "import flask, psycopg; print('Flask and PostgreSQL connector OK')"

app.py
from flask import Flask, jsonify, request
import psycopg

app = Flask(__name__)

DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "studentdb2",
    "user": "postgres",
    "password": "YOUR_PASSWORD"
}

def db():
    return psycopg.connect(**DB)

@app.route("/")
def home():
    return "Student API is running"

@app.route("/students")
def get_students():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name,email,course) VALUES (%s,%s,%s)",
        (data["name"], data["email"], data["course"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Student added"

if __name__ == "__main__":
    app.run(debug=True)
