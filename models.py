from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    url = db.Column(db.String(500), nullable = True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# class Tag(db.Model):
#     __tablename__ = 'tags'

#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     name = db.Column(db.String(30), nullable = False, unique = True)
#     post_tags = db.relationship('Post_Tags', backref='tag', cascade="all, delete-orphan")