from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_FILE = 'tickets.db'

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    cur = con.execute(query, args)
    rv = cur.fetchall()
    con.commit()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    # Fetch all open tickets
    tickets = query_db("SELECT * FROM tickets WHERE status != 'Closed' ORDER BY priority DESC")
    return render_template('index.html', tickets=tickets)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    priority = request.form.get('priority')
    query_db("INSERT INTO tickets (title, priority) VALUES (?, ?)", (title, priority))
    return redirect('/')

@app.route('/close/<int:id>')
def close(id):
    query_db("UPDATE tickets SET status = 'Closed' WHERE id = ?", (id,))
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
