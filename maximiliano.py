from flask import Flask, request, Response
import ConfigParser
import json
import os

TASKS_CONTENT_TYPE = "application/vnd.abiquo.tasks+json"
TASK_CONTENT_TYPE = "application/vnd.abiquo.task+json"

app = Flask(__name__)

# initialization process
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(os.environ['HOME'], ".config/maximiliano.conf"))


@app.route("/", methods=["POST"])
def listen():
    return parse_request(request)


@app.route("/twitter", methods=["GET"])
def twitter_listener():
    return "Twitter will process this request %s" % str(request)


@app.route("/fari", methods=["GET"])
def fari_listener():
    return "El FARI will process this request %s" % str(request)


def execute_workflow(task):
    '''
    Will receive a list of tasks (VM if only one)
    '''
    print "Root received task list %s" % str(task)

    # Parsear enterprise name
    print Config.get("enterprises", get_enterprise_name())
    return 500


def get_enterprise_name():
    return "FAKE"


def parse_request(request):
    if TASKS_CONTENT_TYPE == request.headers['content-type']:
        dto = json.dumps(request.data)
        execute_workflow(dto)
    elif TASK_CONTENT_TYPE == request.headers['content-type']:
        dto = json.dumps(request.data)
        execute_workflow([dto])
        return Response(status=200)
    else:
        return Response(status=415)

if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)
