from flask import Flask, request, session, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def to_users():
    """ Redirects to Show All Users """
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """ Shows All Users """
    users = User.query.all()
    return render_template('show_users.html', users=users)


@app.route('/users/new')
def show_form():
    """ Displays New User Form  """
    return render_template('add_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """ Adds New User to db """
    firstName = request.form['first-name']
    lastName = request.form['last-name']
    url = request.form['url']

    new_user = User(first_name=firstName,last_name=lastName,url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:uid>')
def show_user(uid):
    """ Displays User via User ID set in db """
    user = User.query.get(uid)
    posts = user.posts
    return render_template('show_user.html', user=user, uid=uid, posts=posts)

@app.route('/users/<int:uid>/edit')
def edit_user(uid):
    """ Displays Edit User Form """
    user = User.query.get(uid)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:uid>/edit', methods=['POST'])
def edit_user_post(uid):
    """ Edits and saves an individual user """
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
    """ Deletes User """
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:uid>/posts/new')
def get_post_form(uid):
    """ Shows form for new post """
    user = User.query.get(uid)
    return render_template('new_post.html', user=user, uid=uid)

@app.route('/users/<int:uid>/posts/new', methods=['POST'])
def add_post(uid):
    """ Adds a new post to the user's detail page """
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(uid)
    
    new_user = Post(title=title,content=content, user=user)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{uid}')

@app.route('/posts/<int:pid>')
def show_post(pid):
    """ Displays Post Title, Content, and User that Posted """
    post = Post.query.get(pid)
    return render_template('show_post.html',post=post)

@app.route('/posts/<int:pid>/edit')
def show_post_edit_form(pid):
    """ Displays form to edit a post """
    post = Post.query.get(pid)
    user = post.user
    return render_template('edit_post_form.html',post=post,user=user)

@app.route('/posts/<int:pid>/edit', methods=['POST'])
def save_post_edit(pid):
    post = Post.query.get(pid)
    title = request.form['title']
    content= request.form['content']
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{pid}')

@app.route('/posts/<int:pid>/delete')
def delete_post(pid):
    """ Deletes User """
    post = Post.query.get(pid)
    user = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user}')

@app.route('/tags')
def show_all_tags():
    return render_template('show_tags.html')

@app.route('/tags/<int:id>')
def show_tag():
    return render_template('show_tag.html')

@app.route('/tags/new')
def show_create_tag_form():
    return render_template('create_tag_form.html')



