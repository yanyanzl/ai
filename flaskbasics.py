# this is to learn how flask works

# run this file and then open the http://127.0.0.1:5000
# in any web browser for the content

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello() -> str:
    return "Hello World, this is my first flask page!"


if __name__ == "__main__":
    app.run()

