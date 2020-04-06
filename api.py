import flask
import libnum
from flask import request, make_response, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/getY', methods=['GET'])
def getY():
    query_parameters = request.args
    g = int(query_parameters.get('g'))
    x = int(query_parameters.get('x'))
    n = int(query_parameters.get('n'))
    y = pow(g, x, n)
    resp = make_response(jsonify(y = y))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    resp.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token"
    return resp

@app.route('/getT', methods=['GET'])
def getT():
    query_parameters = request.args
    g = int(query_parameters.get('g'))
    v = int(query_parameters.get('v'))
    n = int(query_parameters.get('n'))
    t = pow(g, v, n)
    resp = make_response(jsonify(t = t))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    resp.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token"
    return resp

@app.route('/getR', methods=['GET'])
def getR():
    query_parameters = request.args
    v = int(query_parameters.get('v'))
    c = int(query_parameters.get('c'))
    x = int(query_parameters.get('x'))
    r = (v - c * x)

    resp = make_response(jsonify(r = r))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    resp.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token"
    return resp

@app.route('/calculateResult', methods=['GET'])
def calculateResult():
    query_parameters = request.args
    g = int(query_parameters.get('g'))
    r = int(query_parameters.get('r'))
    n = int(query_parameters.get('n'))
    y = int(query_parameters.get('y'))
    c = int(query_parameters.get('c'))
    result = (libnum.invmod(pow(g, -r, n), n) * pow(y, c, n)) % n

    resp = make_response(jsonify(result = result))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    resp.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token"
    return resp
    
app.run(host="0.0.0.0", port=80)