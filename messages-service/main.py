from flask import Flask, jsonify

from utils import use_response_template


app = Flask('Message-service')


@app.route('/message-svc/api/v1.0/get_messages', methods=['GET'])
def get_messages():
    status = 200
    response = use_response_template(status=status, resp_msg="not implemented yet")
    return jsonify(response), status


@app.route('/message-svc/api/v1.0/post_messages', methods=['POST'])
def post_messages():
    status = 404
    response = use_response_template(status=status, resp_msg="POST request is not supported yet")
    return jsonify(response), status


if __name__ == '__main__':
    app.run(debug=True, port=8083)
