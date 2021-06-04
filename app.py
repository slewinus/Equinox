import os
import re
from datetime import datetime

import mysql.connector
from flask import Flask, render_template, redirect, url_for, session, request

from feed import *
from user import *
from subquinox import *
from amis import *
from like import *

app = Flask(__name__)

app.secret_key = os.urandom(12).hex()


def connect():
    cnx = mysql.connector.connect(
            host="sql280.main-hosting.eu",
            user="u938835060_test",
            password="AGIEXx6hB]",
            database="u938835060_elliott")
    return cnx


def reconnect(cnx):
    if not cnx.is_connected():
        cnx = mysql.connector.connect(
            host="sql280.main-hosting.eu",
            user="u938835060_test",
            password="AGIEXx6hB]",
            database="u938835060_elliott")
        return cnx
    return cnx


global mydb
mydb = connect()


@app.route('/')
def home():
    if 'loggedin' in session and 'username' in session:
        global mydb
        mydb = reconnect(mydb)
        subs = get_all_subs(mydb)
        posts = get_home_feed(session['id'], mydb, 0, 10)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'], session['id'])
        return render_template('index.html', subs=subs, posts=posts, user=user)
    return redirect(url_for('login'))


@app.route('/post/', methods=['GET', 'POST'])
def post():
    if 'loggedin' in session and 'username' in session:
        global mydb
        mydb = reconnect(mydb)
        msg = ''
        if request.method == 'POST' and 'content' in request.form and 'titre' in request.form:
            titre = request.form['titre']
            content = request.form['content']
            comm = request.form['community']
            img = request.form['img']
            now = datetime.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor = mydb.cursor()
            cursor.execute('INSERT INTO posts VALUES(NULL, %s, %s, %s, %s, 0, 0, %s, %s)', (session['id'], titre, content, img, comm, date,))
            mydb.commit()
            cursor.close()
            msg = 'Post envoyé!'
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        subs = get_all_subs(mydb)
        return render_template('post.html', msg=msg, subs=subs, user=user)
    return redirect(url_for('login'))


@app.route('/community')
def community():
    if 'loggedin' in session and 'username' in session:
        comm_id = request.args.get('comm')
        global mydb
        mydb = reconnect(mydb)
        subs = get_all_subs(mydb)
        posts = get_sub_content(comm_id, session['id'], mydb, 0, 20)
        cursor = mydb.cursor()
        cursor.execute('SELECT c.id, c.name, c.img_link FROM communities AS c WHERE c.id = %s', (comm_id,))
        c = cursor.fetchone()
        cursor.close()
        comm = Subquinox(c[0], c[1], c[2])
        print(comm.get_id())
        print(comm_id)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        return render_template('community.html', subs=subs, posts=posts, user=user, comm=comm)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        global mydb
        mydb = reconnect(mydb)
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['firstname'] = account[2]
            session['lastname'] = account[3]
            session['password'] = account[4]
            session['img_link'] = account[5]
            session['bio'] = account[6]
            # Redirect to home page
            cursor.close()
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Pseudo/Mot de passe incorrect !'
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
        global mydb
        mydb = reconnect(mydb)
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Le compte existe déjà !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Le pseudo doit uniquement comporter des chiffres et des lettres !'
        elif not username or not password:
            msg = 'Veuillez remplir le formulaire !'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (NULL, %s, "", "", %s, "https://www.pngkey.com/png/full/204-2049354_ic-account-box-48px-profile-picture-icon-square.png", "")', (username, password,))
            mydb.commit()
            msg = 'Vous vous êtes bien enregistré !'
        cursor.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Veuillez remplir le formulaire !'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/profile', methods=['GET'])
