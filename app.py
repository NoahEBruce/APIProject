from flask import Flask, jsonify, request, redirect, url_for
import hashlib
import requests
import math
import redis
from redis import Redis, RedisError
import sys

import logging

app = Flask(__name__)

if __name__ == '__main__':
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #Change Redis DB if working with Docker

    redis = Redis(host="redis-server", port=6379, db=0)
    app.run(host='0.0.0.0', port=4000)

logger = logging.getLogger(__name__)

# POST or CREATE function, checks if keyval is proper, db is okay, then creates keyval
# PUT or UPDATE function, checks if keyval exists, updates
@app.route('/keyval', methods=['POST', 'PUT'])
def pnp_write():

    incoming_jsoned = {
    # Preparing the returned JSON info
    'key': None,
    'value': None,
    'command': 'CREATE' if request.method=='POST' else 'UPDATE',
    'result': False, 'error': None
    }

    # Ckeck if valid JSON is being received
    try:
        package = request.get_json(silent=True)
        incoming_jsoned['key'] = package['key']
        incoming_jsoned['value'] = package['value']
        incoming_jsoned['command'] += f" {package['key']}/{package['value']}"
    except:
        incoming_jsoned['error'] = "Invalid request due to input error, invalid JSON, etc."
        return jsonify(incoming_jsoned), 400

    # Check if Redis is available and working
    try:
        redis_keyvals = redis.get(incoming_jsoned['key'])
    except RedisError:
        incoming_jsoned['error'] = "Redis has encountered an error and is not functioning properly."
        return jsonify(incoming_jsoned), 400

    # Does key exists? Is anything real?
    if request.method == 'POST' and not redis_keyvals == None:
        incoming_jsoned['error'] = "Unable to add pair: key already exists."
        return jsonify(incoming_jsoned), 409

    # Just kidding, can't update what doesn't exist
    elif request.method == 'PUT' and redis_keyvals == None:
        incoming_jsoned['error'] = "Unable to update record because key does not exist."
        return jsonify(incoming_jsoned), 404

    # Passing all proper tests and requests, create key and announce success
    else:
        if redis.set(incoming_jsoned['key'], incoming_jsoned['value']) == False:
            incoming_jsoned['error'] = "Value could not / was not properly created in Redis."
            return jsonify(incoming_jsoned), 400
        if incoming_jsoned['result'] == True:
            return jsonify(incoming_jsoned), 200

# GET or READ function, checks if keyval does not exist, then attemps to create
# DELETE function, checks if keyval exists, if does, then deletes it
@app.route('/keyval/<string:key>', methods=['GET', 'DELETE'])
def gnd_retdel(key):
    incoming_json = {
        'key': key, 'value': None,
        'command': "{} {}".format('RETRIEVE' if request.method=='GET' else 'DELETE', key),
        'result': False, 'error': None
    }

    # Check if Redis connection is working
    try:
        redis_keyvals = redis.get(key)
    except RedisError:
        incoming_json['error'] = "Redis connection was unsuccessful."
        return jsonify(incoming_json), 400

    # Nothing occurs if nothing is realllllllllllll
    if redis_keyvals == None:
        incoming_json['error'] = "The supplied key does not exist."
        return jsonify(incoming_json), 404
    else:
        incoming_json['value'] = redis_keyvals

    if request.method == 'GET':
        incoming_json['result'] = True
        return jsonify(incoming_json), 200

    else:
        if request.method == 'DELETE':
            ret = redis.delete(key)
        if ret == 1:
            incoming_json['result'] = True
            return jsonify(incoming_json)
        else:
            incoming_json['error'] = f"Unable to delete key (expected return value 1; client returned {ret})"
            return jsonify(incoming_json), 400
        
@app.route('/')
def hello():
    return jsonify(output="Hello World!")

@app.route('/api/add', methods=['POST'])
def add():
    data = request.get_json()
    sum = data['a'] + data['b']
    return jsonify({'sum': sum})

