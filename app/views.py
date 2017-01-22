from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from passlib.hash import sha256_crypt
from app import app, db
from .forms import RegistrationForm

import json
from .models import User, Product, Category, Bill
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
            name = form.name.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            if User.query.filter_by(username=username).first():
                return render_template('register.html', form=form)
            else:
                db.session.add(User(username, email, name, password))
                db.session.commit()
                # gc.collect() garbage collect
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
    #posts = []
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
    # print(post.mongo_id)
    # post.remove()
    if request.method == 'POST':
        Comment(text=request.form['comment'], author=session[
                'username'], post=post).save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("post.html", title=post.title, post=post, comments=comments)


@app.route('/account/')
def user_page():
    user_data = User.query.with_entities(User.name, User.email,
                                         User.username).filter_by(username=session['username']).first()
    #user_bills = db.session.query(Bill, Product).with_entities(Bill.amount, Bill.delivery_place, Product.id,
    #                                                           Bill.delivery_date).filter_by(
    #    username=session['username']).filter_by(id=Product.id).all()
    user_posts = Post.query.filter(Post.author == session['username']).all()
    #print(user_posts)
    user_comments = Comment.query.filter(
        Comment.author == session['username']).all()
    # print(user_comments)
    return render_template("user.html", title=user_data[2], user_data=user_data,
                           #user_bills=user_bills,
                           posts=user_posts, comments=user_comments)


@app.route('/history')
def history():
    return render_template("history.html", title='And there were History')


@app.route('/comingsoon')
def coming_soon():
    return render_template("coming_soon.html", title='Coming soon!')
'''
@app.route('/<category>/', methods=["GET", "POST"])
def Products(category):
    title = Category.query.filter_by(url=category).first()
    if title == None:
        return redirect(url_for('index'))
    minprice = 0
    maxprice = 150
    orderby = 'asc'
    Products_query = Product.query.with_entities(Product.name, Product.price, Product.url).filter_by(
        category=Category.query.filter_by(url=category).first().id).order_by(Product.price.asc()).all()
    if request.method == 'POST':
        minprice = request.form['minprice']
        maxprice = request.form['maxprice']
        orderby = request.form['ord']
        if orderby == 'desc':
            Products_query = Product.query.with_entities(Product.name, Product.price, Product.url).filter_by(
                category=Category.query.filter_by(url=category).first().id).filter(
                Product.price >= minprice, Product.price <= maxprice).order_by(Product.price.desc()).all()
        else:
            Products_query = Product.query.with_entities(Product.name, Product.price, Product.url).filter_by(
                category=Category.query.filter_by(url=category).first().id).filter(Product.price >= minprice,
                                                                                   Product.price <= maxprice).order_by(
                Product.price.asc()).all()
    return render_template("Products.html", title=title.name, Products=Products_query, minprice=minprice, maxprice=maxprice,
                           orderby=orderby)


@app.route('/<category>/item/<Product>', methods=["GET", "POST"])
def Product_view(category, Product):
    Product = Product.query.with_entities(Product.name, Product.price, Product.url, Product.id).filter_by(
        url=Product).first()
    if request.method == 'POST':
        Product_dict = {
            'id': Product[3],
            'amount': request.form['amount']
        }
        if request.cookies.get('list_to_buy') == None:
            resp = app.make_response(redirect('/cart/'))
            resp.set_cookie('list_to_buy', value=json.dumps([Product_dict]))
            return resp
        else:
            Product_list = json.loads(request.cookies.get('list_to_buy'))
            Product_list.append(Product_dict)
            resp = app.make_response(redirect('/cart/'))
            resp.set_cookie('list_to_buy', value=json.dumps(Product_list))
            return resp
    return render_template("page.html", title=Product[0], Product=Product)
'''
