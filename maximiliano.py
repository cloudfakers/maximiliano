from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def listen():
    print request
    return "runing %s" % str(request)

if __name__ == "__main__":
    app.run(host='localhost', port=8081)
