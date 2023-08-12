from flask import Flask, jsonify, request, redirect, url_for
import hashlib
import requests
import math
import redis
from redis import Redis, RedisError
import sys

COMMAND = sys.argv[0:]
COMMAND2 = sys.argv[1]

print(" ")

n = len(sys.argv)

for x in range(0, n):
    print(sys.argv[x], x)


print(" ")

s = COMMAND2

md5_hash = hashlib.md5(s.encode()).hexdigest()

print("input:", s)
print("output:", md5_hash)
