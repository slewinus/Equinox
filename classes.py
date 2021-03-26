class User:
    def __init__(self, n, p, pp):
        self.username = n
        self.password = p
        self.bio = str()
        self.pic_link = pp
        self.age = None

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username

    def get_bio(self):
        return self.bio

    def get_picture_link(self):
        return self.pic_link


class Community:
    def __init__(self, n, i):
        self.name = n
        self.icon_link = i

    def get_name(self):
        return self.name

    def get_icon_link(self):
        return self.icon_link


class Submission:
    def __init__(self, u, t, txt, c=None, im=None):
        self.user = u
        self.title = t
        self.text = txt
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

    def has_image(self):
        return self.image_link is not None

    def get_image(self):
        return self.image_link

    def get_author(self):
        return self.user.get_username()


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