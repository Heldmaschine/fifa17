from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from passlib.hash import sha256_crypt
from app import app,db
from .forms import RegistrationForm

import json
from .models import User, Product, Category, Bill
from .mongo_models import Post, Comment
import datetime

@app.route('/')
def index():
    #Products = Product.query.filter_by(category=1).limit(5)
    #fix
    posts_unsolved = Post.query.filter(Post.category == 0).all()
    posts_solved = Post.query.filter(Post.category == 1).all()
    posts_news = Post.query.filter(Post.category == 2).all()
    return render_template("index.html", #Products=Products,
                           houseplants=Product.query.filter_by(category=2).limit(5),
                           bouquets=Product.query.filter_by(category=3).limit(5), posts_unsolved=posts_unsolved,
                           posts_solved=posts_solved, posts_news=posts_news)

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            name = form.name.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            if User.query.filter_by(username=username).first():
                return render_template('register.html', form=form)
            else:
                db.session.add(User(username, email, name, password))
                db.session.commit()
                #gc.collect() garbage collect
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        return render_template("register.html", form=form)
    except Exception as e:
        return (str(e))

@app.route('/login/', methods=["GET", "POST"])
def login_page():
	error = ''
	if request.method == "POST":
		if User.query.filter_by(username=request.form['username']).first() and \
			sha256_crypt.verify(request.form['password'], User.query.filter_by(
				username=request.form['username']).first().password):
			session['logged_in'] = True
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			error = 'Логин или пароль введен неверно, повторите попытку'
	return render_template("login.html", error=error)

@app.route('/board/<category>', methods=["GET", "POST"])
def board(category = "all"):
    #posts = []
    if category == 'unsolved':
        posts = Post.query.filter(Post.category==0).all()
    elif category =='solved':
        posts = Post.query.filter(Post.category == 1).all()
    elif category == "news":
        posts = Post.query.filter(Post.category==2).all()
    elif category == "all":
        posts = Post.query.all()
    if request.method == 'POST':
        post = Post(title=request.form['title'], text=request.form['question'], author=session['username'], category=0)
        post.save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("board.html", title='Forum', posts=posts)

@app.route('/board/post/<id>', methods=["GET", "POST"])
def post(id):
    post = Post.query.get(str(id))
    comments = Comment.query.filter(Comment.post.mongo_id==post.mongo_id).all()
    print(post.mongo_id)
    #post.remove()
    if request.method == 'POST':
        Comment(text=request.form['comment'], author=session['username'], post=post).save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("post.html", title=post.title, post=post, comments=comments)