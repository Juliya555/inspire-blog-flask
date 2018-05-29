from flask import Blueprint
from flask import render_template

from models import Post

from flask import request
from app import db

posts = Blueprint("posts", __name__, template_folder="templates")


# http://localhost/all_posts
@posts.route("/all_posts")
def show_all_posts():
    posts = Post.query.all()

    q = request.args.get("q")
    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))  # .all()
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=6)
    return render_template("posts/all_posts.html", pages=pages)
