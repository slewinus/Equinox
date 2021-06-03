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
    from submission import Submission
    from subquinox import Subquinox
    comms = [Subquinox(c[0], c[1], c[2]) for c in comms]
    posts = [Submission(User(p[10], p[11], p[12], p[13], p[14], p[15], p[9]), p[0], p[2], p[3], p[4] if p[4] != '' else None, p[5], p[6], comms[p[7]], p[8]) for p in result]
    posts.sort()
    posts.reverse()
    return posts[first_post:last_post]
