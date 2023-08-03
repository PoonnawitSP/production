from flask import Flask,  request, jsonify, render_template
import uuid
from app import db, projectId, name
import bcrypt

class user:
   
   def userSignIn(self):
    
      flag = 0
      userdetails = {
          'email' : request.json['email'],
          'password' : request.json['password'],
      } 
      #userdetails['password'] = (bcrypt.hashpw(userdetails['password'].encode('utf-8'), bcrypt.gensalt())).decode('utf-8')  
      #userdetails['password'] = (f.encrypt(userdetails['password'].encode()))     
      for document in db.users.find():
          email = document["email"]
          password = document["password"]
          a = document["email"] == userdetails['email']
          b = bcrypt.checkpw(userdetails['password'].encode('utf-8'), document["password"])
          if(document["email"] == userdetails['email'] and bcrypt.checkpw(userdetails['password'].encode('utf-8'), document["password"])):
            global name 
            name = document["email"]
            flag+=1
            return jsonify({'msg': "SignIn succcessful"})
      #if db.users.find_one({"email": userdetails['email'], "password": userdetails['password']}):
        #flag+=1
        #return jsonify({'msg': "SignIn succcessful"})
            
      if flag == 0:
        return jsonify({'error': "invalid email id or password"}), 500
      

   def createNewUser(self):
    
        confirmPassword = request.json['confirmPassword']
        newUser = {
            '_id': uuid.uuid4().hex,
            'firstName' : request.json['firstName'],
            'lastName' : request.json['lastName'],
            'preferredName' : request.json['preferredName'],
            'email' : request.json['email'],
            'contact' : request.json['contact'],
            'password' : request.json['password'],       
        }  
        
        if(db.users.find_one({ "email": newUser['email']})):  

            return jsonify({'error': "Email id already exists please try signing or use another email"}), 500
    
        else:
            if(newUser['password'] == confirmPassword):

                #newUser['password'] = (f.encrypt(newUser['password'].encode()))  
                newUser['password'] = (bcrypt.hashpw(newUser['password'].encode('utf-8'), bcrypt.gensalt()))

                if db.users.insert_one(newUser):
                    global name
                    name = newUser["email"]
                    return jsonify({'msg': "User Added Successfully"})     
                else:
                    return jsonify({'error': "error creating new user"})
            else:
                return jsonify({'error': "Both the passwords are not matching"}), 400
            
            
   def logout(self) :
               
        global projectId
        projectId = 0
        global name 
        name = ""
        return jsonify({'msg': "logout successfull"}) 


class project:

    def projectLogin(self):
        flag = 0
        projectDetails = {
          'projectName' : request.json['projectName'],
          'projectId' : request.json['projectId'],
        }  

        members = [] 

        if(name == "") :
            return jsonify({'error': "Please login first to login to a project"}), 400

        result = db.projects.find_one({"projectName": projectDetails['projectName'], "projectId": projectDetails['projectId']})  
            
        if result:
            if "members" in result :
                db.projects.update_one({'_id': result["_id"]}, {'$addToSet': {"members": name}})
            else :
                members.append(name)
                db.projects.update_one({'_id': result["_id"]},{'$set' : {"members" : members}})
            flag+=1
            global projectId
            projectId = result["_id"]
            return jsonify({'msg': "Login succcessful"})
            
        if flag == 0:
            return jsonify({'error': "invalid project name or project id"}), 500

       
    def createProject(self):
       newProject = {
          '-id': uuid.uuid4().hex,
          'projectName': request.json['projectName'],
          'projectId': request.json['projectId'],
          'description': request.json['description']
       }
       members = []
       if(name == "") :
            return jsonify({'error': "Please login first to create new peoject"}), 400
       if(db.projects.find_one({"projectId": newProject['projectId']})):
           return jsonify({'error': "Project Id Aready Exists use different Project Id"}), 500
       
       if db.projects.insert_one(newProject):
            result = db.projects.find_one({"projectName": newProject['projectName'], "projectId": newProject['projectId']})
            members.append(name)
            db.projects.update_one({'_id': result["_id"]},{'$set' : {"members" : members}})
            if result:
                global projectId
                projectId = result["_id"]       
            return jsonify({'msg': "Project Added Successfuly"})
       else:
            return jsonify({'error': "Error creating project"})
       

    def getsignin(self):

        if name == "" :
            return jsonify({'error': "Not signed in"}), 400

        else :
            return jsonify({'msg': "signed in"}), 200

       


