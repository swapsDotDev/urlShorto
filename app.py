from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
import string
import random
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'  # Use env var in production

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'urlshortener'),
    'charset': 'utf8mb4',
    'autocommit': True
}


def get_db():
    """Get MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        raise


def init_db():
    """Initialize database tables."""
    # First connect without database to create it if it doesn't exist
    create_db_config = DB_CONFIG.copy()
    del create_db_config['database']
    
    try:
        conn = mysql.connector.connect(**create_db_config)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        conn.close()
        
        # Now connect to the specific database
        conn = get_db()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create urls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                long_url TEXT NOT NULL,
                short_code VARCHAR(255) UNIQUE NOT NULL,
                user VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_short_code (short_code),
                INDEX idx_user (user)
            )
        ''')
        
        cursor.close()
        conn.close()
        print("Database initialized successfully")
        
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
        raise


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        custom_code = request.form.get('custom_code')
        user = session.get('username')

        # Add URL validation
        if not re.match(r'^https?://', long_url):
            flash('Invalid URL')
            return redirect('/')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        try:
            if custom_code:
                code = custom_code
            else:
                code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            cursor.execute(
                'INSERT INTO urls (long_url, short_code, user) VALUES (%s, %s, %s)',
                (long_url, code, session.get('username'))
            )
            conn.commit()
            flash(f'URL shortened successfully! Your short URL: {request.host_url + code}')
            return redirect('/')
        except mysql.connector.IntegrityError:
            flash('Custom code already taken.')
            return redirect('/')
        finally:
            cursor.close()
            conn.close()
    return render_template('index.html')


@app.route('/<code>')
def redirect_url(code):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT long_url FROM urls WHERE short_code = %s', (code,))
        url = cursor.fetchone()
        if url:
            return redirect(url['long_url'])
        else:
            return render_template('error.html'), 404
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT * FROM users WHERE username = %s AND password = %s', (username, password)
            )
            user = cursor.fetchone()
            if user:
                session['username'] = username
                flash('Login successful!')
                return redirect('/')
            else:
                flash('Invalid credentials')
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash('Username already exists.')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    