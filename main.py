from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


class Welcome(Resource):
    def get(self):
        return "Welcome to the LLM Service"


api.add_resource(Welcome, "/api")

if __name__ == "__main__":
    app.run(debug=True)