class dashboard:

    def getWebCam_Capacity(self):
       
        capacity_webcam = 100
            #'capacity_headset': 100
        

        result = db.fixed_values.find_one({"capacity_webcam": {"$exists": True}})
        if result:
            capacity_webcam = result["capacity_webcam"]
       
        return jsonify({"value": capacity_webcam})
    
    def getHeadset_Capacity(self):

        capacity_headset = 100

        result = db.fixed_values.find_one({"capacity_headset": {"$exists": True}})
        if result:
            capacity_headset = result["capacity_headset"]
       
        return jsonify({"value": capacity_headset})
    
    def getWebcamAvailability(self):

        result = db.Availability.find_one({"webcam": {"$exists": True}})
        if result:
            availability_webcam = result["webcam"]
       
        return jsonify({"value": availability_webcam})
    

    def getHeadsetAvailability(self):

        result = db.Availability.find_one({"headset": {"$exists": True}})
        if result:
            availability_headset = result["headset"]
       
        return jsonify({"value": availability_headset})
    
    def getdetails(self):

        response = {
            "projectId" : "",
            "checkout_webcam": "",
            "checkout_headset": ""
        }

        if projectId == 0 :
            return jsonify({'error': "Not signed in"}), 400
        else :
            project_id = db.projects.find_one({"_id": projectId})
            if project_id :
                response["projectId"] = project_id["projectId"]
                if "headset" in project_id :
                    response["checkout_headset"] = project_id["headset"]
                if "webcam" in project_id :
                    response["checkout_webcam"] = project_id["webcam"]
                return jsonify({"value": response})
            else :
                return jsonify({"value": response})
            
    

    def getmembers(self) :

        project_id = db.projects.find_one({"_id": projectId})
        if project_id :
            if "members" in project_id :
                members = project_id["members"]
                return jsonify(members)
            else :
                return jsonify("not logged in")

    def checkout(self):
        
        HardwareSets = {
          'headset' : request.json['headset'],
          'webcam' : request.json['webcam'],
        }  

        if HardwareSets['headset'] != "" and (HardwareSets['webcam'] == None or HardwareSets['webcam'] == ""):
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            
            if result_headset:
                if int(HardwareSets['headset']) > result_headset["headset"] :
                    return jsonify({'error': "You have rquested for more items than available. Please request items within availability"}), 500
                else :
                    new_headset = result_headset["headset"] - int(HardwareSets['headset'])
                    id = {'_id' : result_id["_id"]}
                    values = {'$set' : {"headset" : new_headset}}
                    db.Availability.update_one(id, values)
                    project_id = db.projects.find_one({"_id": projectId})
                    if project_id : 
                        if "headset" in project_id :
                            update_headset = project_id["headset"] + int(HardwareSets["headset"])
                            UpdateHeadset = {'$set' : {"headset" : update_headset}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateHeadset)
                        else :
                            update_headset = int(HardwareSets["headset"])
                            UpdateHeadset = {'$set' : {"headset" : int(HardwareSets["headset"])}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateHeadset)
                        
                        if "webcam" in project_id :
                            update_webcam = project_id["webcam"]
                        else :
                            update_webcam = ""
                    else :
                        return jsonify({'error': "Please login first to checkout"}), 300

                    response = {

                            "headset" : new_headset,
                            "webcam" : result_webcam["webcam"],
                            "checkout_headset" : update_headset,
                            "checkout_webcam" : update_webcam
                    }
                    return jsonify({"value": response, "msg": "Succesfull"}), 200
            else :
                return jsonify({'error': "Error checking out"}), 400



        elif HardwareSets['webcam'] != "" and (HardwareSets['headset'] == None or HardwareSets['headset'] == ""):
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            
            if result_webcam:
                if int(HardwareSets['webcam']) > result_webcam["webcam"] :
                    return jsonify({'error': "You have rquested for more items than available. Please request items within availability"}), 500
                else :
                    new_webcam = result_webcam["webcam"] - int(HardwareSets['webcam'])
                    id = {'_id' : result_id["_id"]}
                    values = {'$set' : {"webcam" : new_webcam}}
                    db.Availability.update_one(id, values)
                    project_id = db.projects.find_one({"_id": projectId})
                    if project_id : 
                        if "webcam" in project_id :
                            update_webcam = project_id["webcam"] + int(HardwareSets["webcam"])
                            UpdateWebcam = {'$set' : {"webcam" : update_webcam}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateWebcam)
                        else :
                            update_webcam = int(HardwareSets["webcam"])
                            UpdateWebcam = {'$set' : {"webcam" : int(HardwareSets["webcam"])}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateWebcam)

                        if "headset" in project_id :
                            update_headset = project_id["headset"]
                        else :
                            update_headset = ""

                    else :        
                        return jsonify({'error': "Please login first to checkout"}), 300

                    response = {

                            "headset" : result_headset["headset"],
                            "webcam" : new_webcam,
                            "checkout_webcam" : update_webcam,
                            "checkout_headset" : update_headset
                    }

                    return jsonify({"value": response, "msg": "Succesfull"}), 200
            else :
                return jsonify({'error': "Error checking out"}), 400




        elif HardwareSets['webcam'] != "" and HardwareSets['headset'] != "" :
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            
            if result_headset and result_webcam:
                if int(HardwareSets['webcam']) > result_webcam["webcam"] and int(HardwareSets['headset']) > result_headset["headset"]:
                    return jsonify({'error': "You have rquested for more items than available. Please request items within availability"}), 500
                else :
                    new_webcam = result_webcam["webcam"] - int(HardwareSets['webcam'])
                    new_headset = result_headset["headset"] - int(HardwareSets['headset'])
                    id = {'_id' : result_id["_id"]}
                    values = {'$set' : {"webcam" : new_webcam, "headset" : new_headset}}
                    db.Availability.update_one(id, values)
                    project_id = db.projects.find_one({"_id": projectId})
                    if project_id : 
                        if "webcam" in project_id :
                            update_webcam = project_id["webcam"] + int(HardwareSets["webcam"])
                            UpdateWebcam = {'$set' : {"webcam" : update_webcam}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateWebcam)
                        else :
                            update_webcam = int(HardwareSets["webcam"])
                            UpdateWebcam = {'$set' : {"webcam" : int(HardwareSets["webcam"])}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateWebcam)


                        if "headset" in project_id :
                            update_headset = project_id["headset"] + int(HardwareSets["headset"])
                            UpdateHeadset = {'$set' : {"headset" : update_headset}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateHeadset)
                        else :
                            update_headset = int(HardwareSets["headset"])
                            UpdateHeadset = {'$set' : {"headset" : int(HardwareSets["headset"])}}
                            id_update = {'_id' : project_id["_id"]}
                            db.projects.update_one(id_update, UpdateHeadset)
                    else :
                        return jsonify({'error': "Please login first to checkout"}), 300


                    response = {

                            "headset" : new_headset,
                            "webcam" : new_webcam,
                            "checkout_webcam" : update_webcam,
                            "checkout_headset" : update_headset
                    }

                    return jsonify({"value": response, "msg": "Succesfull"}), 200
            else :
                return jsonify({'error': "Error checking out"}), 400

        else :
            return jsonify({'error': "Error Checking out"}), 400    
        
         
    def checkin(self):    

        HardwareSets = {
          'headset' : request.json['headset'],
          'webcam' : request.json['webcam'],
        }  

        if HardwareSets['headset'] != "" and (HardwareSets['webcam'] == None or HardwareSets['webcam'] == ""):
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            project_id = db.projects.find_one({"_id": projectId})
            if project_id : 
                if "headset" in project_id :
                    if int(HardwareSets["headset"]) > project_id["headset"]:
                        return jsonify({'error': "You are trying to checkin more than you have checkedout"}), 400
                    else :
                        new_headset = result_headset["headset"] + int(HardwareSets['headset'])
                        id = {'_id' : result_id["_id"]}
                        values = {'$set' : {"headset" : new_headset}}
                        db.Availability.update_one(id, values)

                        update_headset = project_id["headset"] - int(HardwareSets["headset"])
                        UpdateHeadset = {'$set' : {"headset" : update_headset}}
                        id_update = {'_id' : project_id["_id"]}
                        db.projects.update_one(id_update, UpdateHeadset)

                        if "webcam" in project_id:
                            update_webcam = project_id["webcam"]
                        else :
                            update_webcam = ""

                        response = {

                            "headset" : new_headset,
                            "webcam" : result_webcam["webcam"],
                            "checkout_webcam" : update_webcam,
                            "checkout_headset" : update_headset
                        }

                        return jsonify({"value": response, "msg": "Succesfull"}), 200
                
                else :
                    return jsonify({'error': "The field you are requesting to checkin has not been checkedout by your project"}), 500
                
            else :
                return jsonify({'error': "Please login first to checkin"}), 300
        
        
        elif HardwareSets['webcam'] != "" and (HardwareSets['headset'] == None or HardwareSets['headset'] == ""):
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            project_id = db.projects.find_one({"_id": projectId})
            if project_id : 
                if "webcam" in project_id :
                    if int(HardwareSets["webcam"]) > project_id["webcam"]:
                        return jsonify({'error': "You are trying to checkin more than you have checkedout"}), 400
                    else :
                        new_webcam = result_webcam["webcam"] + int(HardwareSets['webcam'])
                        id = {'_id' : result_id["_id"]}
                        values = {'$set' : {"webcam" : new_webcam}}
                        db.Availability.update_one(id, values)

                        update_webcam = project_id["webcam"] - int(HardwareSets["webcam"])
                        Update = {'$set' : {"webcam" : update_webcam}}
                        id_update = {'_id' : project_id["_id"]}
                        db.projects.update_one(id_update, Update)

                        if "headset" in project_id :
                            update_headset = project_id["headset"]
                        else :
                            update_headset = ""

                        response = {

                            "headset" : result_headset["headset"],
                            "webcam" : new_webcam,
                            "checkout_webcam" : update_webcam,
                            "checkout_headset" : update_headset
                        }

                        return jsonify({"value": response, "msg": "Succesfull"}), 200
            
                else :
                    return jsonify({'error': "The field you are requesting to checkin has not been checkedout by your project"}), 500

            else :
                return jsonify({'error': "Please login first to checkin"}), 300
            
        elif HardwareSets['webcam'] != "" and HardwareSets['headset'] != "":
            result_headset = db.Availability.find_one({"headset": {"$exists": True}})
            result_webcam = db.Availability.find_one({"webcam": {"$exists": True}})
            result_id = db.Availability.find_one({"_id": {"$exists": True}})
            project_id = db.projects.find_one({"_id": projectId})
            if project_id : 
                if "webcam" in project_id and "headset" in project_id:
                    if int(HardwareSets["webcam"]) > project_id["webcam"] or int(HardwareSets["headset"]) > project_id["headset"]:
                        return jsonify({'error': "You are trying to checkin more than you have checkedout"}), 400
                    else :
                        new_webcam = result_webcam["webcam"] + int(HardwareSets['headset'])
                        new_headset = result_headset["headset"] + int(HardwareSets['headset'])
                        id = {'_id' : result_id["_id"]}
                        values = {'$set' : {"webcam" : new_webcam, "headset": new_headset}}
                        db.Availability.update_one(id, values)

                        update_webcam = project_id["webcam"] - int(HardwareSets["webcam"])
                        update_headset = project_id["headset"] - int(HardwareSets["headset"])
                        Update = {'$set' : {"webcam" : update_webcam, "headset": update_headset}}
                        
                        id_update = {'_id' : project_id["_id"]}
                        db.projects.update_one(id_update, Update)

                        response = {

                            "headset" : new_headset,
                            "webcam" : new_webcam,
                            "checkout_webcam" : update_webcam,
                            "checkout_headset" : update_headset
                        }

                        return jsonify({"value": response, "msg": "Succesfull"}), 200
            
                else :
                    return jsonify({'error': "The field you are requesting to checkin has not been checkedout by your project"}), 500

            else :
                return jsonify({'error': "Please login first to checkin"}), 300

        else :
            return jsonify({'error': "Error Checking in"}), 100

    
  
   
   



          