from flask import Blueprint, render_template, request,\
redirect, url_for, session, current_app
from .models import Post, User
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/posts')
def show_posts():
    if session.get('user_available'):
        posts = current_app.session.query(Post).all()
        return render_template('posts.html', posts=posts)
    return redirect(url_for('blog.index'))

@bp.route('/add', methods=['GET', 'POST'])
def add_post():
    if session.get('user_available'):
        form = AddPostForm()
        session_db = current_app.session
        us = session_db.query(User).filter_by(username=session['current_user']).first()
        if form.validate_on_submit():
            post = Post(title=form.title.data,
                      description=form.description.data,
                      puid=us.uid)
            session_db.add(post)
            session_db.commit()
            return redirect(url_for('blog.show_posts'))
        return render_template('add.html', form=form)
    return redirect(url_for('blog.index'))

@bp.route('/update/<int:pid>/<post_owner>', methods=['GET', 'POST'])
def update_post(pid, post_owner):
    if session.get('current_user') == post_owner:
        session_db = current_app.session
        post = session_db.query(Post).get(pid)
        form = AddPostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.description = form.description.data
            session_db.commit()
            return redirect(url_for('blog.show_posts'))
        return render_template('update.html', form=form)
    return redirect(url_for('blog.show_posts'))

@bp.route('/delete/<int:pid>/<post_owner>', methods=['GET', 'POST'])
def delete_post(pid, post_owner):
    if session.get('current_user') == post_owner:
        session_db = current_app.session
        post = session_db.query(Post).get(pid)
        session_db.delete(post)
        session_db.commit()
        return redirect(url_for('blog.show_posts'))
    return redirect(url_for('blog.show_posts'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        session_db = current_app.session
        user = User(username=form.username.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=form.password.data)
        session_db.add(user)
        session_db.commit()
        return redirect(url_for('blog.index'))
    return render_template('signup.html', form=form)

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        session_db = current_app.session
        user = session_db.query(User).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_available'] = True
            session['current_user'] = user.username
            return redirect(url_for('blog.show_posts'))
    return render_template('signin.html', form=form)
