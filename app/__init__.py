from flask import Flask, g, request, current_app, flash
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from jinja2 import Template

from .extensions import db
from .config import Config

import uuid
import os
from .permissions import is_allowed
from .models import User

alembic = Alembic()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from .site.routes import site_blueprint
    from .admin import admin_blueprint
    from .nomination.routes import nominate_blueprint
    from .vote.routes import vote_blueprint

    from .errors.handlers import error_blueprint

    def template_function(func):
        app.jinja_env.globals[func.__name__] = func
        return func

    @template_function
    def is_admin():
        if is_development():
            print("development - is_admin")
            u = User.query.filter(User.jhed_id == 'dbelros1').first()
        else:
            if 'USERPRINCIPALNAME' in request.headers:
                u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()
        print(u)
        if u is None:
            return "bad bad bad", 500

        if u.administrator:
            print("Is an administrator")
            return True
            
        return False

    @template_function
    def is_authenticated():
        print(request.headers)
        if 'USERPRINCIPALNAME' in request.headers:
            print("headers exist")
            u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()
            print(u)
            if u is None:
                print("user in headers does not exist")
                return "bad bad bad bad bad", 500

            return True

        print("header's don't exist")
        return False
    
    app.register_blueprint(site_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(nominate_blueprint)
    app.register_blueprint(vote_blueprint)

    app.register_blueprint(error_blueprint)

    db.init_app(app)
    alembic.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    csrf.init_app(app)
    Bootstrap(app)
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response
    @app.before_request
    def set_user():
        if is_development():
            u = User.query.filter(User.jhed_id == 'dbelros1').first()
        else:
            u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()
                
        if u is not None:
            if is_development():
                u.givenname = 'Derek'
                u.surname = 'Belrose'
                u.email = 'dbelrose@jhu.edu'
            else:
                u.givenname = request.headers.get('GIVENNAME')
                u.surname = request.headers.get('SN')
                u.email = request.headers.get('MAIL')

            db.session.commit()
        else:
            u = User()
            u.id = generate_uuid()
            if is_development():
                u.jhed_id = 'dbelros1'
                u.givenname = 'Derek'
                u.surname = 'Belrose'
                u.email = 'dbelrose@jhu.edu'
                u.permissions = 111
            else:
                u.jhed_id = request.headers.get('USERPRINCIPALNAME')
                u.givenname = request.headers.get('GIVENNAME')
                u.surname = request.headers.get('SN')
                u.email = request.headers.get('MAIL')

            db.session.add(u)
            db.session.commit()
                
    return app

def generate_uuid():
    return(str(uuid.uuid1()))


def is_development():
    if os.getenv('LOCAL_DEV'):
        return True

    return False
        
