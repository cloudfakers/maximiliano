from flask import Flask, request, Response
from config import Config
import json
import requests as client

TASKS_CONTENT_TYPE = "application/vnd.abiquo.tasks+json"
TASK_CONTENT_TYPE = "application/vnd.abiquo.task+json"

app = Flask(__name__)
config = Config()


@app.route("/", methods=["POST"])
def listen():
    return parse_request(request)


# @app.route("/twitter", methods=["POST"])
def twitter_listener(tasks):
    for task in tasks:
        continue_task(task)
    return "Twitter will process this request %s" % str(request)


# @app.route("/fari", methods=["POST"])
def fari_listener(tasks):
    for task in tasks:
        cancel_task(task)
    return "El FARI will process this request %s" % str(request)


def execute_workflow(tasks):
    """
    Will receive a list of tasks (VM if only one)
    """
    # Parsear enterprise name
    enterprise_name = get_enterprise_name(tasks)
    workflow_parser = config.get("enterprises", enterprise_name)
    if workflow_parser == 'twitter':
        return twitter_listener(tasks)
    elif workflow_parser == 'fari':
        return fari_listener(tasks)
    else:
        return 500


def get_enterprise_name(tasks):
    # client request vapp
    vm_url = None
    for link in tasks[0]['links']:
        if link['rel'] == 'target':
            vm_url = link['href']
            break
    vm_response = client.get("%s/%s" %
                             (config.api_endpoint, vm_url),
                             auth=(config.api_user, config.api_password))

    vm_dto = json.loads(vm_response.text)

    for link in vm_dto['links']:
        if link['rel'] == 'enterprise':
            # TODO if fails
            return link['title']
    raise Exception("No enterprise link found")


def continue_task(task):
    client.post("%s/%s" % (config.api_endpoint,
                           __get_action_href('continue', task)),
                data="continue please",
                auth=(config.api_user, config.api_password))


def cancel_task(task):
    client.post("%s/%s" % (config.api_endpoint,
                           __get_action_href('cancel', task)),
                data="continue please",
                auth=(config.api_user, config.api_password))


def parse_request(request):
    """
    Checks if a request is valid to start a workflow (200) or no (415)
    """
    if request.headers['content-type'].startswith(TASKS_CONTENT_TYPE):
        dto = json.loads(request.data)
        print execute_workflow(dto['collection'])
        return Response(status=200)
    elif request.headers['content-type'].startswith(TASK_CONTENT_TYPE):
        dto = json.loads(request.data)
        print execute_workflow([dto])
        return Response(status=200)
    else:
        return Response(status=415)


def __get_action_href(name, task):
    for link in task['links']:
        if link['rel'] == name:
            return link['href']


if __name__ == "__main__":
    host = config.get("config", "host")
    port = int(config.get("config", "port"))
    app.run(host=host, port=port, debug=True)
