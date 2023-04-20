from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import os
from waitress import serve
from werkzeug.utils import secure_filename
from matching import mapMatching

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def home():
    return "Server is running"


@app.route('/getOutputs', methods=['GET'])
@cross_origin()
def get_outputs():
    return send_file(os.path.join(os.getcwd(), 'outputs.zip'), as_attachment=True)


@app.route('/gpx', methods=['POST'])
@cross_origin()
def getMatch():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(os.getcwd(), filename))
    res = mapMatching(filename=filename)
    return jsonify(res)


@app.route('/path', methods=['POST'])
@cross_origin()
def getPath():
    data = request.form.to_dict()
    coords = iter(data['coords'].split(','))
    arr = []
    for x in coords:
        arr.append([float(x), float(next(coords))])
    res = mapMatching(coords=arr)
    return jsonify(res)


def run_server():
    app.debug = True
    serve(app, host='0.0.0.0', port=5000, threads=1)


if __name__ == '__main__':
    run_server()
