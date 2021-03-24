class User:
    def __init__(self, n, p):
        self.username = n
        self.password = p
        self.bio = str()
        self.age = None

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username

    def get_bio(self):
        return self.bio


class Community:
    def __init__(self, n, i):
        self.name = n
        self.icon_link = i

    def get_name(self):
        return self.name

    def get_icon_link(self):
        return self.icon_link


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