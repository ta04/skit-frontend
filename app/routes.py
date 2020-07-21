import json
import requests
import helper
from flask import render_template, request, redirect, make_response, jsonify, url_for
from app import app


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        password = request.form.get("password")
        n = helper.generateN()
        g = helper.calculateG(n)
        x = helper.calculateX(password, n)
        y = helper.calculateY(g, x, n)

        payload = {
            "first_name": request.form.get("first-name"),
            "last_name": request.form.get("last-name"),
            "username": request.form.get("username"),
            "password": y,
            "prime_number": n,
            "generator_value": g,
            "email_address": request.form.get("email-address"),
            "phone_number": request.form.get("phone-number"),
            "date_of_birth": request.form.get("date-of-birth"),
            "address": request.form.get("address"),
            "role": "customer",
            "status": "active"
        }
        response = requests.post(
            "http://localhost:50057/user/store", json=payload)
        if response.status_code == 200:
            return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # calculate t
        g, n = None, None
        payload = {
            "username": username,
            "with_credentials": True
        }
        response = requests.post(
            "http://localhost:50057/user/show", json=payload)
        if response.status_code == 200:
            responseJson = response.json()
            g = responseJson['user']['generator_value']
            n = responseJson['user']['prime_number']
        v = helper.generateV(n)
        t = helper.calculateT(g, v, n)

        # do auth1
        c = None
        payload = {
            "username": username,
            "t": f'{t}'
        }
        response = requests.post(
            "http://localhost:50057/auth/auth1", json=payload)
        if response.status_code == 200:
            responseJson = response.json()
            c = responseJson['c']

        # do auth2
        x = helper.calculateX(password, n)
        r = helper.calculateR(v, int(c), x)
        payload = {
            "username": username,
            "r": f'{r}',
            "c": c
        }
        response = requests.post(
            "http://localhost:50057/auth/auth2", json=payload)
        if response.status_code == 200:
            responseJson = response.json()
            token = responseJson['token']

            return redirect(url_for('home', token=token))


@app.route('/home', methods=['GET'])
def home():
    query_parameters = request.args
    token = query_parameters.get('token')
    
    response = requests.post("http://localhost:50057/product/index", json={})
    if response.status_code == 200:
        responseJson = response.json()
        products = responseJson['products']

        if token:
            return render_template('home.html', products=products, token=token)
        else:
            return render_template('home.html', products=products)


@ app.route('/calculateResult', methods=['GET'])
def calculateResult():
    query_parameters = request.args
    g = int(query_parameters.get('g'))
    r = int(query_parameters.get('r'))
    n = int(query_parameters.get('n'))
    y = int(query_parameters.get('y'))
    c = int(query_parameters.get('c'))
    result = helper.calculateResult(g, r, n, y, c)
    resp = make_response(jsonify(result=result))
    return resp
