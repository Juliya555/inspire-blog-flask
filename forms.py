from wtforms import Form
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email

from flask import request
from sqlalchemy.orm import load_only
from models import Category, Tag, Subscriber


def category_query():
    return Category.query


def tags_query():
    return Tag.query


class PostForm(Form):
    short_title = StringField("Short Title", validators=[Length(min=1, max=30, message="too long")], render_kw={"placeholder": "max 30 characters"})
    title = StringField("Title")
    body = TextAreaField("Body")
    category_id = QuerySelectField("Category", query_factory=category_query,
                                allow_blank=True, get_label="title",
                                get_pk=lambda x: x.id)

    tags = QuerySelectMultipleField("Tags", query_factory=tags_query,
                                allow_blank=True, get_label="name",
                                get_pk=lambda x: x.id,
                                # _name="tags[]"
                                )

    # images = FileField("Images")


class CommentForm(Form):
    body = StringField("", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SubscriberForm(Form):
    subscriber_name = StringField("", validators=[DataRequired()])
    email = StringField("Email address", validators=[Email()])
    submit = SubmitField("Submit")

