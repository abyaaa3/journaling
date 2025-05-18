from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret'  # Change this!
DB_FILE = 'journal.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.before_request
def require_login():
    if request.endpoint != 'login' and 'logged_in' not in session:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'your-password':  # Change this!
            session['logged_in'] = True
            return redirect('/')
    return """
        <form method='POST'>
            <input name='password' type='password' placeholder='Password'>
            <input type='submit' value='Login'>
        </form>
    """

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM entries ORDER BY date DESC')
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/new', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO entries (title, content, date) VALUES (?, ?, ?)', (title, content, date))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('new.html')

@app.route('/delete/<int:id>')
def delete_entry(id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM entries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
