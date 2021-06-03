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

