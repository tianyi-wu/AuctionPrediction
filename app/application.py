# coding:utf-8

from flask import (
    Flask,
    jsonify
)

import time

application = Flask(__name__)
application.config['STATIC_FOLDER'] = 'static'


@application.route('/predict/<string:auction_id>', methods=['GET'])
def predict(auction_id):
    time.sleep(1)
    return jsonify(value='100', minimum='50', maximum='150')


if __name__ == '__main__':
    application.run(debug=True)
