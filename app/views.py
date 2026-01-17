from flask import Blueprint, render_template, request,\
redirect, url_for, current_app
from .models import Post, User, Tag, PostTags
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db

bp = Blueprint('blog', __name__)

# Index - posts route-----
@bp.route('/')
def index():
    posts = db.session.query(Post).order_by(Post.pid.desc()).all()
    return render_template('index.html', posts=posts)

# Signin route-----
@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('blog.index'))
    return render_template('signin.html', form=form)

# Show tag route-----
@bp.route('/tag/<string:name>')
@login_required
def show_tag(name):
    tag = db.session.query(Tag).filter_by(name=name).first()
    if not tag:
        return redirect(url_for('blog.index'))
    posts = tag.posts
    total_minutes = sum(post.study_minutes for post in posts)
    return render_template('tag.html', posts=posts, tag=tag, total_minutes=total_minutes)

# Add route-----
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    # add new post
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    description=form.description.data,
                    puid=current_user.uid,
                    study_minutes=form.study_minutes.data
        )

        # add tags
        raw_tags = form.tags.data or ""
        tag_names = [t.strip() for t in raw_tags.split(",") if t.strip()]

        for name in tag_names:

            tag =db.session.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)

            post.tags.append(tag)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.index'))

    return render_template('add.html', form=form)

# Update route-----
@bp.route('/update/<int:pid>', methods=['GET', 'POST'])
@login_required
def update_post(pid):
    post = db.session.get(Post, pid)

    if current_user.uid != post.puid:
        return redirect(url_for('blog.index'))

    form = AddPostForm(obj=post)
    # 既存のタグをフォームにセット
    if request.method == 'GET':
        tag_names = [tag.name for tag in post.tags]
        form.tags.data = ", ".join(tag_names)

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.study_minutes = form.study_minutes.data
        # update tags
        raw_tags = form.tags.data or ""
        tag_names = [t.strip() for t in raw_tags.split(",") if t.strip()]

        post.tags.clear()

        for name in tag_names:
            tag = db.session.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            post.tags.append(tag)

        db.session.commit()
        return redirect(url_for('blog.index'))
    return render_template('update.html', form=form)

# Delete route-----
@bp.route('/delete/<int:pid>', methods=['GET', 'POST'])
@login_required
def delete_post(pid):
    post = db.session.query(Post).get(pid)
    if current_user.uid == post.puid:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog.index'))
    return redirect(url_for('blog.index'))

# Signup route-----
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('blog.index'))
    return render_template('signup.html', form=form)

# Logout route-----
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))
