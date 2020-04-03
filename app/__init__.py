# Flask
from flask import Flask, request
app = Flask(__name__)

# Add Routes
from app import routes

if __name__ == '__main__':
    app.run()
