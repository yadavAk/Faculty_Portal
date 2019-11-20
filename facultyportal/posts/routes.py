from flask import (render_template, url_for, flash, 
                redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from facultyportal import db, mdb
from facultyportal.models import Post
from facultyportal.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/new/publication", methods=['GET', 'POST'])
@login_required
def new_publication():
    form = PostForm()
    if form.validate_on_submit():
        mdb.addPublication(current_user.email, form.title.data, form.content.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')


@posts.route("/new/award", methods=['GET', 'POST'])
@login_required
def new_award():
    form = PostForm()
    if form.validate_on_submit():
        mdb.addAward(current_user.email, form.title.data, form.content.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')


@posts.route("/new/other", methods=['GET', 'POST'])
@login_required
def new_other():
    form = PostForm()
    if form.validate_on_submit():
        mdb.addOther(current_user.email, form.title.data, form.content.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('create_post.html', title='New Post', 
                            form=form, legend='New Post')


@posts.route("/post/bio/<string:biotitle>")
def post_bio(biotitle):
    # post = Post.query.get_or_404(post_id)
    post = mdb.getBio(current_user.email, biotitle)
    return render_template('post_bio.html', title=biotitle, post=post)


@posts.route("/post/<string:pubtitle>")
def post(pubtitle):
    # post = Post.query.get_or_404(post_id)
    post = mdb.getPublication(current_user.email, pubtitle)
    return render_template('post.html', title=pubtitle, post=post)

@posts.route("/post/award/<string:awardtitle>")
def post_award(awardtitle):
    # post = Post.query.get_or_404(post_id)
    post = mdb.getAward(current_user.email, awardtitle)
    return render_template('post_award.html', title=awardtitle, post=post)

@posts.route("/post/other/<string:othertitle>")
def post_other(othertitle):
    # post = Post.query.get_or_404(post_id)
    post = mdb.getOther(current_user.email, othertitle)
    return render_template('post_other.html', title=othertitle, post=post)

@posts.route("/bio/update/", methods=['GET', 'POST'])
@login_required
def update_bio():
    biotitle = request.args.get('biotitle')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        mdb.updateBio(email=current_user.email, title=title, content=content)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post_bio', biotitle=title))
    elif request.method == 'GET':
        form.title.data = biotitle
        try:
            post = mdb.getBio(current_user.email, biotitle)
            form.content.data = post['bio']['content']
        except:
            form.content.data = 'Bio Empty'
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')


@posts.route("/publication/update/", methods=['GET', 'POST'])
@login_required
def update_post():
    pubtitle = request.args.get('pubtitle')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        mdb.updatePublication(email=current_user.email, old_title=pubtitle, title=title, content=content)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', pubtitle=title))
    elif request.method == 'GET':
        form.title.data = pubtitle
        print(pubtitle)
        post = mdb.getPublication(current_user.email, pubtitle)
        form.content.data = post['pubs'][0]['content']
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')


@posts.route("/awards/update/", methods=['GET', 'POST'])
@login_required
def update_award():
    awardtitle = request.args.get('awardtitle')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        mdb.updateAward(email=current_user.email, old_title=awardtitle, title=title, content=content)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post_award', awardtitle=title))
    elif request.method == 'GET':
        form.title.data = awardtitle
        post = mdb.getAward(current_user.email, awardtitle)
        form.content.data = post['award'][0]['content']
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')

@posts.route("/other/update/", methods=['GET', 'POST'])
@login_required
def update_other():
    othertitle = request.args.get('othertitle')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        mdb.updateOther(email=current_user.email, old_title=othertitle, title=title, content=content)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post_other', othertitle=title))
    elif request.method == 'GET':
        form.title.data = othertitle
        post = mdb.getOther(current_user.email, othertitle)
        form.content.data = post['other'][0]['content']
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
    return redirect(url_for('users.profile'))


@posts.route("/award/delete", methods=['POST'])
@login_required
def delete_award():
    awardtitle = request.args.get('awardtitle')
    # if post.author != current_user:
    #     abort(403) # 403 means forbidden route
    mdb.deleteAward(email=current_user.email, title=awardtitle)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.profile'))


@posts.route("/other/delete", methods=['POST'])
@login_required
def delete_other():
    othertitle = request.args.get('othertitle')
    # if post.author != current_user:
    #     abort(403) # 403 means forbidden route
    mdb.deleteOther(email=current_user.email, title=othertitle)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.profile'))


