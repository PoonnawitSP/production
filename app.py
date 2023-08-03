from flask import Flask,  request, jsonify, render_template
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from pymongo import MongoClient
import certifi
import models


app = Flask(__name__, static_folder = './build', static_url_path='/')

projectId = 0
name = ""

file_path = 'mongoDBuri.txt' 
with open(file_path, 'r') as file:
    data = file.read()


app.config['MONGO_URI'] = data
mongo = PyMongo(app)
client = MongoClient(data, tlsCAFile=certifi.where())
db = client.APAD_app
CORS(app)

@app.route('/')
def Home():
    return app.send_static_file('index.html')

@app.route('/signIn', methods=['POST'])
def signIn():
    return models.user().userSignIn()

@app.route('/createNewUser', methods=['POST'])
def createNewUser():
    return models.user().createNewUser()

@app.route('/createNewProject', methods=['POST'])
def createNewProject():
    return models.project().createProject()

@app.route('/login', methods=['POST'])
def projectLogin():
    return models.project().projectLogin()

@app.route('/getWebCam_Capacity', methods=['GET'])
def getWebCam_Capacity():
    return models.dashboard().getWebCam_Capacity()

@app.route('/getHeadset_Capacity', methods=['GET'])
def getHeadset_Capacity():
    return models.dashboard().getHeadset_Capacity()

@app.route('/getHeadset_Availability', methods=['GET'])
def getHeadset_Availability():
    return models.dashboard().getHeadsetAvailability()

@app.route('/getWebcam_Availability', methods=['GET'])
def getWebcam_Availability():
    return models.dashboard().getWebcamAvailability()

@app.route('/checkout', methods=['POST'])
def checkout():
    return models.dashboard().checkout()

@app.route('/checkin', methods=['POST'])
def checkin():
    return models.dashboard().checkin()

@app.route('/getdetails', methods=['GET'])
def getdetails():
    return models.dashboard().getdetails()

@app.route('/getmembers', methods=['GET'])
def getmembers():
    return models.dashboard().getmembers()

@app.route('/getsignin', methods=['GET'])
def getsignin():
    return models.project().getsignin()

@app.route('/logout', methods=['GET'])
def logout():
    return models.user().logout()

if __name__ == '__main__':
    app.run(debug=True)