from datetime import date
from flask import abort, render_template, redirect, url_for, flash,request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user,login_required
from flaskblog.forms import RegisterForm,LoginForm,CreatePostForm,CommentForm
from flaskblog import app
from flaskblog import db
from flaskblog.models import BlogPost,User,Comment

#Create the login manager from Flask Login
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,ident=user_id)


#gravatar
gravatar=Gravatar(app,
                  size=100,
                  rating='g',
                  default='retro',
                  force_default=False,
                  force_lower=False,
                  use_ssl=False,
                  base_url=None)







def admin_only(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if current_user.id != 1:
            return abort(403)
        return func(*args,**kwargs)
    return decorated_function


def check_if_user(email):
    result=db.session.execute(db.select(User).where(User.email==email))
    user=result.scalar()
    return user




@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    print (posts)
    print ("we should return index.html")
    return render_template("index.html",all_posts=posts)

@app.route('/new-post',methods=['POST','GET'])
@admin_only
def add_new_post():
    create_post_form=CreatePostForm()
    if create_post_form.validate_on_submit():
        new_post=BlogPost(
            title=create_post_form.title.data,
            subtitle=create_post_form.subtitle.data,
            body=create_post_form.body.data,
            img_url=create_post_form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html',form=create_post_form)

@app.route('/login',methods=['POST','GET'])
def login():
    login_form=LoginForm()
    if login_form.validate_on_submit():
        print ("Form validated")
        _email=login_form.email.data
        _password=login_form.password.data
        result=db.session.execute(db.select(User).where(User.email==_email))
        print (result)
        user=result.scalar()
        print (user)
        if not user:
            print ("incorrect username")
        else:
            if not check_password_hash(user.password,_password):
                print ("incorrect password")
            else:
                print ("Sucessfull login")
                login_user(user)
                return redirect ((url_for('get_all_posts')))

    return render_template('login.html',form=login_form)

@app.route('/register',methods=['POST','GET'])
def register():
    reg_form=RegisterForm()
    if reg_form.validate_on_submit():
        _email=reg_form.email.data
        _password=reg_form.password.data
        print ("Form validated")    
        if not check_if_user(_email):
            password=generate_password_hash(_password,method='pbkdf2:sha256:600000',salt_length=8)
            print (password)
            new_user=User(
                name=reg_form.name.data,
                email=reg_form.email.data,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f"{reg_form.name.data} is registered successfully",category='info')
            login_user(new_user)
            return redirect("/")
        else:
            flash("The email address is already registered",category='info')
            return redirect(url_for('login'))
    else:
        print ("No form, lets send empty page")
        return render_template("register.html",form=reg_form)

    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

@app.route('/post/<int:post_id>',methods=['POST','GET'])
def show_post(post_id):
    requested_post=db.get_or_404(BlogPost,post_id)
    comment_form=CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment=Comment(
            text = comment_form.comment_text.data,
            comment_author = current_user,
            parent_post = requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    
    return render_template('post.html',post=requested_post,current_user=current_user,form=comment_form)

@app.route('/delete/<int:post_id>')
@admin_only
def delete_post(post_id):
    post_to_delete=db.get_or_404(BlogPost,post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route('/edit-post/<int:post_id>',methods=['POST','GET'])
@admin_only
def edit_post(post_id):
    selected_post=db.get_or_404(BlogPost,post_id)
    edit_form=CreatePostForm(
        title=selected_post.title,
        subtitle=selected_post.subtitle,
        img_url=selected_post.img_url,
        author=selected_post.author,
        body=selected_post.body
    )

    if edit_form.validate_on_submit():
        selected_post.title = edit_form.title.data
        selected_post.subtitle = edit_form.subtitle.data
        selected_post.img_url = edit_form.img_url.data
        selected_post.author = current_user
        selected_post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post',post_id=selected_post.id))
    return render_template('make-post.html',form=edit_form, is_edit=True)
    



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

