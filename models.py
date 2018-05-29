from app import db
from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin


def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, "-", str(s))


# table for ManyToMany (Post-Tag)
post_tags = db.Table("post_tags",
                     db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
                     db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
                     )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_title = db.Column(db.String(30))
    title = db.Column(db.String(140))
    post_slug = db.Column(db.String(140), unique=True)  # URL for human reading
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"),
                            nullable=False)
    images = db.relationship("PostImage", backref="post", lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    tags = db.relationship("Tag", secondary=post_tags,
                           backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return "<Post id: {}, title: {}>".format(self.id, self.title)

    def generate_slug(self):
        if self.title:
            self.post_slug = slugify(self.title)


class PostImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image_path = db.Column(db.String(140))
    is_main = db.Column(db.Boolean)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __init__(self, *args, **kwargs):
        super(PostImage, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<PostImage name: {}, post_id:{}>".format(self.name, self.post_id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    category_slug = db.Column(db.String(140), unique=True)  # URL for human reading
    filter_name = db.Column(db.String(50))
    image = db.Column(db.String(140))
    posts = db.relationship("Post", backref="category", lazy=True)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.category_slug = slugify(self.title)

    def __repr__(self):
        return "<Category title: {}>".format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tag_slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        if self.name:
            self.tag_slug = slugify(self.name)

    def __repr__(self):
        return "Tag name: {}, id:{}".format(self.name, self.id)


### Flask Security

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, index=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<User %r>" % self.username


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __repr__(self):
        return "comment_id:{}, <comment: {}>".format(self.id, self.body[:25])


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_name = db.Column(db.String(25), unique=True, index=True)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return "<Subscriber %r>" % self.subscriber_name
