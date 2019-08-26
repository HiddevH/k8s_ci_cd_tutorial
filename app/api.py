from flask import Flask, jsonify
from flask_restful import Resource, Api
import sys
import optparse
import time

app = Flask(__name__)
api = Api(app)

start = int(round(time.time()))

class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello World'})

class Test(Resource):
    def get(self):
        return jsonify({'test': 'test'})

api.add_resource(HelloWorld, '/helloworld') # Route_1
api.add_resource(Test, '/test') # Route_2
# api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="python api.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(port=int(args.port), debug=False)
