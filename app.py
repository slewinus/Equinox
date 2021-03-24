from flask import Flask, render_template
from classes import User, GraphDic, Community

app = Flask(__name__)

comm = []
dev = Community("Developpement Web", "https://www.iconninja.com/files/134/910/544/network-website-web-internet-icon.svg")
games = Community("Jeux vidéos", "https://www.iconninja.com/files/574/642/378/b-controller-game-icon.svg")
parlotte = Community("Parlotte", "https://www.pinclipart.com/picdir/middle/126-1269524_chat-speech-bubbles-symbol-svg-png-icon-simbolo.png")
comm.append(dev)
comm.append(games)
comm.append(parlotte)
elliott = User("Elliott", "purple2003", "https://i.stack.imgur.com/l60Hf.png")


@app.route('/')
def index():
    return render_template('index.html', subs=comm, user=elliott)


if __name__ == '__main__':
    app.run()
