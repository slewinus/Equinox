from flask import Flask, render_template, redirect, url_for, session, request
from classes import User, GraphDic, Community, Submission
import mysql.connector, os, re

app = Flask(__name__)

app.secret_key = os.urandom(12).hex()
mydb = mysql.connector.connect(
    host="sql280.main-hosting.eu",
    user="u938835060_test",
    password="AGIEXx6hB]",
    database="u938835060_elliott"
)


@app.route('/home')
def home():
    if 'loggedin' in session:
        user_id = session['id']
        subs, posts = get_content(user_id)
        return render_template('index.html', subs=subs, posts=posts, user=User(session['username'], session['password'], session['img_link']))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['password'] = account[4]
            session['img_link'] = account[5]
            # Redirect to home page
            cursor.close()
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (NULL, %s, "", "", %s, "")', (username, password,))
            mydb.commit()
            msg = 'You have successfully registered!'
        cursor.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/suggestions/')
def suggest():
    if 'loggedin' in session:
        return render_template('suggestions.html')
    return redirect(url_for('login'))


@app.route('/like_post/', methods=['POST'])
def like_post():
    return render_template('index.html')


def get_content(user_id):
    cursor = mydb.cursor()
    user_id = session['id']
    cursor.execute(
        'SELECT c.id, c.name, c.img_link FROM communities AS c JOIN communities_sub AS cs ON c.id = cs.comm_id WHERE cs.user_id = %s',
        (user_id,))
    communities = cursor.fetchall()
    subs = [Community(s[1], s[2]) for s in communities]

    cursor.execute('SELECT posts.user_id, posts.title, posts.text, posts.likes, posts.dislikes, posts.id, posts.img_link, posts.comm_id FROM posts JOIN friendships AS f ON posts.user_id = f.user1_id WHERE f.user2_id = %s', (user_id,))
    result = cursor.fetchall()
    cursor.execute(
        'SELECT posts.user_id, posts.title, posts.text, posts.likes, posts.dislikes, posts.id, posts.img_link, posts.comm_id FROM posts JOIN friendships AS f ON posts.user_id = f.user2_id WHERE f.user1_id = %s',
        (user_id,))
    result += cursor.fetchall()
    posts = []
    for p in result:
        cursor.execute('SELECT * FROM user WHERE id=%s', (p[0],))
        u = cursor.fetchone()
        u = User(u[1], u[4], u[5])
        cursor.execute('SELECT * FROM communities WHERE id=%s', (p[7],))
        c = cursor.fetchone()
        if c is not None:
            c = Community(c[1], c[2])
        else:
            c = Community('General', '')
        posts.append(Submission(u, p[1], p[2], p[3], p[4], p[5], c, p[6]))
    cursor.close()
    return subs, posts


if __name__ == '__main__':
    app.run()
