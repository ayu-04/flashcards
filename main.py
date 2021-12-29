from flask import Flask
from flask_restful import Api
from models import db,user,cards,decks

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.sqlite3'
db.init_app(app)
app.app_context().push()
api=Api(app)
u=user.query.all()
for i in u:
    db.session.delete(i)
    db.session.commit()
d=decks.query.all()
for i in d:
    db.session.delete(i)
    db.session.commit()
c=cards.query.all()
for i in c:
    db.session.delete(i)
    db.session.commit()
from controllers import *

from api import DeckAPI,CardAPI,ScoreAPI

api.add_resource(DeckAPI,"/api/<string:username>/<string:password>/deck/<string:title>","/api/<string:username>/<string:password>/deck")
api.add_resource(CardAPI,"/api/<string:username>/<string:password>/card/<string:title>","/api/<string:username>/<string:password>/card/<string:title>/<string:question>")
api.add_resource(ScoreAPI,"/api/<string:username>/<string:password>/score/<string:title>")

app.run(host='0.0.0.0')