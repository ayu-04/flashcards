from flask import  request
from flask import render_template
from flask import current_app as app
from flask import redirect
from flask import url_for
from models import user,decks,cards,db
from data import Cards
from datetime import datetime
import io 
import csv
#---------------App-------------------
#login
@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')

	if request.method=='POST' and request.form['username']!='' and request.form['password']!='':
		u_name=request.form['username']
		p_word=request.form['password']
		u=user.query.filter_by(username=u_name).first()
		if u==None:
			return inc_pass()
		if u.password==p_word:
			return redirect(url_for('dashboard',u_name=u_name))
		else:
			return redirect('/incorrect_password')
	else:
		return inc_pass()

@app.route('/incorrect_password',methods=['GET'])
def inc_pass():
	return render_template('inc_pass.html')

@app.route('/create_account',methods=['GET','POST'])
def create_acc():
	if request.method=='GET':
		return render_template('create_acc.html')
	if request.method=='POST' and request.form['username']!='' and request.form['password']!='':
		u_name=request.form['username']
		p_word=request.form['password']
		u=user.query.filter_by(username=u_name).first()
		if u!=None:
			return user_exists()
		else:
			u=user(username=u_name,password=p_word)
			db.session.add(u)
			db.session.commit()
			for c in Cards:
				d=decks(username=u_name,title=c,rec_score=None,date_time=None)
				db.session.add(d)
				db.session.commit()
				for j in range(len(Cards[c])):
					x=cards(username=u_name,title=c,card_no=j,question=Cards[c][j][0],answer=Cards[c][j][1])
					db.session.add(x)
					db.session.commit()
			return redirect(url_for('dashboard',u_name=u_name))
	else:
		return redirect('/create_account_incorrect_password')

@app.route('/create_account_incorrect_password',methods=['GET'])
def inc_pass_create_acc():
	return render_template('inc_pass_create_acc.html')
	
@app.route('/user_exists',methods=['GET'])
def user_exists():
	return render_template('user_exists.html')

#dashboard
@app.route('/<string:u_name>/dashboard',methods=['GET'])
def dashboard(u_name):
	u=user.query.filter_by(username=u_name).first()
	user_cards=decks.query.filter_by(username=u.username).all()
	do_it_again=[]
	try_smtg_new=[]
	for i in user_cards:
		if i.date_time!=None:
			do_it_again.append(i)
		else:
			try_smtg_new.append(i)
	do_it_again.sort(reverse=True,key=lambda x:x.date_time)
	return render_template('dashboard.html',do_it_again=do_it_again,try_smtg_new=try_smtg_new,username=u.username)

@app.route('/<string:u_name>/flashcard/<string:t>/0',methods=['GET','POST'])
def flashcard(u_name,t):
	print(datetime.now())
	d_t=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	d_t=datetime.strptime(d_t,'%Y-%m-%d %H:%M:%S')
	d=decks.query.filter_by(username=u_name,title=t).first()
	d.rec_score=0
	db.session.commit()
	d.date_time=d_t
	db.session.commit()
	c=cards.query.filter_by(username=u_name,title=t).all()
	if len(c)>0:
		return card(u_name,t,0)
	else:
		return render_template('no_cards.html',username=u_name)

@app.route('/<string:u_name>/flashcard/<string:t>/<int:i>',methods=['GET','POST'])
def card(u_name,t,i):
	c=cards.query.filter_by(username=u_name,title=t).all()
	d=decks.query.filter_by(username=u_name,title=t).first()
	if len(c)>i:
		if request.method=='GET':
			return render_template('card.html',u_name=d.username,c_no=i,i=c[i],score=d.rec_score)
		if request.method=='POST':
			if request.form['submit']=='Easy':
				d.rec_score+=10
				db.session.commit()
			if request.form['submit']=='Medium':
				d.rec_score+=5
				db.session.commit()
			if request.form['submit']=='Hard':
				d.rec_score+=3
				db.session.commit()
			if request.form['submit']=='Incorrect':
				d.rec_score+=0
				db.session.commit()
			return render_template('card.html',u_name=d.username,c_no=i,i=c[i],score=d.rec_score)
	else:
		return redirect(url_for('gameover',u_name=u_name,t=d.title))

@app.route('/<string:u_name>/gameover/<string:t>',methods=['GET'])
def gameover(u_name,t):
	d=decks.query.filter_by(title=t).first()
	return render_template('gameover.html',d=d)
#create deck
@app.route('/<string:u_name>/create',methods=['GET','POST'])
def create(u_name):
	if request.method=='GET':
		return render_template('deck_create.html',username=u_name)
	if request.method=='POST' and request.form['title']!='' and request.form['no_of_cards']!='':
		t=request.form['title']
		count=request.form['no_of_cards']
		try:
			count=int(count)
		except:
			return render_template('inc_title.html',username=u_name)
		if count<1:
			return render_template('inc_title.html',username=u_name)
		d=decks.query.filter_by(username=u_name,title=t).first()
		if d!=None:
			return redirect(url_for('deck_exists',u_name=u_name))
		else:
			d=decks(username=u_name,title=t,rec_score=None,date_time=None)
			db.session.add(d)
			db.session.commit()
			return redirect(url_for('card_create',u_name=u_name,t=t,card_no=0,count=count))
	else:
		return render_template('inc_title.html',username=u_name)

