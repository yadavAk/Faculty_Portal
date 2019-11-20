from flask import (render_template, url_for, flash, 
                redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from facultyportal import db, mdb
from facultyportal.models import Post
from facultyportal.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_publication():
    form = PostForm()
    if form.validate_on_submit():
        mdb.addPublication(current_user.email, form.title.data, form.content.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')

@posts.route("/post/<string:pubtitle>")
def post(pubtitle):
    # post = Post.query.get_or_404(post_id)
    post = mdb.getPublication(current_user.email, pubtitle)
    return render_template('post.html', title=pubtitle, post=post)

@posts.route("/post/update/", methods=['GET', 'POST'])
@login_required
def update_post():
    pubtitle = request.args.get('pubtitle')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        mdb.updatePublication(email=current_user.email, title=title, content=content)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', pubtitle=pubtitle))
    elif request.method == 'GET':
        form.title.data = pubtitle
        post = mdb.getPublication(current_user.email, pubtitle)
        form.content.data = post['pubs'][0]['content']
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')

@posts.route("/post/delete", methods=['POST'])
@login_required
def delete_post():
    pubtitle = request.args.get('pubtitle')
    # if post.author != current_user:
    #     abort(403) # 403 means forbidden route
    mdb.deletePublication(email=current_user.email, title=pubtitle)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


