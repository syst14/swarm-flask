from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import sys
import optparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qwe14@localhost:3306/mysql'
db = SQLAlchemy(app)
ma = Marshmallow(app)
db_status = 'BAD'

class Sneakers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), unique=False)
    model = db.Column(db.String(80), unique=True)

    def __init__(self, brand, model):
        self.brand = brand
        self.model = model


class SneakersSchema(ma.Schema):
    class Meta:
        fields = ('brand', 'model')

try:
    all = Users.query.all()
    db_status = 'OK'
except Exception as e:
    try:
        db.create_all()
        db_status = 'OK'
    except Exception as e:
        pass


sneaker_schema = SneakersSchema()
sneakers_schema = SneakersSchema(many=True)

@app.route("/status", methods=["GET"])
def status():
    return "APP - OK; DB - " + db_status

@app.route("/sneakers", methods=["GET"])
def get_sneakers():
    all_sneakers = Sneakers.query.all()
    res = sneakers_schema.dump(all_sneakers)
    return jsonify(res.data)

@app.route("/sneakers", methods=["POST"])
def add_sneakers():
    data = request.get_json()
    brand = data['brand']
    model = data['model']
    
    new_sneakers = Sneakers(brand, model)

    db.session.add(new_sneakers)
    db.session.commit()
    return '200 OK'


@app.route("/sneakers/<id>", methods=["GET"])
def sneakers_detail(id):
    sneakers = Sneakers.query.get(id)
    return sneaker_schema.jsonify(sneakers)


@app.route("/sneakers/<id>", methods=["PUT"])
def sneakers_update(id):
    data = request.get_json()
    sneakers = Sneakers.query.get(id)
    brand = data['brand']
    model = data['model']

    sneakers.brand = brand
    sneakers.model = model

    db.session.commit()
    return '200 OK'


@app.route("/sneakers/<id>", methods=["DELETE"])
def sneakers_delete(id):
    sneakers = Sneakers.query.get(id)

    db.session.delete(sneakers)
    db.session.commit()
    return '200 OK'


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python main.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print "Missing required argument: -p/--port"
        sys.exit(1)

    app.run(host='0.0.0.0', port=int(args.port), debug=True)
