from flask import Flask, render_template, request, redirect
import sqlite3, random, string

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('urls.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT,
                  short_code TEXT UNIQUE)''')
    conn.commit()
    conn.close()

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        url = request.form['url']
        code = generate_code()
        conn = sqlite3.connect('urls.db')
        conn.execute('INSERT INTO urls(original_url, short_code) VALUES (?,?)',(url, code))
        conn.commit()
        conn.close()
        short_url = request.host_url + code
    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirect_url(code):
    conn = sqlite3.connect('urls.db')
    row = conn.execute('SELECT original_url FROM urls WHERE short_code=?',(code,)).fetchone()
    conn.close()
    if row:
        return redirect(row[0])
    return 'URL not found'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
