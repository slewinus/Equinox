from like import *

class User:
    def __init__(self, n, p, f, last, pp, b, i):
        self.username = n
        self.password = p
        self.firstname = f
        self.lastname = last
        self.bio = b
        self.pic_link = pp
        self.id = i

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username

    def get_bio(self):
        return self.bio

    def get_picture_link(self):
        return self.pic_link

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_id(self):
        return self.id


def get_user_posts(user_id, db, first_post, last_post):
    from subquinox import Subquinox
    from feed import Submission
    cursor = db.cursor()
    cursor.execute('SELECT posts.*, u.* FROM posts JOIN user AS u ON u.id = posts.user_id WHERE u.id = %s', (user_id,))
    result = cursor.fetchall()
    cursor.execute('SELECT * FROM communities ORDER BY id')
    comms = cursor.fetchall()
    comms = [Subquinox(c[0], c[1], c[2]) for c in comms]
    result = [Submission(User(p[10], p[11], p[12], p[13], p[14], p[15], p[9]), p[0], p[2], p[3], p[4] if p[4] != '' else None, p[5], p[6], comms[p[7] - 1], p[8]) for p in result]
    posts = []
    result.sort()
    result.reverse()
    for post in result[first_post:last_post]:
        if is_post_liked(user_id, post.get_id(), db):
            posts.append((post, 'liked'))
        elif is_post_disliked(user_id, post.get_id(), db):
            posts.append((post, 'disliked'))
        else:
            posts.append((post, None))
    return posts


def get_user_from_id(user_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT username, firstname, lastname, img_link, bio FROM user WHERE id = %s', (user_id,))
    result = cursor.fetchone()
    return User(result[0], "", result[1], result[2], result[3], result[4], user_id)