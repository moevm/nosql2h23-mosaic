from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import json
from time import time
from random import randint as rnd


class neo4j:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(self.driver.verify_connectivity())

    def close(self):
        self.driver.close()
    
    def addNewAccount(self, email_str, password_str):
        with self.driver.session() as session:
            print()
            result = session.run("MATCH (n:User {email: $email}) RETURN n.email", email=email_str)
            result = list(result)
            
            if len(result) != 0:
                return -1
            
            summary = session.run("CREATE (:User {email: $email, password: $password})",email = email_str, password = password_str)
            return 0
    
    def checkAccountCredentials(self, email_str, password_str):
        with self.driver.session() as session:
            print(">>>In neo4j::checkAccountCredentials")
            result = session.run("MATCH (n:User {email: $email}) RETURN n.password", email=email_str)

            result = list(result)
            #print(result[0].get("n.password"))

            if len(result) != 0:
                if password_str == result[0].get("n.password"):
                    return True
                else:
                    return False
            else:
                return False
    
    def addNewMosaic(self, email, pic):
        pass

    def getAllMosaics(self, email):
        pass


db = neo4j("bolt://localhost:7687", "neo4j", "password")

def generate_token():
    symset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_="

    token = ""
    
    for i in range(16):
        token += symset[rnd(1,len(symset))-1]
    
    return token



datas = ["pic1", "pic2", "pic3", "pic4","pic5"]
tokens = []



app = Flask(__name__)

@app.route("/api")
@app.route("/api/get_picks")
def api_get_picks():

    data = {
        "total": len(datas),
        "names": datas
    }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response, 200


@app.route("/api")
@app.route("/api/user_profile")
def api_get_user_profile():

    data = {
        "total": len(datas),
        "names": datas
    }

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response, 200


@app.route("/api")
@app.route("/api/login", methods=['GET', 'POST'])
def api_login():
    if request.method == "POST":
        data = request.form
        print(data)
        email = data["email"]
        password = data["password"]


        success = db.checkAccountCredentials(email, password)

        if success:
            token = generate_token()
            response = {"token":token}
            response = jsonify(response)
            tokens.append((token, email))
        else:
            response = {"token":"0"}
            response = jsonify(response)

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200


@app.route("/api")
@app.route("/api/signup", methods=['GET', 'POST'])
def api_signup():
    if request.method == "POST":
        data = request.form
        print(data)
        email = data["email"]
        password = data["password"]

        success = db.addNewAccount(email, password)

        if success:
            response = "1"
        else:
            response = "0"

        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200


if __name__ == "__main__":
    app.run(debug=True, port = 5001)
    db.close()
    