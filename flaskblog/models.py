from sqlalchemy.orm import relationship,DeclarativeBase
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flaskblog import db 

#Create models
print ("create models")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    
    #This will act like a List of BlogPost objects attached to each User. 
    #The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

    def __repr__(self):
        return f"User('{self.name})', '{self.email}')"
    
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="posts")
   
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment",back_populates="parent_post")

    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


class Comment(db.Model):
    __tablename__ = "comments"
    id=db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User",back_populates="comments")

    post_id=db.Column(db.Integer,db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost",back_populates="comments")
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User ('{self.comment_author}','{self.text}')"
    



