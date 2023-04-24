import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/sendjson', methods=['POST'])
def postJson():
    Signal = request.json
    save_file = open("savedsignal.json", "w")
    json.dump(Signal, save_file, indent=10)
    save_file.close()
    return Signal


@app.route('/getjson', methods=['GET'])
def getJson():
    with open('savedsignal.json', 'r') as openfile:
        obj = json.load(openfile)
        if(obj["signal"] == "peak"):
            return jsonify(1)
    return jsonify(0)


if __name__ == '__main__':
    app.run(debug=True)
