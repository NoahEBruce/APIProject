from flask import Flask, jsonify, request, redirect, url_for
import hashlib
import requests
import math
import redis
from redis import Redis, RedisError
import sys

print(" ")

n = len(sys.argv)

for x in range(0, n):
    print(sys.argv[x], x)

print(" ")

if len(sys.argv) < 3:
    print("Please provide at least two command-line arguments.")
    sys.exit(1)

COMMAND = sys.argv[1]
COMMAND2 = sys.argv[2]

print("Input 1:", COMMAND)
print("Input 2:", COMMAND2)

s = COMMAND2
md5_hash = hashlib.md5(s.encode()).hexdigest()

print("input:", s)
print("output:", md5_hash)
