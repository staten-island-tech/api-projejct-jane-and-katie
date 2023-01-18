import os
from flask import Flask, render_template, request
import requests
import json

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

    return app


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(name)

r = requests.get("https://pokeapi.co/api/v2/pokemon/charmander").json()

data = requests.get("https://pokeapi.co/api/v2/pokemon?limit=150&offset=0").json()

@app.route('/', methods=('GET', 'POST'))
def getPost():
    if request.method == 'POST':
        name = request.form['name']
        data = requests.get(f"'https://api.api-ninjas.com/v1/{name}").json()
        response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
        print(request.form)
        return render_template('test.html',data=data)
    else:
        return render_template('index.html')
    
if __name__=="__main__":
    app.run(debug=True)