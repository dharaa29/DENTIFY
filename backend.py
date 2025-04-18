from flask import Flask, render_template, request, redirect, session
import cv2
import os
import datetime
import sqlite3
import numpy as np

app = Flask(__name__)
app.secret_key = "secret_key"


# Create or connect to the SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                mobile TEXT NOT NULL,
                balance REAL DEFAULT 500
            )''')

conn.commit()
# Routes
@app.route('/')
def home():
    return render_template('home.html')

        


@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        mobile = request.form['mobile']
        
       
        
        c.execute("INSERT INTO users (id, name, password, mobile) VALUES (?, ?, ?, ?)", (user_id, name, password, mobile))
        conn.commit()
        c.close()
        
        session['user_id'] = user_id
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE id = ? AND password = ?", (user_id, password))
        user = c.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if 'user_id' in session:
        user_id = session['user_id']
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        return render_template('dashboard.html', user=user)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
