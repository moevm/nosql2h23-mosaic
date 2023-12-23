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
            
            result = session.run("CREATE (:User {email: $email, password: $password})",email = email_str, password = password_str)
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
    
    def addNewMosaic(self, email_str, pic, title_str):
        with self.driver.session() as session:
            print(">>>In neo4j::addNewMosaic")
            if len(list(session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) WHERE m.title = $title return m", email=email_str, title=title_str))):
                return False
            result = session.run("CREATE (m:Mosaic {picture: $picture, title: $title, creation_timestamp: $timest}) MATCH (u:User) WHERE u.email = $email CREATE (m)-[:OWNED_BY]->(u)", picture=pic, title=title_str, timest=time(), email=email_str)
            return True


    def getAllMosaics(self, email_str):
        with self.driver.session() as session:
            result = session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) return m", email=email_str)
            
            return list(result)
    
    def deleteMosaicByTitle(self, title_str):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Mosaic) WHERE m.title = $title DETACH DELETE (m)", title=title_str)


db = neo4j("bolt://localhost:7687", "neo4j", "password")

def generate_token():
    symset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_="

    token = ""
    
    for i in range(16):
        token += symset[rnd(1,len(symset))-1]
    
    return token



datas = ["pic1", "pic2", "pic3", "pic4","pic5"]
tokens = []



def findUserByToken(tokens, token):
    print(">>> In findUserByToken")
    print(tokens)
    for i in tokens:
        if i[0] == token:
            return i[1]
    
    return False


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
@app.route("/api/user_profile", methods=['GET','POST'])
def api_get_user_profile():
    if request.method == "POST":
        user = findUserByToken(tokens, request.form["token"])

        if user:
            records = db.getAllMosaics(user)

            #print(records)

            picture_titles = []
            timestamps = []
            pictures = []
            
            #print(records[0].keys())
            
            for record in records: #'m' is a local variable in CYPHER neo4j query
                picture_titles.append(record["m"].get("title"))
                timestamps.append(record["m"].get("creation_timestamp"))
                pictures.append(record["m"].get("picture"))
            
            data = {"titles": picture_titles, "timestamps":timestamps, "pictures": pictures}
            
            #print(data)

            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')

            return response, 200
    
    response = "FAIL"
    return response, 500
        

@app.route("/api")
@app.route("/api/add_picture", methods=['GET','POST'])
def api_add_picture():
    if request.method == "POST":
        token = request.form["token"]
        picture = request.form["picture"]
        title = request.form["title"]
        
        user = findUserByToken(tokens, token)

        if user:
            result = db.addNewMosaic(user, picture, title)
            
            if result:
                response = "OK"
                return response, 200
            else:
                response = "FAIL"
                return response, 400




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
    