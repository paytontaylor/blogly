from flask import Flask, request, session, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def to_users():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    users = User.query.all()
    return render_template('show_users.html', users=users)


@app.route('/users/new')
def show_form():
    return render_template('add_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    firstName = request.form['first-name']
    lastName = request.form['last-name']
    url = request.form['url']

    new_user = User(first_name=firstName,last_name=lastName,url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:uid>')
def show_user(uid):
    user = User.query.get(uid)
    return render_template('show_user.html', user=user, uid=uid)

@app.route('/users/<int:uid>/edit')
def edit_user(uid):
    user = User.query.get(uid)
    return render_template('edit_user_form.html', user=user, uid=uid)

@app.route('/users/<int:uid>/edit', methods=['POST'])
def edit_user_post(uid):
    user = User.query.get(uid)
    firstName = request.form['first-name']
    lastName = request.form['last-name']
    url = request.form['url']
    user.first_name = firstName
    user.last_name = lastName
    user.url = url
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:uid>/delete')
def delete_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')