from flask import Blueprint, render_template, request,\
redirect, url_for, current_app
from .models import Post, User
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('blog', __name__)

# Index route-----
@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SignInForm()
    if form.validate_on_submit():
        session_db = current_app.session
        user = session_db.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('blog.show_posts'))
    return render_template('index.html', form=form)

# Show posts route-----

@bp.route('/posts')
@login_required
def show_posts():
    posts = current_app.session.query(Post).all()
    return render_template('posts.html', posts=posts)

# Add route-----
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    session_db = current_app.session
    us = current_user
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    description=form.description.data,
                    puid=us.uid)
        session_db.add(post)
        session_db.commit()
        return redirect(url_for('blog.show_posts'))
    return render_template('add.html', form=form)

# Update route-----
@bp.route('/update/<int:pid>', methods=['GET', 'POST'])
@login_required
def update_post(pid):
    session_db = current_app.session
    post = session_db.query(Post).get(pid)

    if current_user.uid != post.puid:
        return redirect(url_for('blog.show_posts'))

    form = AddPostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        session_db.commit()
        return redirect(url_for('blog.show_posts'))
    return render_template('update.html', form=form)

# Delete route-----
@bp.route('/delete/<int:pid>', methods=['GET', 'POST'])
@login_required
def delete_post(pid):
    session_db = current_app.session
    post = session_db.query(Post).get(pid)
    if current_user.uid == post.puid:
        session_db.delete(post)
        session_db.commit()
        return redirect(url_for('blog.show_posts'))
    return redirect(url_for('blog.show_posts'))

# Signup route-----
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        session_db = current_app.session
        user = User(username=form.username.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=hashed_pw)
        session_db.add(user)
        session_db.commit()
        return redirect(url_for('blog.index'))
    return render_template('signup.html', form=form)

# Logout route-----
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))