def profile():
    if 'loggedin' in session and 'username' in session:
        user_id = request.args.get('user')
        global mydb
        mydb = reconnect(mydb)
        posts = get_user_posts(user_id, mydb, 0, 25)
        subs = get_all_subs(mydb)
        user = get_user_from_id(user_id, mydb)
        user2 = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'], session['id'])
        return render_template('profile.html', subs=subs, posts=posts, user=user, user2=user2)
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global mydb
    mydb = reconnect(mydb)
    if 'loggedin' in session:
        # Output message if something goes wrong...
        msg = ''
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            img_link = request.form['img_link']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            bio = request.form['bio']
            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
            account = cursor.fetchone()
            cursor.close()
            if account and account[0] != session['id']:
                msg = 'Le pseudo est déjà utilisé'
            else:
                cursor = mydb.cursor()
                cursor.execute('UPDATE user SET username = %s, password = %s, img_link = %s, firstname = %s, lastname = %s, bio = %s WHERE id = %s', (username, password, img_link, firstname, lastname, bio, session['id']))
                mydb.commit()
                session['username'] = username
                session['password'] = password
                session['img_link'] = img_link
                session['firstname'] = firstname
                session['lastname'] = lastname
                session['bio'] = bio
                msg = 'Profil mis à jour!'
                cursor.close()
        # Show the login form with message (if any)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        subs = get_all_subs(mydb)
        return render_template('settings.html', msg=msg, subs=subs, user=user)
    else:
        return redirect(url_for('login'))


@app.route('/amis', methods=['GET', 'POST'])
def amis():
    if 'loggedin' in session:
        global mydb
        mydb = reconnect(mydb)
        # Output message if something goes wrong...
        msg = ''
        msg2=''
        if request.method == 'POST':
            if 'username' in request.form:
                username = request.form['username']
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
                user2_id = cursor.fetchone()[0]
                cursor.close()
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM friend_request WHERE user1_id = %s AND user2_id = %s', (str(session['id']), str(user2_id),))
                fr = cursor.fetchone()
                cursor.close()
                if fr is None and not is_friend(session['id'], str(user2_id)):
                    cursor = mydb.cursor()
                    cursor.execute('INSERT INTO friend_request VALUES (NULL, %s, %s)', (str(session['id']), str(user2_id),))
                    mydb.commit()
                    msg = "Demande d'ami envoyée!"
                else :
                    msg = "Echec lors de l'envoi de la demande d'ami"
            else:
                user_id = request.form['user_id']
                cursor = mydb.cursor()
                cursor.execute('INSERT INTO friendships VALUES (NULL, %s, %s)', (session['id'], user_id,))
                mydb.commit()
                cursor = mydb.cursor()
                cursor.execute('DELETE FROM friend_request WHERE user1_id = %s AND user2_id = %s ', (user_id, session['id'],))
                mydb.commit()
                msg2 = 'Demande acceptée!'
                cursor.close()
        # Show the login form with message (if any)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        subs = get_all_subs(mydb)
        requests = get_friend_requests(session['id'], mydb)
        liste_amis = friends_list(session['id'], mydb)
        suggestions = suggestion_amis(session['id'], mydb)
        return render_template('friend-request.html', msg=msg, msg2=msg2, subs=subs, user=user, requ=requests, amis=liste_amis, sugg=suggestions)
    else:
        return redirect(url_for('login'))


@app.route('/like', methods=['POST'])
def like_post():
    if 'loggedin' in session:
        global mydb
        mydb = reconnect(mydb)
        post_id = request.form['post_id']
        previous_page = request.form['previous_page']
        if not is_post_liked(session['id'], post_id, mydb):
            if is_post_disliked(session['id'], post_id, mydb):
                remove_dislike(session['id'], post_id, mydb)
            add_like(session['id'], post_id, mydb)
        else:
            remove_like(session['id'], post_id, mydb)
        return redirect(previous_page)
    else:
        return redirect(url_for('login'))


@app.route('/dislike', methods=['POST'])
def dislike_post():
    if 'loggedin' in session:
        global mydb
        mydb = reconnect(mydb)
        post_id = request.form['post_id']
        previous_page = request.form['previous_page']
        if not is_post_disliked(session['id'], post_id, mydb):
            if is_post_liked(session['id'], post_id, mydb):
                remove_like(session['id'], post_id, mydb)
            add_dislike(session['id'], post_id, mydb)
        else:
            remove_dislike(session['id'], post_id, mydb)
        return redirect(previous_page)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()