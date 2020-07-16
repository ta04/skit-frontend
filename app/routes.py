from flask import render_template, request, redirect
from app import app
import requests
import helper
import json


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
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
        jsonPayload = json.dumps(payload)
        response = requests.post("http://localhost:50057/user/store", json=jsonPayload)
        if response.status_code == 200:
            return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # elif request.method == 'POST':
