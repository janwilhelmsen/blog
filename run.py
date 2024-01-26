from flaskblog import app

# from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase
# from datetime import date 
# from flask import Flask, abort, render_template, redirect, url_for, flash,request
# from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
# from flask_grava  tar import Gravatar
# from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user,login_required
# from flask_sqlalchemy import SQLAlchemy
# # from functools import wraps
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import relationship,DeclarativeBase
# from flaskblog.forms import RegisterForm, CreatePostForm, LoginForm, CommentForm
# import os
# import smtplib


# class Base(DeclarativeBase):
#     pass    

# db=SQLAlchemy(model_class=Base)
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get('DB_URI_BLOG')
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY_FLASK')


# ckeditor = CKEditor(app)
# Bootstrap5(app)




# class User(UserMixin, db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     name = db.Column(db.String(100))
    
#     #This will act like a List of BlogPost objects attached to each User. 
#     #The "author" refers to the author property in the BlogPost class.
#     posts = relationship("BlogPost", back_populates="author")
#     comments = relationship("Comment", back_populates="comment_author")

#     def __repr__(self):
#         return f"User('{self.name})', '{self.email}')"
    
# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
    
#     #Create Foreign Key, "users.id" the users refers to the tablename of User.
#     author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
#     author = relationship("User", back_populates="posts")
   
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#     comments = relationship("Comment",back_populates="parent_post")

    
#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date}')"


# class Comment(db.Model):
#     __tablename__ = "comments"
#     id=db.Column(db.Integer, primary_key=True)
#     author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     comment_author = relationship("User",back_populates="comments")

#     post_id=db.Column(db.Integer,db.ForeignKey("blog_posts.id"))
#     parent_post = relationship("BlogPost",back_populates="comments")
#     text = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"User ('{self.comment_author}','{self.text}')"
    




# with app.app_context():
#     db.create_all()

# def admin_only(func):
#     @wraps(func)
#     def decorated_function(*args,**kwargs):
#         if current_user.id != 1:
#             return abort(403)
#         return func(*args,**kwargs)
#     return decorated_function


# def check_if_user(email):
#     result=db.session.execute(db.select(User).where(User.email==email))
#     user=result.scalar()
#     return user




# @app.route('/')
# def get_all_posts():
#     result = db.session.execute(db.select(BlogPost))
#     posts = result.scalars().all()
#     print (posts)
#     return render_template("index.html",all_posts=posts)

# @app.route('/new-post',methods=['POST','GET'])
# @admin_only
# def add_new_post():
#     create_post_form=CreatePostForm()
#     if create_post_form.validate_on_submit():
#         new_post=BlogPost(
#             title=create_post_form.title.data,
#             subtitle=create_post_form.subtitle.data,
#             body=create_post_form.body.data,
#             img_url=create_post_form.img_url.data,
#             author=current_user,
#             date=date.today().strftime("%B %d, %Y")
#         )
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for('get_all_posts'))
#     return render_template('make-post.html',form=create_post_form)

# @app.route('/login',methods=['POST','GET'])
# def login():
#     login_form=LoginForm()
#     if login_form.validate_on_submit():
#         print ("Form validated")
#         _email=login_form.email.data
#         _password=login_form.password.data
#         result=db.session.execute(db.select(User).where(User.email==_email))
#         print (result)
#         user=result.scalar()
#         print (user)
#         if not user:
#             print ("incorrect username")
#         else:
#             if not check_password_hash(user.password,_password):
#                 print ("incorrect password")
#             else:
#                 print ("Sucessfull login")
#                 login_user(user)
#                 return redirect ((url_for('get_all_posts')))

#     return render_template('login.html',form=login_form)

# @app.route('/register',methods=['POST','GET'])
# def register():
#     reg_form=RegisterForm()
#     if reg_form.validate_on_submit():
#         _email=reg_form.email.data
#         _password=reg_form.password.data
#         print ("Form validated")    
#         if not check_if_user(_email):
#             password=generate_password_hash(_password,method='pbkdf2:sha256:600000',salt_length=8)
#             print (password)
#             new_user=User(
#                 name=reg_form.name.data,
#                 email=reg_form.email.data,
#                 password=password
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             flash(f"{reg_form.name.data} is registered successfully",category='info')
#             login_user(new_user)
#             return redirect("/")
#         else:
#             flash("The email address is already registered",category='info')
#             return redirect(url_for('login'))
#     else:
#         print ("No form, lets send empty page")
#         return render_template("register.html",form=reg_form)

    

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('get_all_posts'))

# @app.route('/about')
# def about():
#     return render_template('about.html')

# # @app.route('/contact')
# # def contact():
# #     return render_template('contact.html')

# @app.route('/post/<int:post_id>',methods=['POST','GET'])
# def show_post(post_id):
#     requested_post=db.get_or_404(BlogPost,post_id)
#     comment_form=CommentForm()
#     if comment_form.validate_on_submit():
#         if not current_user.is_authenticated:
#             flash("You need to login or register to comment.")
#             return redirect(url_for("login"))
#         new_comment=Comment(
#             text = comment_form.comment_text.data,
#             comment_author = current_user,
#             parent_post = requested_post
#         )
#         db.session.add(new_comment)
#         db.session.commit()
    
#     return render_template('post.html',post=requested_post,current_user=current_user,form=comment_form)

# @app.route('/delete/<int:post_id>')
# @admin_only
# def delete_post(post_id):
#     post_to_delete=db.get_or_404(BlogPost,post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('get_all_posts'))

# @app.route('/edit-post/<int:post_id>',methods=['POST','GET'])
# @admin_only
# def edit_post(post_id):
#     selected_post=db.get_or_404(BlogPost,post_id)
#     edit_form=CreatePostForm(
#         title=selected_post.title,
#         subtitle=selected_post.subtitle,
#         img_url=selected_post.img_url,
#         author=selected_post.author,
#         body=selected_post.body
#     )

#     if edit_form.validate_on_submit():
#         selected_post.title = edit_form.title.data
#         selected_post.subtitle = edit_form.subtitle.data
#         selected_post.img_url = edit_form.img_url.data
#         selected_post.author = current_user
#         selected_post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for('show_post',post_id=selected_post.id))
#     return render_template('make-post.html',form=edit_form, is_edit=True)
    



# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         data = request.form
#         send_email(data["name"], data["email"], data["phone"], data["message"])
#         return render_template("contact.html", msg_sent=True)
#     return render_template("contact.html", msg_sent=False)







if __name__ == "__main__":
    app.run(debug=True)
