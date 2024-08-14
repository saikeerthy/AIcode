from flask import Flask, jsonify, request
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: request.remote_addr)

items = []

@app.route('/items', methods=['GET'])
@limiter.limit("100/day;10/hour;1/minute")
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
@limiter.limit("100/day;10/hour;1/minute")
def create_item():
    new_item = request.get_json()
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
