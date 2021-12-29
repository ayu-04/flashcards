from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

#-----------models-----------

class user(db.Model):
	__tablename__='user'
	username=db.Column(db.String,primary_key=True)
	password=db.Column(db.String,unique=True,nullable=False)
class decks(db.Model):
	__tablename__='decks'
	username=db.Column(db.String,db.ForeignKey(user.username),primary_key=True)
	title=db.Column(db.String,primary_key=True)
	rec_score=db.Column(db.Integer)
	date_time=db.Column(db.DateTime)
class cards(db.Model):
	__tablename__='cards'
	username=db.Column(db.String,db.ForeignKey(user.username),primary_key=True)
	title=db.Column(db.String,db.ForeignKey(decks.title),primary_key=True)
	card_no=db.Column(db.Integer,primary_key=True)
	question=db.Column(db.String,nullable=False)
	answer=db.Column(db.String,nullable=False)
