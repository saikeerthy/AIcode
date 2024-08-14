from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # change this!
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

def role_required(role):
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            current_user = User.query.filter_by(username=get_jwt_identity()).first()
            if not current_user or current_user.role != role:
                abort(403)  # forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/items', methods=['GET'])
@role_required('admin')
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
@role_required('admin')
def create_item():
    new_item = request.get_json(force=True, silent=True)
    if not new_item or 'name' not in new_item or 'value' not in new_item:
        abort(400)  # bad request
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
