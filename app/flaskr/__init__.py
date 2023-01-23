import os

from flask import Flask, render_template, request, Response
import requests
import json


from flaskr.pages import *

app=Flask(__name__)



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

@app.route("/")
@app.route("/home")
def Home():
    return render_template("index.html")

@app.route("/<name>")
def getinterest(name):
    if name in nav:
        desc=nav[name]['desc']
        desc2=nav[name]['desc2']
        desc3=nav[name]['desc3']
        images=nav[name]['images']
        images2=nav[name]['images2']
                
        return render_template("navpages.html", name=name, nav=nav, images=images, images2=images2, desc=desc, desc2=desc2, desc3=desc3)
    else:
        return render_template("error.html")

@app.route('/home', methods=('GET', 'POST'))
def getPost():
        if request.method == 'POST':
            name=request.form['title']
            print(name)
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}").json()
            print(response)
            return render_template('search.html',response=response, name=name)
        else:
            return render_template('error.html')
        return app

