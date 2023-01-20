import os
from collections import defaultdict
from flask import Flask, render_template, request, Response
import requests
import json
from pytrie import Trie
import uuid
import re


from flaskr.nav import *


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


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def Home():
    return render_template("index.html")


@app.route("/<name>", methods=['GET', 'POST'])
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


data = list()
country_index = defaultdict(list)
name_index = dict()
domain_index = defaultdict(list)


r = requests.get('https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json')


@app.route("/search?name=", methods=['GET', 'POST'])
def search():
    if not data_loaded:
        load_data()

    country = request.args.get('country')
    name = request.args.get('name')
    name_contains = request.args.get('name_contains')
    domain = request.args.get("domain")
    filtered = data
    if name and country:
            name = name.lower()
            country = country.lower()
            name_filtered = prefix_tree.values(prefix=name)
            filtered = [uni for uni in name_filtered if uni['country'].lower() == country]
    elif name_contains and country:
            country = country.lower()
            regex = re.compile(r'\b{0}'.format(name_contains.lower()))
            name_filtered = [uni for uni in data if regex.search(uni['name'].lower())]
            filtered = [uni for uni in name_filtered if uni['country'].lower() == country]
    elif name_contains:
            regex = re.compile(r'\b{0}'.format(name_contains.lower()))
            filtered = [uni for uni in data if regex.search(uni['name'].lower())]
    elif name:
            name = name.lower()
            filtered = prefix_tree.values(prefix=name)
    elif country:
            country = country.lower()
            filtered = country_index[country]
    elif domain:
            filtered = domain_index[domain]

    return Response(json.dumps(filtered), mimetype='application/json')


data_loaded = False




def load_data():
    global data_loaded, prefix_tree, data, country_index, name_index, domain_index
    response = requests.get("https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json")
    data = response.json()
    for i in data:
        country_index[i["country"].lower()].append(i)
        name_index[i['name'].lower()] = i
        for domain in i["domains"]:
            domain_index[domain].append(i)
        splitted = i['name'].split(" ")
        if len(splitted) > 1:
            for splitted_name in splitted[1:]:
                name_index[splitted_name.lower() + str(uuid.uuid1())] = i
    prefix_tree = Trie(**name_index)


    data_loaded = True


if __name__=="__main__":
    app.run(debug=True)
