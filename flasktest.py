"""
We will store all tweets here
Each user can execute the following commands:
    tweet "message" : creates a new tweet
    view            : displays all known tweets
    block "user"    : blocks "user" from seeing my tweets
    unblock "user"  : unblocks "user" from seeing my tweets

Methods:
    getAllTweets
    tweet: sends a message to all non-blocked peers
    < above commands >

"""


import sys
from flask import Flask
from flask import Request

peer = 0
peers = [('127.0.0.1', 1111), ('127.0.0.1', 2222), ('127.0.0.1', 3333)]


app = Flask(__name__)

@app.route('/')
def hello_world():
    print peer
    return 'Hello, World!'


if __name__ == "__main__":
    # print sys.argv
    if int(sys.argv[1]) == 1111:
        peer = 2222
        app.run(host='127.0.0.1', port=1111)
    else:
        app.run(host='127.0.0.1', port=2222)
        peer = 1111