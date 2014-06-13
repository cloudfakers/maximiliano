from flask import Flask, request
from random import randint
import ConfigParser
import os


app = Flask(__name__)
# initialization process
Config = ConfigParser.ConfigParser()
Config.read(os.path.abspath(os.path.dirname(__file__)) + "/config/maximiliano.conf")
print Config.sections()


@app.route("/", methods=["GET"])
def listen():    
	print "Root received request %s" % str(request)	
	task = 'FAKE, Sergi will process this shit'
	return execute_workflow(task)

'''
Will receive a list of tasks (VM if only one)
'''
def execute_workflow(task):
	print "Root received task list %s" % str(task)

	# Parsear enterprise name	
	
	print Config.get("enterprises", get_enterprise_name())
	return 500

def get_enterprise_name():
	print "FAKE"

@app.route("/twitter", methods=["GET"])
def twitter_listener():    
    return "Twitter will process this request %s" % str(request)    

@app.route("/fari", methods=["GET"])
def fari_listener():
    return "El FARI will process this request %s" % str(request)        

if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)