@app.route('/<string:u_name>/deck_exists',methods=['GET'])
def deck_exists(u_name):
	return render_template('already_exists.html',username=u_name)
#create card
@app.route('/<string:u_name>/card_create/<string:t>/<int:count>/<int:card_no>',methods=['GET','POST'])
def card_create(u_name,t,count,card_no):
	if card_no<count:
		if request.method=='GET':
			return render_template('card_create.html',count=count-card_no-1)
		if request.method=='POST':
			ques=request.form['question']
			ans=request.form['answer']
			c=cards(username=u_name,title=t,card_no=card_no,question=ques,answer=ans)
			db.session.add(c)
			db.session.commit()
			return redirect(url_for('card_create',u_name=u_name,t=t,card_no=card_no+1,count=count))
	else:
		return redirect(url_for('deck_done',u_name=u_name,t=t))

@app.route('/<string:u_name>/deck_done/<string:t>',methods=['GET'])
def deck_done(u_name,t):
	return render_template('deck_done.html',username=u_name)

#edit deck
@app.route('/<string:u_name>/edit',methods=['GET'])
def edit(u_name):
	user_cards=decks.query.filter_by(username=u_name).all()
	if request.method=='GET':
		return render_template('main_deck_edit.html',cards=user_cards)

@app.route('/<string:u_name>/deck_edit/<string:t>',methods=['GET'])
def deck_edit(u_name,t):
	c=cards.query.filter_by(username=u_name,title=t).all()
	return render_template('deck_edit.html',c=c)

#edit deck edit card
@app.route('/<string:u_name>/card_edit/<string:t>/<int:c_no>',methods=['GET','POST'])
def card_edit(u_name,t,c_no):
	c=cards.query.filter_by(username=u_name,title=t,card_no=c_no).first()
	if request.method=='GET':
		return render_template('card_edit.html',c=c)
	if request.method=='POST':
		ques=request.form['question']
		ans=request.form['answer']
		c.question=ques
		db.session.commit()
		c.answer=ans
		db.session.commit()
		return redirect(url_for('deck_edit',u_name=u_name,t=t))

#edit deck delete card		
@app.route('/<string:u_name>/card_delete/<string:t>/<int:c_no>',methods=['GET','POST'])
def card_delete(u_name,t,c_no):
	c=cards.query.filter_by(username=u_name,title=t,card_no=c_no).first()
	db.session.delete(c)
	db.session.commit()
	return redirect(url_for('deck_edit',u_name=u_name,t=t)) 

#edit deck add card
@app.route('/<string:u_name>/edit_card_create/<string:t>',methods=['GET','POST'])
def edit_card_create(u_name,t):
	c=cards.query.filter_by(username=u_name,title=t).all()
	if request.method=='GET':
		return render_template('edit_card_create.html')
	if request.method=='POST':
		ques=request.form['question']
		ans=request.form['answer']
		last=c[-1].card_no
		x=cards(username=u_name,title=t,card_no=last+1,question=ques,answer=ans)
		db.session.add(x)
		db.session.commit()
		return redirect(url_for('deck_edit',u_name=u_name,t=t))

#delete decks
@app.route('/<string:u_name>/dele',methods=['GET','POST'])
def dele(u_name):
	d=decks.query.filter_by(username=u_name).all()
	if request.method=='GET':
		return render_template('deck_delete.html',d=d)
	if request.method=='POST':
		titles=request.form.getlist('titles')
		for i in titles:
			c=cards.query.filter_by(username=u_name,title=i).all()
			for j in c:
				db.session.delete(j)
				db.session.commit()
			d=decks.query.filter_by(username=u_name,title=i).first()
			db.session.delete(d)
			db.session.commit()
		return redirect(url_for('dashboard',u_name=u_name))

#import deck
@app.route('/<string:u_name>/import',methods=['GET','POST'])
def imp(u_name):
	if request.method=='GET':
		return render_template('deck_import.html')
	if request.method=='POST':
		f = request.files['data_file']
		t=request.form['title']
		d=decks.query.filter_by(username=u_name,title=t).first()
		if d!=None:
			return redirect(url_for('deck_exists',u_name=u_name))
		if not f:
			return "No file"
		stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
		csv_input = csv.reader(stream)
		d=decks(username=u_name,title=t,rec_score=None,date_time=None)
		db.session.add(d)
		db.session.commit()
		i=0
		for row in csv_input:
			c=cards(username=u_name,title=t,card_no=i,question=row[0],answer=row[1])
			db.session.add(c)
			db.session.commit()
			i+=1
		return redirect(url_for('deck_done',u_name=u_name,t=t))

#export deck
@app.route('/<string:u_name>/export',methods=['GET','POST'])
def exp(u_name):
	d=decks.query.filter_by(username=u_name).all()
	if request.method=='GET':
		return render_template('deck_export.html',d=d)
	if request.method=='POST':
		t=request.form['title']
		c=cards.query.filter_by(username=u_name,title=t).all()
		x=[]
		for i in c:
			x.append([i.question,i.answer])
		t_file=t+'.csv'
		with open('static/'+t_file, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(x)
		return render_template('download.html',file=t_file,username=u_name)

