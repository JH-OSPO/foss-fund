from flask import Blueprint, render_template, redirect, request

site_blueprint = Blueprint('site', __name__)

@site_blueprint.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@site_blueprint.route('/login')
def login():
    url = request.args.get('url')
    print(url)
    return redirect(url)
