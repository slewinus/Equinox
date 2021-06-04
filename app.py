import os
import re
from datetime import datetime

import sqlite3
from flask import Flask, render_template, redirect, url_for, session, request

from feed import *
from user import *
from subquinox import *
from amis import *
from like import *

app = Flask(__name__)

app.secret_key = os.urandom(12).hex()


@app.route('/')
def home():
    if 'loggedin' in session and 'username' in session:
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        subs = get_all_subs(con)
        posts = get_home_feed(session['id'], con, 0, 10)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'], session['id'])
        return render_template('index.html', subs=subs, posts=posts, user=user)
    return redirect(url_for('login'))


@app.route('/post/', methods=['GET', 'POST'])
def post():
    if 'loggedin' in session and 'username' in session:
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        msg = ''
        if request.method == 'POST' and 'content' in request.form and 'titre' in request.form:
            titre = request.form['titre']
            content = request.form['content']
            comm = request.form['community']
            img = request.form['img']
            now = datetime.now()
            date = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor = con.cursor()
            cursor.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?, 0, 0, ?, ?)', (session['id'], titre, content, img, comm, date,))
            con.commit()
            cursor.close()
            msg = 'Post envoyé!'
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        subs = get_all_subs(con)
        return render_template('post.html', msg=msg, subs=subs, user=user)
    return redirect(url_for('login'))


@app.route('/community')
def community():
    if 'loggedin' in session and 'username' in session:
        comm_id = request.args.get('comm')
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        subs = get_all_subs(con)
        posts = get_sub_content(comm_id, session['id'], con, 0, 20)
        cursor = con.cursor()
        cursor.execute('SELECT c.id, c.name, c.img_link FROM communities AS c WHERE c.id = ?', (comm_id,))
        c = cursor.fetchone()
        cursor.close()
        comm = Subquinox(c[0], c[1], c[2])
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
        # Create variables for easy access
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = con.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password,))
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
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = con.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
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
            cursor.execute('INSERT INTO user VALUES (NULL, ?, "", "", ?, "https://www.pngkey.com/png/full/204-2049354_ic-account-box-48px-profile-picture-icon-square.png", "")', (username, password,))
            con.commit()
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
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        posts = get_user_posts(user_id, con, 0, 25)
        subs = get_all_subs(con)
        user = get_user_from_id(user_id, con)
        user2 = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'], session['id'])
        return render_template('profile.html', subs=subs, posts=posts, user=user, user2=user2)
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
            cursor = con.cursor()
            cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
            account = cursor.fetchone()
            cursor.close()
            if account and account[0] != session['id']:
                msg = 'Le pseudo est déjà utilisé'
            else:
                cursor = con.cursor()
                cursor.execute('UPDATE user SET username = ?, password = ?, img_link = ?, firstname = ?, lastname = ?, bio = ? WHERE id = ?', (username, password, img_link, firstname, lastname, bio, session['id'],))
                con.commit()
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
        subs = get_all_subs(con)
        return render_template('settings.html', msg=msg, subs=subs, user=user)
    else:
        return redirect(url_for('login'))


@app.route('/amis', methods=['GET', 'POST'])
def amis():
    if 'loggedin' in session:
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # Output message if something goes wrong...
        msg = ''
        msg2= ''
        if request.method == 'POST':
            if 'username' in request.form:
                username = request.form['username']
                cursor = con.cursor()
                cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
                user2_id = cursor.fetchone()[0]
                cursor.execute('SELECT * FROM friend_request WHERE user1_id = ? AND user2_id = ?', (str(session['id']), str(user2_id),))
                fr = cursor.fetchone()
                if fr is None and not is_friend(session['id'], str(user2_id)):
                    cursor.execute('INSERT INTO friend_request VALUES (NULL, ?, ?)', (str(session['id']), str(user2_id,)))
                    con.commit()
                    msg = "Demande d'ami envoyée!"
                else :
                    msg = "Echec lors de l'envoi de la demande d'ami"
            else:
                user_id = request.form['user_id']
                cursor = con.cursor()
                cursor.execute('INSERT INTO friendships VALUES (NULL, ?, ?)', (session['id'], user_id,))
                con.commit()
                cursor.execute('DELETE FROM friend_request WHERE user1_id = ? AND user2_id = ? ', (user_id, session['id'],))
                con.commit()
                msg2 = 'Demande acceptée!'
                cursor.close()
        # Show the login form with message (if any)
        user = User(session['username'], session['password'], session['firstname'], session['lastname'], session['img_link'], session['bio'],
                    session['id'])
        subs = get_all_subs(con)
        requests = get_friend_requests(session['id'], con)
        liste_amis = friends_list(session['id'], con)
        suggestions = suggestion_amis(session['id'], con)
        return render_template('friend-request.html', msg=msg, msg2=msg2, subs=subs, user=user, requ=requests, amis=liste_amis, sugg=suggestions)
    else:
        return redirect(url_for('login'))


@app.route('/like', methods=['POST'])
def like_post():
    if 'loggedin' in session:
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        post_id = request.form['post_id']
        previous_page = request.form['previous_page']
        if not is_post_liked(session['id'], post_id, con):
            if is_post_disliked(session['id'], post_id, con):
                remove_dislike(session['id'], post_id, con)
            add_like(session['id'], post_id, con)
        else:
            remove_like(session['id'], post_id, con)
        return redirect(previous_page)
    else:
        return redirect(url_for('login'))


@app.route('/dislike', methods=['POST'])
def dislike_post():
    if 'loggedin' in session:
        con = sqlite3.connect('./equinox.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        post_id = request.form['post_id']
        previous_page = request.form['previous_page']
        if not is_post_disliked(session['id'], post_id, con):
            if is_post_liked(session['id'], post_id, con):
                remove_like(session['id'], post_id, con)
            add_dislike(session['id'], post_id, con)
        else:
            remove_dislike(session['id'], post_id, con)
        return redirect(previous_page)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
