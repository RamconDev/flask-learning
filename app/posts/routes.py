from app.posts import posts_bp as posts

from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.posts.forms import CreatePostForm
from app import db

from app.models import Post, Category


@posts.route('/posts_list')
def posts_list():
    posts = db.session.execute(
        db.select(Post).order_by(Post.id.desc())
    ).scalars().all()
    return render_template('posts_list.html', posts=posts)

@posts.route('/post_create', methods=['GET', 'POST'])
@login_required
def post_create():

    form = CreatePostForm()

    categories = Category.query.all()
    form.category.choices = [(0, 'No Category')] + [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post = Post.create_post(
            title = form.title.data,
            content = form.content.data,
            user_id = current_user.id,
            category_id = form.category.data
        )
        db.session.add(post)
        db.session.commit()
        flash("Post creado exitosamente!")
        return redirect( url_for('posts.posts_list') )

    return render_template('/create_post.html', form=form)

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Post no encontrado")
        return redirect(url_for('posts.posts_list'))
    return render_template('post_single.html', post=post)

@posts.route('/post_edit')
def post_edit():
    pass

@posts.route('/post_delete/<int:post_id>')
def post_delete(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        flash("Post no encontrado")
        return redirect(url_for('posts.posts_list'))
    db.session.delete(post)
    db.session.commit()
    flash("Post eliminado exitosamente!")
    return redirect(url_for('posts.posts_list'))