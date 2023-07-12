from flask import Flask

server = Flask(__name__)

from app import routes

# @server.route('/')
# def index():
#     return "Hello"

# if __name__ == '__main__':
#     server.run()


