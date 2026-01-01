from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Database Connection

def get_db():
    return sqlite3.connect('lms.db')

# create tables 

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY, title TEXT, description TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS progress(id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER, status TEXT)")
    con.commit()
    con.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        if user:
            session['user'] = user[0]
            return redirect('/profile')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        con = get_db()
        con.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        con.commit()
        return redirect('/')
    return render_template('register.html')    
 

@app.route('/progress')
def progress():
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    data = con.execute("SELECT * FROM progress").fetchall()
    return render_template('progress.html', data=data)

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/')
    con =  get_db()
    user = con.execute("SELECT * FROM users WHERE id=?", (session['user'],)).fetchone()
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)    



