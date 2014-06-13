from flask import Flask, request, Response
import ConfigParser
import json
import os
import requests as client

TASKS_CONTENT_TYPE = "application/vnd.abiquo.tasks+json"
TASK_CONTENT_TYPE = "application/vnd.abiquo.task+json"

app = Flask(__name__)

# initialization process
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(os.environ['HOME'], ".config/maximiliano.conf"))


@app.route("/", methods=["POST"])
def listen():
    return parse_request(request)


@app.route("/twitter", methods=["POST"])
def twitter_listener():
    return "Twitter will process this request %s" % str(request)


@app.route("/fari", methods=["POST"])
def fari_listener():
    return "El FARI will process this request %s" % str(request)


def execute_workflow(tasks):
    '''
    Will receive a list of tasks (VM if only one)
    '''
    # Parsear enterprise name
    enterprise_name = get_enterprise_name(tasks)
    workflow_parser = Config.get("enterprises", enterprise_name)
    print "Workflow request received. " + workflow_parser \
        + " will parse this fucking request from " + enterprise_name
    if (workflow_parser == 'twitter'):
        return twitter_listener()
    elif (workflow_parser == 'fari'):
        return twitter_listener
    else:
        return 500


def get_enterprise_name(tasks):
    # client request vapp
    vm_url = ""
    for link in tasks['collection'][0]['links']:
        if link['rel'] == 'target':
            vm_url = link['href']
            break
    print "http://%s/api/%s" % ("10.60.1.245", vm_url)
    vm_response = client.get("http://%s/api/%s" % ("10.60.1.245", vm_url),
                             auth=('admin', 'xabiquo'))

    vm_dto = json.loads(vm_response.text)

    for link in vm_dto['links']:
        if link['rel'] == 'enterprise':
            #TODO if fails
            return link['title']


def parse_request(request):
    if TASKS_CONTENT_TYPE == request.headers['content-type']:
        dto = json.loads(request.data)
        execute_workflow(dto)
    elif TASK_CONTENT_TYPE == request.headers['content-type']:
        dto = json.loads(request.data)
        execute_workflow([dto])
        return Response(status=200)
    else:
        return Response(status=415)

if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)
