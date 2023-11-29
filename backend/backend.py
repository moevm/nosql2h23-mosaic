from flask import Flask, request, jsonify
from time import time

datas = ["pic1", "pic2", "pic3", "pic4","pic5"]




app = Flask(__name__)

@app.route("/api")
@app.route("/api/get_picks/")
def api_get_picks():
    data = {
        "total": len(datas),
        "names": datas
    }

    response =jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response, 200

if __name__ == "__main__":
    app.run(debug=True)