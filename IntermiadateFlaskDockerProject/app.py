from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection settings from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'flaskdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST
        )
        return conn
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return "Flask App with PostgreSQL!"

@app.route('/users')
def get_users():
    conn = connect_db()
    if isinstance(conn, str):
        return jsonify({"error": conn}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
