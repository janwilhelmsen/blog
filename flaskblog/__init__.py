from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship,DeclarativeBase
from flaskblog.forms import RegisterForm, CreatePostForm, LoginForm, CommentForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
#from flaskblog.models import User,Comment,BlogPost
import os

class Base(DeclarativeBase):
    pass    

db=SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get('DB_URI_BLOG')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY_FLASK')


ckeditor = CKEditor(app)
Bootstrap5(app)

# #gravatar
# gravatar=Gravatar(app,
#                   size=100,
#                   rating='g',
#                   default='retro',
#                   force_default=False,
#                   force_lower=False,
#                   use_ssl=False,
#                   base_url=None)

db.init_app(app)

# #Create the login manager from Flask Login
# login_manager=LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return db.get_or_404(User,ident=user_id)


with app.app_context():
    print ("create DB")
    db.create_all()

from flaskblog import routes