def is_post_liked(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user_like WHERE user_id = ? AND post_id = ?', (user_id, post_id,))
    return cursor.fetchone() is not None


def is_post_disliked(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user_dislike WHERE user_id = ? AND post_id = ?', (user_id, post_id,))
    return cursor.fetchone() is not None


def add_like(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('INSERT INTO user_like VALUES(NULL, ?, ?)', (user_id, post_id,))
    db.commit()
    cursor.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
    db.commit()


def remove_like(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('DELETE FROM user_like WHERE user_id = ? AND post_id = ?', (user_id, post_id,))
    db.commit()
    cursor.execute('UPDATE posts SET likes = likes - 1 WHERE id = ?', (post_id,))
    db.commit()


def add_dislike(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('INSERT INTO user_dislike VALUES(NULL, ?, ?)', (user_id, post_id,))
    db.commit()
    cursor.execute('UPDATE posts SET dislikes = dislikes + 1 WHERE id = ?', (post_id,))
    db.commit()


def remove_dislike(user_id, post_id, db):
    cursor = db.cursor()
    cursor.execute('DELETE FROM user_dislike WHERE user_id = ? AND post_id = ?', (user_id, post_id,))
    db.commit()
    cursor.execute('UPDATE posts SET dislikes = dislikes - 1 WHERE id = ?', (post_id,))
    db.commit()
