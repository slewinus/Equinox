from flask import Flask, render_template
from classes import User, GraphDic, Community, Submission

app = Flask(__name__)

comm = []
posts = []

dev = Community("Developpement Web", "https://www.iconninja.com/files/134/910/544/network-website-web-internet-icon.svg")
games = Community("Jeux vidéos", "https://www.iconninja.com/files/574/642/378/b-controller-game-icon.svg")

comm.append(dev)
comm.append(games)

elliott = User("Elliott", "purple2003", "https://www.pngkey.com/png/full/204-2049354_ic-account-box-48px-profile-picture-icon-square.png")

post1 = Submission(elliott, "Hello World!", "What am I to become?", 2021, 19, 0, dev,
                   "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Robot-icon.svg/1200px-Robot-icon.svg.png")
post2 = Submission(elliott, "Second post!", """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam tristique mauris lacus, nec pulvinar diam mollis quis. In aliquam tellus et nibh mattis, vitae imperdiet sem maximus. Donec tempor tellus tellus, in volutpat libero commodo non. Sed molestie felis eget enim vestibulum, quis pretium mi egestas. Pellentesque ut tempor justo. Nulla dictum arcu vel diam finibus tristique. Nullam tortor nulla, elementum eget consequat vitae, faucibus in nulla. Fusce mattis id dolor vel luctus. Cras et turpis at ex porttitor tincidunt. Mauris ante mi, eleifend mollis diam laoreet, faucibus accumsan dui.

Curabitur sit amet elit consectetur, ultricies eros viverra, tempus eros. Sed efficitur, purus ut porttitor hendrerit, velit ex laoreet lorem, eget posuere purus arcu eu libero. Suspendisse fermentum posuere bibendum. Aliquam porttitor augue dolor, vel finibus neque posuere nec. Etiam egestas enim ligula, in euismod est fermentum ut. Nullam quis nulla risus. In elementum porttitor nunc, vel efficitur nisi. Ut et ante ac lectus fermentum pellentesque in ut turpis. Mauris faucibus dui lectus, nec posuere arcu fringilla nec. Etiam pretium, justo nec molestie ornare, nunc dui finibus urna, eu hendrerit velit nulla at erat. Integer ac nulla mollis, convallis turpis at, porta nibh. Proin mattis arcu non nibh scelerisque eleifend a in eros. Nam in posuere arcu.

Phasellus finibus rutrum lectus quis commodo. Ut vel dignissim nisi. Proin eleifend auctor eros, sagittis rhoncus orci egestas eu. Aenean at augue ipsum. Integer eget faucibus mauris. Fusce a justo a mi blandit pharetra vel hendrerit elit. Sed malesuada sagittis tellus, sed ultrices mi rhoncus sed. Cras eget eros justo. Ut non pretium orci. Donec sed nisl varius, varius velit sit amet, varius nunc. Aenean tristique feugiat tellus at accumsan.

Fusce euismod orci nec lobortis pellentesque. Mauris nec velit urna. Suspendisse potenti. Aenean euismod vulputate dignissim. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In lorem magna, maximus eu lobortis vel, laoreet at mi. Nam et ligula imperdiet, interdum elit ut, varius odio. Nunc accumsan, felis vel consectetur fringilla, dolor libero suscipit nunc, vitae interdum mi massa id nunc.""",
                   150, 12, 1, games)
suggestions = []
posts.append(post1)
posts.append(post2)


@app.route('/')
def index():
    return render_template('index.html', subs=comm, user=elliott, posts=posts, sugg=suggestions)


@app.route('/like_post/', methods=['POST'])
def like_post():
    return render_template('index.html', subs=comm, user=elliott, posts=posts)


if __name__ == '__main__':
    app.run()
