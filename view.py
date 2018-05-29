from app import app
from flask import render_template, request
from flask import redirect
from flask import url_for
from flask import flash

from app import db

from flask_security import login_required
from flask_security import current_user

from flask_mail import Mail
from flask_mail import Message


mail = Mail()
mail.init_app(app)


from models import Category, Post, Tag, PostImage, Comment, User, Subscriber
from forms import PostForm, CommentForm, SubscriberForm


@app.route("/")
def index():
    categories = Category.query.all()
    posts = Post.query.all()
    users = User.query.all()
    return render_template('index.html', categories=categories, posts=posts, users=users)


# http://localhost/create_post
@app.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == 'POST':
        short_title = request.form['short_title']
        title = request.form['title']
        body = request.form['body']
        category_id = request.form['category_id']
        author_id = current_user.id

        post = Post(short_title=short_title, title=title, body=body, category_id=category_id,
                    author_id=author_id)

        dict_tags = dict(request.form.items())['tags']
        tags = Tag.query.filter(Tag.id == dict_tags).first_or_404()
        post.tags.append(tags)
        db.session.add(post)
        db.session.commit()

        category = Category.query.filter(Category.id == category_id).first_or_404()
        category_slug = category.category_slug
        return redirect(url_for('show_category_posts', category_slug=category_slug))

    form = PostForm()
    return render_template('create_post.html', forma=form)


# http://localhost/category_slug
@app.route("/<category_slug>")
def show_category_posts(category_slug):
    category = Category.query.filter(Category.category_slug==category_slug).first_or_404()
    posts = Post.query.filter(Post.category_id==category.id)
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = posts.filter(Post.title.contains(q) | Post.body.contains(q))#.all()
    else:
        posts = posts.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=6)
    return render_template('category_posts.html', category=category, pages=pages)


# http://localhost/category_slug/post_slug
@app.route("/<string:category_slug>/<string:post_slug>", methods=["GET", "POST"])
def post_detail(category_slug, post_slug):
    category = Category.query.filter(Category.category_slug==category_slug).first_or_404()
    post = Post.query.filter(Post.post_slug==post_slug).first_or_404()
    tags = post.tags
    images = PostImage.query.filter(PostImage.post_id==post.id)
    categories = Category.query.all()

    form = CommentForm()

    if request.method == "POST":
        body = request.form["body"]
        author = current_user._get_current_object()
        post_id = post.id

        comment = Comment(body=body,
                          author=author,
                          post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been published.")
        return redirect(url_for("post_detail", category_slug=category.category_slug, post_slug=post.post_slug))

    return render_template("post_detail.html", category=category, post=post, tags=tags, images=images, categories=categories)


# http://localhost/category_slug/post_slug/tag
@app.route("/tag/<tag_slug>")
def tag_detail(tag_slug):
    tag = Tag.query.filter(Tag.tag_slug==tag_slug).first_or_404()
    posts = Post.query.filter(Post.tags.any(id=tag.id))

    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    posts = posts.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=6)
    return render_template("tag_detail.html", tag=tag, pages=pages)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = SubscriberForm()
    if request.method == "POST":
        subscriber_name = request.form["subscriber_name"]
        email = request.form["email"]

        subscriber = Subscriber(subscriber_name=subscriber_name,
                                email=email)
        db.session.add(subscriber)
        db.session.commit()

        message_subject = "10 Color Theory Basics Everyone Should Know"
        message_body = "Thank you for choosing Inspire Blog! Enjoy new ideas every day :) \n" \
                       "To start with - please follow our guide on Color Theory Basics."

        msg = Message(subject=message_subject,
                      body=message_body,
                      sender="inspire.blog55@gmail.com",
                      recipients=[email])

        filename = "10 Color Theory Basics Everyone Should Know.pdf"

        with app.open_resource("static/images/messages/" + filename) as fp:
            msg.attach(filename, "10 Color Theory Basics Everyone Should Know/pdf", fp.read())

        mail.send(msg)
        flash("Message sent")
        return redirect(url_for("index"))

    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404