class Subquinox:
    def __init__(self, id, n, i):
        self.id = id
        self.name = n
        self.icon_link = i

    def get_name(self):
        return self.name

    def get_icon_link(self):
        return self.icon_link

    def get_id(self):
        return self.id


def get_all_subs(db):
    cursor = db.cursor()
    cursor.execute('SELECT c.id, c.name, c.img_link FROM communities AS c')
    communities = cursor.fetchall()
    return [Subquinox(s[0], s[1], s[2]) for s in communities]


def get_sub_content(comm_id, db, first_post, last_post):
    cursor = db.cursor()
    cursor.execute('SELECT posts.*, u.* FROM posts JOIN user AS u ON u.id = posts.user_id WHERE comm_id = %s', (comm_id,))
    result = cursor.fetchall()
    cursor.execute('SELECT * FROM communities ORDER BY id')
    comms = cursor.fetchall()
    from user import User
    from submission import Submission
    comms = [Subquinox(c[0], c[1], c[2]) for c in comms]
    posts = [Submission(User(p[10], p[11], p[12], p[13], p[14], p[15], p[9]), p[0], p[2], p[3], p[4] if p[4] != '' else None, p[5], p[6], comms[p[7]], p[8]) for p in result]
    posts.sort()
    posts.reverse()
    return posts[first_post:last_post]