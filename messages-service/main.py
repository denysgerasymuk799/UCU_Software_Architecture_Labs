from flask import make_response, request, abort, Response
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/message-svc/api/v1.0/get_messages', methods=['GET'])
def get_messages():
    status = 200
    response = {
        "_status_code": status,
        "response": "not implemented yet"
    }
    return jsonify(response), status
    # return Response(response, 200)


@app.route('/message-svc/api/v1.0/post_messages', methods=['POST'])
def post_messages():
    # abort(Response('POST request is not supported yet', 304))
    status = 404
    response = {
        "_status_code": status,
        "response": "POST request is not supported yet"
    }
    return jsonify(response), status


if __name__ == '__main__':
    app.run(debug=True, port=8082)
