from like import *


class Submission:
    def __init__(self, u, p_id, t, txt, im, up, down, c, d):
        self.user = u
        self.title = t
        self.text = txt
        self.likes = up
        self.dislikes = down
        self.id = p_id
        self.community = c
        self.image_link = im
        self.date = d

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def get_user(self):
        return self.user

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def get_community(self):
        return self.community

    def has_community(self):
        return self.community is not None

    def has_image(self):
        return self.image_link is not None

    def get_image(self):
        return self.image_link

    def get_author(self):
        return self.user.get_username()

    def get_likes(self):
        return self.likes

    def get_dislikes(self):
        return self.dislikes

    def like(self):
        self.likes += 1

    def dislike(self):
        self.dislikes += 1

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date.strftime("%d/%m/%Y, %H:%M")


def get_home_feed(user_id, db, first_post, last_post):
    cursor = db.cursor()
    cursor.execute('SELECT posts.*, u.* FROM posts JOIN friendships AS f ON posts.user_id = f.user1_id JOIN user AS u ON u.id = posts.user_id WHERE f.user2_id = %s', (user_id,))
    result = cursor.fetchall()
    cursor.execute('SELECT posts.*, u.* FROM posts JOIN friendships AS f ON posts.user_id = f.user2_id JOIN user AS u on u.id = posts.user_id WHERE f.user1_id = %s', (user_id,))
    result += cursor.fetchall()
    cursor.execute('SELECT posts.*, u.* FROM posts JOIN user AS u ON u.id = user_id WHERE user_id = %s', (user_id,))
    result += cursor.fetchall()
    cursor.execute('SELECT * FROM communities ORDER BY id')
    comms = cursor.fetchall()
    from user import User
    from subquinox import Subquinox
    comms = [Subquinox(c[0], c[1], c[2]) for c in comms]
    result = [Submission(User(p[10], p[11], p[12], p[13], p[14], p[15], p[9]), p[0], p[2], p[3], p[4] if p[4] != '' else None, p[5], p[6], comms[p[7]-1], p[8]) for p in result]
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
