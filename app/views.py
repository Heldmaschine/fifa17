from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from passlib.hash import sha256_crypt
from app import app, db
from .forms import RegistrationForm

import json
from .models import User
from .mongo_models import Post, Comment
import datetime


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            fname = form.fname.data
            lname = form.lname.data
            phone = form.phone.data
            university = form.university.data
            paycheck = form.paycheck.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            if User.query.filter_by(username=username).first():
                return render_template('register.html', form=form)
            else:
                db.session.add(User(username, email, password, fname, lname, phone, university, paycheck))
                db.session.commit()
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
            error = 'Wrong Username or password'
    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    resp = app.make_response(redirect('/'))
    resp.set_cookie('item', expires=0)
    session.pop('logged_in', None)
    return resp


@app.route('/board/')
@app.route('/board')
def board_redirect():
    resp = app.make_response(redirect('board/all'))
    return resp


@app.route('/board/<category>', methods=["GET", "POST"])
def board(category='all'):
    if category == 'unsolved':
        posts = Post.query.filter(Post.category == 0).all()
    elif category == 'solved':
        posts = Post.query.filter(Post.category == 1).all()
    elif category == 'news':
        posts = Post.query.filter(Post.category == 2).all()
    elif category == 'all':
        posts = Post.query.all()
    if request.method == 'POST':
        post = Post(title=request.form['title'], text=request.form[
                    'question'], author=session['username'], category=0)
        post.save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("board.html", title='Forum', posts=posts)


@app.route('/board/post/<id>', methods=["GET", "POST"])
def post(id):
    post = Post.query.get(str(id))
    comments = Comment.query.filter(
        Comment.post.mongo_id == post.mongo_id).all()
    if request.method == 'POST':
        Comment(text=request.form['comment'], author=session[
                'username'], post=post).save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("post.html", title=post.title, post=post, comments=comments)


@app.route('/account/')
def user_page():
    user_data = User.query.with_entities(User.name, User.email,
                                         User.username).filter_by(username=session['username']).first()
    user_posts = Post.query.filter(Post.author == session['username']).all()
    user_comments = Comment.query.filter(
        Comment.author == session['username']).all()
    return render_template("user.html", title=user_data[2], user_data=user_data,
                           posts=user_posts, comments=user_comments)


@app.route('/history')
def history():
    return render_template("history.html", title='And there were History')


@app.route('/comingsoon')
def coming_soon():
    return render_template("coming_soon.html", title='Coming soon!')