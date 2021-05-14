class User:
    def __init__(self, n, p, f, last, pp, b):
        self.username = n
        self.password = p
        self.firstname = f
        self.lastname = last
        self.bio = b
        self.pic_link = pp

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


class Community:
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


class Submission:
    def __init__(self, u, t, txt, up, down, id, c=None, im=None):
        self.user = u
        self.title = t
        self.text = txt
        self.likes = up
        self.dislikes = down
        self.id = id
        self.community = c
        self.image_link = im

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