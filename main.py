from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from controllers.recipify import recipify

app = Flask(__name__)
CORS(app)
api = Api(app)


class Welcome(Resource):
    def get(self):
        return "Welcome to the LLM Service"

class Recipify(Resource):
    def post(self):
        data = request.get_json()
        if 'recipe' in data:
            recipe = data['recipe']
            recipe_obj = recipify(recipe)
            print(recipe_obj)
            return jsonify({"recipe:": recipe_obj})


api.add_resource(Welcome, "/api")
api.add_resource(Recipify, "/api/recipe")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='3001',debug=True)
