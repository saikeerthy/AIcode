from flask import Flask, jsonify, request

app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
