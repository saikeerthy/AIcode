from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # change this!
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        abort(400)  # bad request
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

items = []

@app.route('/items', methods=['GET'])
@jwt_required
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
@jwt_required
def create_item():
    new_item = request.get_json(force=True, silent=True)
    if not new_item or 'name' not in new_item or 'value' not in new_item:
        abort(400)  # bad request
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
