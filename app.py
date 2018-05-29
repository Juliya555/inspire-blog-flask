from config import Configuration
from flask import Flask
from flask import redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import form
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

app.config["SECURITY_REGISTERABLE"] = True
mail = Mail()
mail.init_app(app)

# email server
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=Configuration.MAIL_USERNAME,
    MAIL_PASSWORD=Configuration.MAIL_PASSWORD,
)

### ADMIN ###
from models import *


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login", next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ["short_title", "title", "body", "tags", "category", "created", "images", "author_id", "comments"]


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ["name", "posts"]


class CategoryAdminView(AdminMixin, BaseModelView, sqla.ModelView):
    form_columns = ["title", "image", "filter_name", "posts"]
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        "image": form.FileUploadField
    }

    # Pass additional parameters to "path" to FileUploadField constructor
    form_args = {
        "image": {
            "label": "Please choose image",
            "base_path": "static/images/category",
            "allow_overwrite": False
        }
    }


class PostImageAdminView(AdminMixin, sqla.ModelView):
    form_columns = ["name", "image_path", "is_main", "post_id"]
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        "image_path": form.FileUploadField
    }

    # Pass additional parameters to "path" to FileUploadField constructor
    form_args = {
        "image_path": {
            "label": "Please choose image",
            "base_path": "static/images/posts_images",
            "allow_overwrite": False
        }
    }


class UserAdminView(AdminMixin, sqla.ModelView):
    form_columns = ["username", "email", "active", "posts", "comments", "roles"]


class CommentAdminView(AdminMixin, sqla.ModelView):
    form_columns = ["body", "timestamp", "author_id", "post_id"]


class SubscriberAdminView(AdminMixin, sqla.ModelView):
    form_columns = ["subscriber_name", "email"]


admin = Admin(app, "Flaskapp", url="/", index_view=HomeAdminView(name="Home"))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(CategoryAdminView(Category, db.session))
admin.add_view(PostImageAdminView(PostImage, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(CommentAdminView(Comment, db.session))
admin.add_view(SubscriberAdminView(Subscriber, db.session))

### Flask Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
