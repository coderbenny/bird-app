import os


from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Bird

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        species = data.get('species')
        
        if not name or not species:
            return jsonify({"error":"Invalid data"}), 404
        
        new_bird = Bird(name=name,species=species)

        db.session.add(new_bird)
        db.session.commit()
        
        response = make_response(
            jsonify({"message":"Bird added succesfully", "bird": new_bird.to_dict()}), 
            200
        )
        
        return response
        
        db.session.rollback()
        return jsonify({"error":"An error occured"}), 400
        
api.add_resource(Birds, '/birds')

class BirdsByID(Resource):

    def get(self,id):
        bird = Bird.query.filter_by(id=id).first()
        if not bird:
            return jsonify({"error":"bird does not exist"}), 404
        response = make_response(
            jsonify(bird.to_dict()),
            200
        )
        
        return response

api.add_resource(BirdsByID, '/birds/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)