from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.utils.errors import register_error_handlers
from app.utils.helpers import timedelta

from app.database.models import db
from app.database.seed import seed_data

from app.integrations.processing.mail.mailpit import mail

from app.resources.auth import auth
from app.resources.admin import admin
from app.resources.company import company
from app.resources.student import student

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ZzJ*PoVgz#IGnQ!D39XSS86dlNa7ejlIpRDv%2JD&B2#ngmKVEfZc0*adE$bup$$JhSii3^dKhxd#pvTJq7z8@h!6JnOerg8MFbB"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_portal.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    app.config["SESSION_REFRESH_EACH_REQUEST"] = True

    app.config["MAIL_SERVER"] = "127.0.0.1"
    app.config["MAIL_PORT"] = 1025
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_DEFAULT_SENDER"] = "info@placementconnect.com"

    db.init_app(app)
    mail.init_app(app)

    CORS(app, origins=["http://127.0.0.1:8000"], supports_credentials=True)

    api = Api(app)
    
    register_error_handlers(api)

    api.add_namespace(auth)
    api.add_namespace(admin)
    api.add_namespace(company)
    api.add_namespace(student)

    return app

def init_db(app):

    with app.app_context():

        db.create_all()

        seed_data()
