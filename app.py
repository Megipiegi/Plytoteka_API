from flask import Flask, jsonify, abort, make_response, request
from models import plytoteka

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/plytoteka/", methods=["GET"])
def plytoteka_list_api_v1():
    return jsonify(plytoteka.all())


@app.route("/api/v1/plytoteka/<int:plyty_id>", methods=["GET"])
def get_plyty(plyty_id):
    plyty = plytoteka.get(plyty_id)
    if not plyty:
        abort(404)
    return jsonify({"plyty": plyty})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/plytoteka/", methods=["POST"])
def create_plyty():
    if not request.json or not 'wykonawca' in request.json:
        abort(400)
    plyty = {
        'id': plytoteka.all()[-1]['id'] + 1,
        'wykonawca': request.json['wykonawca'],
        'album': request.json.get('album', ""),
        'posiadam': False
    }
    plytoteka.create(plyty)
    return jsonify({'plyty': plyty}), 201


@app.route("/api/v1/plytoteka/<int:plyty_id>", methods=['DELETE'])
def delete_plyty(plyty_id):
    result = plytoteka.delete(plyty_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/plytoteka/<int:plyty_id>", methods=["PUT"])
def update_plyty(plyty_id):
    plyty = plytoteka.get(plyty_id)
    if not plyty:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'wykonawca' in data and not isinstance(data.get('wykonawca'), str),
        'album' in data and not isinstance(data.get('album'), str),
        'posiadam' in data and not isinstance(data.get('posiadam'), bool)
    ]):
        abort(400)
    plyty = {
        'wykonawca': data.get('wykonawca', plyty['wykonawca']),
        'album': data.get('album', plyty['album']),
        'posiadam': data.get('posiadam', plyty['posiadam']),
        'id': data.get('id', plyty['id'])
    }
    plytoteka.update(plyty_id, plyty)
    return jsonify({'plyty': plyty})


if __name__ == "__main__":
    app.run(debug=True)