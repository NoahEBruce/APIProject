from flask import Flask, jsonify, request, redirect, url_for
import hashlib
import requests
import math
import redis
from redis import Redis, RedisError
import sys

n = len(sys.argv)

if n < 3:
    print("Usage: python script.py arg1 arg2")
    sys.exit(1)
    
COMMAND = sys.argv[1]
COMMAND2 = sys.argv[2]

print(" ")



for x in range(0, n):
    print(sys.argv[x], x)


print(" ")

s = COMMAND2

md5_hash = hashlib.md5(s.encode()).hexdigest()

print("input:", s)
print("output:", md5_hash)
