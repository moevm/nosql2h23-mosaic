from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import json
from time import time, sleep
from datetime import datetime
from random import randint as rnd
import img2mosaic


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
    
    def addNewMosaic(self, email_str, pic, title_str, blockSize, colors, timest=time()):
        with self.driver.session() as session:
            print(">>>In neo4j::addNewMosaic")
            if len(list(session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) WHERE m.title = $title return m", email=email_str, title=title_str))):
                return False
            result = session.run("MATCH (u:User) WHERE u.email = $email CREATE (m:Mosaic {picture: $picture, title: $title, blockSize:$blockSize, colors:$colors, creation_timestamp: $timest}) CREATE (m)-[:OWNED_BY]->(u)", picture=pic, title=title_str, blockSize=blockSize, colors=colors, timest=timest, email=email_str)
            return True
    
    def constructMosaic(self, title, pixelSize, colors, email):
        with self.driver.session() as session:
            result = list(session.run("MATCH (u:User) WHERE u.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(u) WHERE m.title = $title return m", email=email, title=title))
            print(result)
            imgBase64 = result[0][0].get("picture")
            index = imgBase64.find('base64,')
            imgBase64 = imgBase64[index+7:]
            pixels = img2mosaic.convert(imgBase64, pixelSize, colors)
            
            for y, row in enumerate(pixels):
                for x, rgb in enumerate(row):
                    session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) WHERE m.title = $title CREATE (t:Tile {x: $x, y: $y, r: $r, g: $g, b: $b}) CREATE (t)-[:INCLUDED_BY]->(m)", email=email, title=title, x=x, y=y, r=rgb[0], g=rgb[1], b=rgb[2])
    
    def getMosaicTiles(self, title, email):
        with self.driver.session() as session:
            result = list(session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) WHERE m.title = $title MATCH (t:Tile)-[:INCLUDED_BY]->(m) return t", title=title, email=email))
            return result
    def getAllMosaics(self, email_str):
        with self.driver.session() as session:
            result = session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) return m", email=email_str)
            
            return list(result)
    
    def getJSONForMosaic(self, title, email):
        with self.driver.session() as session:
            data = {}
            result = list(session.run("MATCH (n:User) WHERE n.email = $email MATCH (m:Mosaic)-[:OWNED_BY]->(n) WHERE m.title = $title return m", email=email, title = title))
            
            print(type(result[0]))
            #print(result[0].get('m.blockSize'))
            data['blockSize'] = result[0][0].get('blockSize')
            data['colors'] = result[0][0].get('colors')
            data['creation_timestamp'] = result[0][0].get('creation_timestamp')
            data['picture'] = result[0][0].get('picture')
            data['title'] = result[0][0].get('title')
            
            records = self.getMosaicTiles(title, email)
            
            tiles = []

            for record in records:
                tiles.append({
                    "x": record["t"].get("x"),
                    "y": record["t"].get("y"),
                    "r": record["t"].get("r"),
                    "g": record["t"].get("g"),
                    "b": record["t"].get("b"),
                })

            data['tiles'] = tiles

            return data
    
    def getAllMosaicsJSON(self, email):
        with self.driver.session() as session:

            all_data = {}
            titles = []

            results = list(session.run('MATCH (u:User) WHERE u.email=$email MATCH (m:Mosaic)-[:OWNED_BY]->(u) return m', email=email))
            for result in results:
                titles.append(result[0].get('title'))
            
            print(len(titles))

            for i in range(len(titles)):
                all_data[f'Mosaic{i}'] = self.getJSONForMosaic(titles[i])
            
            return all_data

    def loadAllMosaicsFromJSON(self, email, file):
        with self.driver.session() as session:
            data = json.loads(file)

            for i in range(len(data)):

                colors = data[f'Mosaic{i}']['colors']
                blockSize = data[f'Mosaic{i}']['blockSize']
                title = data[f'Mosaic{i}']['title']
                creation_timestamp = data[f'Mosaic{i}']['creation_timestamp']
                picture = data[f'Mosaic{i}']['picture']
                tiles = data[f'Mosaic{i}']['tiles']

                self.addNewMosaic(email, picture, title, blockSize, colors, creation_timestamp)
            
            for tile in tiles:
                session.run("MATCH (u:User) WHERE u.email=$email MATCH (m:Mosaic)-[:OWNED_BY]->(u) WHERE m.title = $title CREATE (t:Tile {x: $x, y: $y, r: $r, g: $g, b: $b}) CREATE (t)-[:INCLUDED_BY]->(m)", email=email, title=title, x=tile['x'], y=tile['y'], r=tile['r'], g=tile['g'], b=tile['b'])
    
    def deleteMosaicByTitle(self, title_str):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Mosaic) WHERE m.title = $title DETACH DELETE (m)", title=title_str)


db_started = False
st = time()

while not db_started:
    try:
        db = neo4j("bolt://db:7687", "neo4j", "password")
        db_started = True
    except:
        db_started = False
        print(f"Waiting for db to start: {round(time()-st, 2)} sec")
    
    sleep(0.2)

def generate_token():
    symset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890_="

    token = ""
    
    for i in range(16):
        token += symset[rnd(1,len(symset))-1]
    
    return token



datas = ["pic1", "pic2", "pic3", "pic4","pic5"]
tokens = [('0','peter')]



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
@app.route("/api/get_mosaic", methods=['GET','POST'])
def api_get_mosaic():
    if request.method == "POST":

        
        user = findUserByToken(tokens, request.form["token"])

        records = db.getMosaicTiles(request.form["title"], user)


        tiles = []
        
        
        for record in records:
            tiles.append({
                "x": record["t"].get("x"),
                "y": record["t"].get("y"),
                "r": record["t"].get("r"),
                "g": record["t"].get("g"),
                "b": record["t"].get("b"),
            })
        
        data = {"tiles": tiles}
        
        print(data)

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
            colors = []
            blockSizes = []
            progresses = []
            
            #print(records[0].keys())
            
            for record in records: #'m' is a local variable in CYPHER neo4j query
                picture_titles.append(record["m"].get("title"))
                timestamps.append(datetime.fromtimestamp(record["m"].get("creation_timestamp")))
                pictures.append(record["m"].get("picture"))
                colors.append(record["m"].get("colors"))
                blockSizes.append(record["m"].get("blockSize"))
                progresses.append("100%")
            
            data = {"titles": picture_titles, "timestamps":timestamps, "pictures": pictures, "colors": colors, "blockSizes": blockSizes, "progresses":progresses}
            
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
            colors = 256
            blockSize = 10
            result = db.addNewMosaic(user, picture, title, blockSize, colors)
            db.constructMosaic(title, blockSize, colors, user)
            
            if result:
                response = jsonify("OK")
                response.headers.add('Access-Control-Allow-Origin', '*')
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


"""@app.route("/api")
@app.route("/api/jsontest", methods=['GET','POST'])
def api_jsontest():
    if request.method == "POST":
        title = request.form["title"]
        
        response = jsonify(db.getJSONForMosaic(title))

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200"""

@app.route("/api")
@app.route("/api/exporter", methods=['GET','POST'])
def api_jsontestall():
    if request.method == "POST":

        token = request.form['token']
        user = findUserByToken(tokens, token)

        response = jsonify(db.getAllMosaicsJSON(user))

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200


if __name__ == "__main__":
    app.run(debug=True, port = 5001, host='0.0.0.0')
    db.close()
    