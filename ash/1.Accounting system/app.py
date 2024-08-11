from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            account_id INTEGER,
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/')
def home():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts').fetchall()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('index.html', accounts=accounts, transactions=transactions)

# Add transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        type = request.form['type']
        date = request.form['date']

        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (name, amount, type, date) VALUES (?, ?, ?, ?)',
                     (name, amount, type, date))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
