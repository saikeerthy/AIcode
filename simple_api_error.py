from flask import Flask, jsonify, request, abort

app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json(force=True, silent=True)
    if not new_item or 'name' not in new_item or 'value' not in new_item:
        abort(400)  # bad request
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