# returns the MD5 hash of the string that is passed as the input
@app.route('/md5/<string:s>', methods=['GET'])
def md5(s):
    md5_hash = hashlib.md5(s.encode()).hexdigest()
    return jsonify({'input': s,
    'output': md5_hash})

# returns the factorial for the integer that is passed as input
@app.route('/factorial/<int:n>', methods=['GET'])
def factorial_n(n):
    result = math.factorial(n)
    return jsonify({'input': n,
    'output': result})

# returns an array of integers with all the Fibonacci numbers that are less than or equal to the input number
@app.route('/fibonacci/<int:n>', methods=['GET'])
def fibonacci_n(n):
    a, b = 0, 1
    fibo_nums = [a]
    while b <= n:
        a, b = b, a + b
        fibo_nums.append(a)
    return jsonify({'input': n,
    'output': fibo_nums})

# returns a boolean value depending on whether the input is a prime number
@app.route('/is-prime/<int:n>', methods=['GET'])
def is_prime(n):
    with app.app_context():
        integer = int(n)
    if integer < 2:
        return jsonify({'input': integer, 'output': False})
    for i in range(2, integer):
        if integer % i == 0:
            return jsonify({'input': integer, 'output': False})
    return jsonify({'input': integer, 'output': True})

# attempts to post the value of the input into our team Slack channel
@app.route('/slack-alert/<string>', methods=['GET'])
def slack_alert(string):
    with app.app_context():
        url = "https://hooks.slack.com/services/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" 
        package = {"text": string}
        response = requests.post(url, json=package)
    if response.status_code != 200:
        return jsonify({'input': string, 'output': False}), 500
    return jsonify({'input': string, 'output': True})

@app.route('/help')
def get_help():
    print("format: ./app.py COMMAND <arguments>")
    print("Command line options:")
    print("--value : GET or SET values from Redis database.")
    print("        Accepted arguments: GET <key>, SET <key> <value>, DEL <key>")
    print("--md5 : Returns MD5 hash of input string passed.")
    print("        Accepted arguments: <string to MD5 hash>")
    print("--isprime : Returns boolean value of input if prime or not.")
    print("        Accepted arguments: <integer to test if prime>")
    print("--fibo : Returns array of integers with Fibonacci numbers less or equal to input.")
    print("        Accepted arguments: <number>")
    print("--fact : Returns factorial of input number")
    print("        Accepted arguments: <number>")
    print("--slack : Posts a custom slack alert")
    print("        Accepted arguments: <word>...<entire sentence maybe>")
    exit()

if len(sys.argv) < 0:
    get_help()


# name is 0 (./app.py)
# command is 1 (--md5, --fibo)
# argument is 2 (ex, ex, ex)

COMMAND = sys.argv[1:]

if COMMAND[1].lower() == "--value":
    if len(COMMAND) == 4:
        if COMMAND[2].lower() == "get":
            gnd_retdel(COMMAND[2])
        elif COMMAND[2].lower() == "del":
            gnd_retdel(COMMAND[3])
    elif len(COMMAND) == 5 and COMMAND[2].lower() == "set":
        pnp_write(COMMAND[3], COMMAND[4])
    else:
        print("Error: Invalid command or incorrect arguments passed.")

elif COMMAND[1].lower() == "--md5":
    numero = int(COMMAND[2])
    s = numero
    print(md5(s))
    print(logger.info("Some text for console and log file"))

elif COMMAND[1].lower() == "--slack":
   message = str(COMMAND[2])
   slack_alert(message)

elif COMMAND[1].lower() == "--fact":
    canifactor = int(COMMAND[2])
    factorial_n(canifactor)

elif COMMAND[1].lower() == "--fibo":
    fancy = COMMAND[2]
    fibonacci_n(fancy)

elif COMMAND[1].lower() == "--isprime":
    caniprime = int(COMMAND[2])
    is_prime(caniprime)