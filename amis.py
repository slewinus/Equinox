class GraphDic:
    """ Un graphe comme dictionnaire d'adjacence"""

    def __init__(self):
        self.dico = dict()

    def ajouter_sommet(self, s):
        self.dico[s] = []

    def ajouter_arc(self, s1, s2):
        self.dico[s1].append(s2)

    def supprimer_arc(self, s1, s2):
        self.dico[s1].remove(s2)

    def arc(self, s1, s2):
        return s2 in self.dico[str(s1)]

    def sommets(self):
        return self.dico.keys()

    def voisins(self, s):
        return self.dico[s]


class File:
    def __init__(self):
        self.v = []

    def enfiler(self, x):
        self.v.insert(0, x)

    def defiler(self):
        return self.v.pop()

    def est_vide(self):
        return len(self.v) == 0


def get_friend_requests(user_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT f.id, u.username, u.id, u.img_link FROM friend_request AS f JOIN user AS u ON u.id = f.user1_id WHERE f.user2_id = ?', (user_id,))
    return cursor.fetchall()


def friends_list(user_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT f.user2_id, u.username, u.img_link FROM friendships AS f JOIN user AS u ON u.id = f.user2_id WHERE f.user1_id = ?', (user_id,))
    liste_amis = cursor.fetchall()
    cursor = db.cursor()
    cursor.execute('SELECT f.user1_id, u.username, u.img_link FROM friendships AS f JOIN user AS u ON u.id = f.user1_id WHERE f.user2_id = ?', (user_id,))
    liste_amis += cursor.fetchall()
    return liste_amis


def is_friend(user1_id, user2_id, db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM friendships WHERE user1_id = ? AND user2_id = ?', (user1_id, user2_id,))
    fr1 = cursor.fetchone()
    cursor.execute('SELECT * FROM friendships WHERE user1_id = ? AND user2_id = ?', (user2_id, user1_id,))
    fr2 = cursor.fetchone()
    cursor.close()
    return fr1 is not None or fr2 is not None


def creation_graphe(db):
    graphe = GraphDic()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM friendships')
    friendships = cursor.fetchall()
    for user in users:
        graphe.ajouter_sommet(user[0])
    for friendship in friendships:
        graphe.ajouter_arc(friendship[1], friendship[2])
        graphe.ajouter_arc(friendship[2], friendship[1])
    return graphe


def parcours_ch(graphe, user_id):
    vus = {}
    file = File()
    file.enfiler((user_id, None))
    while not file.est_vide():
        n_somm, a_somm = file.defiler()
        if n_somm not in vus:
            vus[n_somm] = a_somm
            for v in graphe.voisins(n_somm):
                file.enfiler((v, n_somm))
    return vus


def distance(parcours, v):
    chemin = []
    sommets = parcours
    if v not in sommets:
        return None
    s = v
    while s is not None:
        chemin.append(s)
        s = sommets[s]
    chemin.reverse()
    return len(chemin) - 1, chemin[1]


def suggestion_amis(user_id, db):
    cursor = db.cursor()
    graphe = creation_graphe(db)
    suggest = []
    parcours = parcours_ch(graphe, user_id)
    cursor.execute('SELECT user2_id FROM friend_request WHERE user1_id = ?', (user_id,))
    requests = [a[0] for a in cursor.fetchall()]
    for sommet in graphe.sommets():
        if sommet != user_id and sommet not in graphe.voisins(user_id) and sommet not in requests:
            cursor.execute('SELECT username, img_link FROM user WHERE id = ?', (sommet,))
            answer = cursor.fetchone()
            dist = distance(parcours, sommet)
            if dist is not None:
                suggest.append((dist[0], answer[0], answer[1], dist[1], sommet))
            else:
                suggest.append((16, answer[0], answer[1], "personne", sommet))
    cursor.close()
    return sorted(suggest)
