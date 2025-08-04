import os
from flask import Flask, render_template, request, redirect, session, url_for
import boto3
import psycopg2

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')

# RDS PostgreSQL config
DB_HOST = os.environ.get('RDS_HOST')
DB_NAME = os.environ.get('RDS_DB_NAME')
DB_USER = os.environ.get('RDS_USER')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')

# AWS S3 config
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/upload')
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['username'] = username
            return redirect('/upload')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        file = request.files['file']
        if file:
            s3 = boto3.client('s3',
                              region_name='ap-southeast-3')
            s3.upload_fileobj(file, S3_BUCKET, file.filename)
            return f"File '{file.filename}' uploaded to S3 bucket."
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
