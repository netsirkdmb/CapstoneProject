###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This API is hosted on Amazon Web Services and allows the user and admin sites  #
#              to make queries to the MySQL database for our employee recognition system.     #
# References:                                                                                 #
# - for help with Flask                                                                       #
#       http://flask.pocoo.org/                                                               #
# - for help with Jinja2                                                                      #
#       https://realpython.com/blog/python/primer-on-jinja-templating/                        #
# - for help setting up virtual environment on AWS                                            #
#       http://docs.python-guide.org/en/latest/dev/virtualenvs/                               #
# - for help with Flask-restful                                                               #
#       http://flask-restful-cn.readthedocs.io/en/0.3.4/quickstart.html                       #
# - for help with LaTeX in Python                                                             #
#       http://akuederle.com/Automatization-with-Latex-and-Python-1                           #
# - for help with MySQL queries between two dates                                             #
#       http://stackoverflow.com/questions/9511409/creating-a-list-of-month-names-between-two-dates-in-mysql
# - for help with MySQL queries and ranking                                                   #
#       http://stackoverflow.com/questions/24118393/mysql-rank-with-ties                      #
###############################################################################################


from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL
import os
import shutil
import yaml
import traceback
import datetime
import arrow

app = Flask(__name__)
api = Api(app)
mysql = MySQL()

# MySQL configurations
f = open("/api/src/MySQLPasswords.yaml")
configDict = yaml.load(f)
app.config.update(configDict)

# request parsers to validate input
# parser for creating admins
adminAccountParser = reqparse.RequestParser(bundle_errors=True)
adminAccountParser.add_argument("email", type=str, help="Email address for new admin.", required=True)
adminAccountParser.add_argument("password", type=str, help="Password for new admin.", required=True)

# parser for creating users
userAccountParser = reqparse.RequestParser(bundle_errors=True)
userAccountParser.add_argument("name", type=str, help="Name for new user.", required=True)
userAccountParser.add_argument("email", type=str, help="Email address for new user.", required=True)
userAccountParser.add_argument("password", type=str, help="Password for new user.", required=True)
userAccountParser.add_argument("signatureImage", type=str, help="Signature for new user.", required=True)
userAccountParser.add_argument("region", type=str, help="Region for new user.", required=True)
# change startDate to required after mid-point check
userAccountParser.add_argument("startDate", type=inputs.date, help="User's start date.", required=False)

# parser for updating user
userAccountUpdateParser = reqparse.RequestParser(bundle_errors=True)
userAccountUpdateParser.add_argument("name", type=str, help="Name for user.", required=True)
userAccountUpdateParser.add_argument("email", type=str, help="Email address for user.", required=True)
userAccountUpdateParser.add_argument("password", type=str, help="Password for user.", required=True)
userAccountUpdateParser.add_argument("signatureImage", type=str, help="Signature for user.", required=False)
userAccountUpdateParser.add_argument("region", type=str, help="Region for user.", required=True)
# change startDate to required after mid-point check
userAccountUpdateParser.add_argument("startDate", type=inputs.date, help="User's start date.", required=False)

# parser for email
emailParser = reqparse.RequestParser(bundle_errors=True)
emailParser.add_argument("email", type=str, help="Email address.", required=True)

# parser for passwordCode
passwordCodeParser = reqparse.RequestParser(bundle_errors=True)
passwordCodeParser.add_argument("passwordCode", type=str, help="User's password code.", required=True)

# parser for creating awardTypes
awardTypeParser = reqparse.RequestParser(bundle_errors=True)
awardTypeParser.add_argument("name", type=str, help="Name for new award type.", required=True)
awardTypeParser.add_argument("prestigeLevel", type=int, help="Prestige level for new award type.", required=True)

# parser for creating awards
awardParser = reqparse.RequestParser(bundle_errors=True)
awardParser.add_argument("receiverID", type=int, help="The user that is getting the award.", required=True)
awardParser.add_argument("giverID", type=int, help="The user that is giving the award.", required=True)
awardParser.add_argument("typeID", type=int, help="The type of award being given.", required=True)
awardParser.add_argument("awardDate", type=str, help="The date award is being given.", required=True)

# parser for get admins/users request
pageParser = reqparse.RequestParser(bundle_errors=True)
pageParser.add_argument("offset", type=inputs.natural)
pageParser.add_argument("limit", type=inputs.positive)

mysql.init_app(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class AdminsList(Resource):
    # get a list of all of the admins in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT adminID, email, password, accountCreationTime FROM admins"
            app.cursor.execute(query)

            admins = list(app.cursor.fetchall())

            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": adminList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new admin in the database
    def post(self):
        admin = adminAccountParser.parse_args()

        adminEmail = admin["email"]
        adminPassword = admin["password"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO admins (email, password) VALUES (%s, %s)"
            app.cursor.execute(stmt, (adminEmail, adminPassword))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"email": adminEmail, "password": adminPassword}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update admin without adminID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all admins."}, 400
    
    # delete all of the admins in the database
    def delete(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM admins"
            app.cursor.execute(stmt)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Message": "admins table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class Admin(Resource):
    # get admin with matching adminID if it exists
    def get(self, adminID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT adminID, email, password, accountCreationTime FROM admins WHERE adminID = %s"
            app.cursor.execute(query, int(adminID))

            admins = list(app.cursor.fetchall())

            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": adminList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # insert admin with adminID error
    def post(self, adminID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the admin that you are creating."}, 400

    # update admin in database, errors if the admin does not exist in the database
    def put(self, adminID):
        admin = adminAccountParser.parse_args()

        adminEmail = admin["email"]
        adminPassword = admin["password"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "UPDATE admins SET email = %s, password = %s WHERE adminID = %s"
            app.cursor.execute(stmt, (adminEmail, adminPassword, adminID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"email": adminEmail, "password": adminPassword}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete an admin from the database, errors if the admin does not exist in the database
    def delete(self, adminID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM admins WHERE adminID = %s"
            app.cursor.execute(stmt, adminID)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            message = str(adminID) + " has now been deleted from admins table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class UsersList(Resource):
    # get a list of all of the users in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT userID, name, email, password, passwordCode, region, startDate, accountCreationTime FROM users"
            app.cursor.execute(query)

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["passwordCode"], 
                userInfo["region"], 
                userInfo["startDate"], 
                userInfo["accountCreationTime"]) = user
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": userData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new user in the database
    def post(self):
        user = userAccountParser.parse_args()

        userName = user["name"]
        userEmail = user["email"]
        userPassword = user["password"]
        userSignature = user["signatureImage"]
        userRegion = user["region"]
        if user["startDate"]:
            userStartDate = user["startDate"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()
            returnData = []
            if userStartDate:
                stmt = "INSERT INTO users (name, email, password, signatureImage, region, startDate) VALUES (%s, %s, %s, %s, %s, %s)"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userSignature, userRegion, userStartDate))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "signatureImage": userSignature, "region": userRegion, "startDate": str(userStartDate)[:-9]}]
            else:
                stmt = "INSERT INTO users (name, email, password, signatureImage, region) VALUES (%s, %s, %s, %s, %s)"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userSignature, userRegion))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "signatureImage": userSignature, "region": userRegion}]
            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": returnData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update user without userID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all users."}, 400
    
    # delete all of the users in the database
    def delete(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM users"
            app.cursor.execute(stmt)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Message": "users table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class User(Resource):
    # get user with matching userID if it exists
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT userID, name, email, password, passwordCode, signatureImage, region, startDate, accountCreationTime FROM users WHERE userID = %s"
            app.cursor.execute(query, int(userID))

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["passwordCode"], 
                userInfo["signatureImage"], 
                userInfo["region"], 
                userInfo["startDate"],
                userInfo["accountCreationTime"]) = user
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": userData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # insert user with userID error
    def post(self, userID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the user that you are creating."}, 400

    # update user in database, errors if the user does not exist in the database
    def put(self, userID):
        user = userAccountUpdateParser.parse_args()

        userName = user["name"]
        userEmail = user["email"]
        userPassword = user["password"]
        if user["signatureImage"]:
            userSignature = user["signatureImage"]
        userRegion = user["region"]
        if user["startDate"]:
            userStartDate = user["startDate"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()
            returnData = []
            if userSignature and userStartDate:
                stmt = "UPDATE users SET name = %s, email = %s, password = %s, signatureImage = %s, region = %s, startDate = %s WHERE userID = %s"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userSignature, userRegion, userStartDate, userID))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "signatureImage": userSignature, "region": userRegion, "startDate": userStartDate}]
            elif userSignature and not userStartDate:
                stmt = "UPDATE users SET name = %s, email = %s, password = %s, signatureImage = %s, region = %s WHERE userID = %s"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userSignature, userRegion, userID))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "signatureImage": userSignature, "region": userRegion}]
            elif userStartDate and not userSignature:
                stmt = "UPDATE users SET name = %s, email = %s, password = %s, region = %s, startDate = %s WHERE userID = %s"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userRegion, userStartDate, userID))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "region": userRegion, "startDate": userStartDate}]
            else:
                stmt = "UPDATE users SET name = %s, email = %s, password = %s, region = %s WHERE userID = %s"
                app.cursor.execute(stmt, (userName, userEmail, userPassword, userRegion, userID))
                returnData = [{"name": userName, "email": userEmail, "password": userPassword, "region": userRegion}]
            
            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": returnData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a user from the database, errors if the user does not exist in the database
    def delete(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM users WHERE userID = %s"
            app.cursor.execute(stmt, userID)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            message = str(userID) + " has now been deleted from users table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardTypesList(Resource):
    # get a list of all of the award types in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT awardTypeID, name, prestigeLevel FROM awardTypes"
            app.cursor.execute(query)

            awardTypes = list(app.cursor.fetchall())

            awardTypesData = []
            for awardType in awardTypes:
                awardTypeInfo = {}
                (awardTypeInfo["awardTypeID"], 
                awardTypeInfo["name"], 
                awardTypeInfo["prestigeLevel"]) = awardType
                awardTypesData.append(awardTypeInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardTypesData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new award type in the database
    def post(self):
        awardType = awardTypeParser.parse_args()

        awardTypeName = awardType["name"]
        awardTypePrestige = awardType["prestigeLevel"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO awardTypes (name, prestigeLevel) VALUES (%s, %s)"
            app.cursor.execute(stmt, (awardTypeName, awardTypePrestige))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"name": awardTypeName, "prestigeLevel": awardTypePrestige}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update award type without awardTypeID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all award types."}, 400
    
    # delete all of the award types in the database
    def delete(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM awardTypes"
            app.cursor.execute(stmt)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Message": "awardTypes table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardType(Resource):
    # get award type with matching awardTypeID if it exists
    def get(self, awardTypeID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT awardTypeID, name, prestigeLevel FROM awardTypes WHERE awardTypeID = %s"
            app.cursor.execute(query, int(awardTypeID))

            awardTypes = list(app.cursor.fetchall())

            awardTypesData = []
            for awardType in awardTypes:
                awardTypeInfo = {}
                (awardTypeInfo["awardTypeID"], 
                awardTypeInfo["name"], 
                awardTypeInfo["prestigeLevel"]) = awardType
                awardTypesData.append(awardTypeInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardTypesData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # insert award type with awardTypeID error
    def post(self, awardTypeID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the award type that you are creating."}, 400

    # update award type in database, errors if the award type does not exist in the database
    def put(self, awardTypeID):
        awardType = awardTypeParser.parse_args()

        awardTypeName = awardType["name"]
        awardTypePrestige = awardType["prestigeLevel"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "UPDATE awardTypes SET name = %s, prestigeLevel = %s WHERE awardTypeID = %s"
            app.cursor.execute(stmt, (awardTypeName, awardTypePrestige, awardTypeID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"name": awardTypeName, "prestigeLevel": awardTypePrestige}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a award type from the database, errors if the award type does not exist in the database
    def delete(self, awardTypeID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM awardTypes WHERE awardTypeID = %s"
            app.cursor.execute(stmt, awardTypeID)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            message = str(awardTypeID) + " has now been deleted from awardTypes table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardsList(Resource):
    # get a list of all of the awards in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID"""
            app.cursor.execute(query)

            awards = list(app.cursor.fetchall())

            awardData = []
            for award in awards:
                awardInfo = {}
                (awardInfo["awardID"], 
                awardInfo["receiverID"], 
                awardInfo["receiverName"], 
                awardInfo["giverID"], 
                awardInfo["giverName"], 
                awardInfo["awardTypeID"], 
                awardInfo["awardType"],
                awardInfo["awardDate"]) = award
                awardInfo["awardDate"] = str(awardInfo["awardDate"])
                awardData.append(awardInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new award in the database
    def post(self):
        award = awardParser.parse_args()

        awardReceiverID = award["receiverID"]
        awardGiverID = award["giverID"]
        awardTypeID = award["typeID"]
        awardDate = award["awardDate"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (%s, %s, %s, %s)"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"receiverID": awardReceiverID, "giverID": awardGiverID, "typeID": awardTypeID, "awardDate": awardDate}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update award without awardID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all awards."}, 400
    
    # delete all of the awards in the database
    def delete(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM awards"
            app.cursor.execute(stmt)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Message": "awards table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class Award(Resource):
    # get award with matching awardID if it exists
    def get(self, awardID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE a.awardID = %s"""
            app.cursor.execute(query, int(awardID))

            awards = list(app.cursor.fetchall())

            awardData = []
            for award in awards:
                awardInfo = {}
                (awardInfo["awardID"], 
                awardInfo["receiverID"], 
                awardInfo["receiverName"], 
                awardInfo["giverID"], 
                awardInfo["giverName"], 
                awardInfo["awardTypeID"], 
                awardInfo["awardType"],
                awardInfo["awardDate"]) = award
                awardInfo["awardDate"] = str(awardInfo["awardDate"])
                awardData.append(awardInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # insert award with awardID error
    def post(self, awardID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the award that you are creating."}, 400

    # update award in database, errors if the award does not exist in the database
    def put(self, awardID):
        award = awardParser.parse_args()

        awardReceiverID = award["receiverID"]
        awardGiverID = award["giverID"]
        awardTypeID = award["typeID"]
        awardDate = award["awardDate"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "UPDATE awards SET receiverID = %s, giverID = %s, typeID = %s, awardDate = %s WHERE awardID = %s"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate, awardID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"receiverID": awardReceiverID, "giverID": awardGiverID, "typeID": awardTypeID, "awardDate": awardDate}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a award from the database, errors if the award does not exist in the database
    def delete(self, awardID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM awards WHERE awardID = %s"
            app.cursor.execute(stmt, awardID)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            message = str(awardID) + " has now been deleted from awards table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUser(Resource):
    # get all awards that userID has given
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE giv.userID = %s"""
            app.cursor.execute(query, int(userID))

            awards = list(app.cursor.fetchall())

            awardData = []
            for award in awards:
                awardInfo = {}
                (awardInfo["awardID"], 
                awardInfo["receiverID"], 
                awardInfo["receiverName"], 
                awardInfo["giverID"], 
                awardInfo["giverName"], 
                awardInfo["awardTypeID"], 
                awardInfo["awardType"],
                awardInfo["awardDate"]) = award
                awardInfo["awardDate"] = str(awardInfo["awardDate"])
                awardData.append(awardInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # insert award with userID error
    def post(self, userID):
        return {"Status": "Fail", "Message": "To create an award that this user has given, please send a post request to /awards."}, 400

    # update awards given by user with userID error
    def put(self, userID):
        return {"Status": "Fail", "Message": "You are not allowed to do a bulk update of all the awards that the user has given."}, 400

    # delete a award from the database, errors if the award does not exist in the database
    def delete(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "DELETE FROM awards WHERE giverID = %s"
            app.cursor.execute(stmt, userID)

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            message = "All awards given by " + str(userID) + " have now been deleted from awards table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class ResetTables(Resource):
    def post(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            result = clearTables()

            app.cursor.close()
            app.conn.close()

            return result
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AddDummyData(Resource):
    def post(self):
        data = None

        app.conn = mysql.connect()
        app.cursor = app.conn.cursor()

        try:
            clearTables()
            app.cursor.callproc('spAddDummyData')
            data = app.cursor.fetchall()
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
        
        if len(data) == 0:
            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success"}, 200
        else:
            app.cursor.close()
            app.conn.close()

            return {"Status": "Fail", "Message": data}, 400


def clearTables():
    app.cursor.callproc('spResetTables')
    data = app.cursor.fetchall()
    if len(data) == 0:
        app.conn.commit()
        return {"Status": "Success"}, 200
    else:
        return {"Status": "Fail", "Message": data}, 400


def convertMonth(mon):
    if mon == 1:
        return "January"
    elif mon == 2:
        return "February"
    elif mon == 3:
        return "March"
    elif mon == 4:
        return "April"
    elif mon == 5:
        return "May"
    elif mon == 6:
        return "June"
    elif mon == 7:
        return "July"
    elif mon == 8:
        return "August"
    elif mon == 9:
        return "September"
    elif mon == 10:
        return "October"
    elif mon == 11:
        return "November"
    else:
        return "December"


def convertDate(dateText):
    theDate = arrow.get(dateText)
    theYear = theDate.format("YYYY")
    theMonth = theDate.format("MMMM")
    theDay = theDate.format("Do")
    return theDay, theMonth, theYear


class CreateAward(Resource):
    # get details of award in order to create PDF certificate
    def get(self, awardID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    rec.email, 
                    a.giverID, giv.name AS giverName, 
                    giv.signatureImage, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE a.awardID = %s"""
            app.cursor.execute(query, int(awardID))

            awards = list(app.cursor.fetchall())

            awardData = []
            for award in awards:
                awardInfo = {}
                (awardInfo["awardID"], 
                awardInfo["receiverID"], 
                awardInfo["receiverName"], 
                awardInfo["receiverEmail"], 
                awardInfo["giverID"], 
                awardInfo["giverName"], 
                awardInfo["giverSignatureImage"], 
                awardInfo["awardTypeID"], 
                awardInfo["awardType"],
                awardInfo["awardDate"]) = award
                awardInfo["awardDate"] = str(awardInfo["awardDate"])
                awardData.append(awardInfo)
            
            app.cursor.close()
            app.conn.close()

            project = "/api/src/"
            pdf_d = "{0}pdf/".format(project)
            
            build_d = "{0}build/".format(project)
            out_file = "{0}tempFile".format(build_d)
            ## code to do certificate with variables
            test_file = "{0}certificate.tex".format(build_d)

            theDay, theMonth, theYear = convertDate(awardData[0]["awardDate"])

            # open certificate.tex for reading and replace variables
            with open(test_file, "r") as rf:
                fileContentsStr = rf.read()
                fileContentsStr = fileContentsStr.replace("###awardType###", awardData[0]["awardType"])
                fileContentsStr = fileContentsStr.replace("###giverName###", awardData[0]["giverName"])
                fileContentsStr = fileContentsStr.replace("###receiverName###", awardData[0]["receiverName"])
                fileContentsStr = fileContentsStr.replace("###theDay###", theDay)
                fileContentsStr = fileContentsStr.replace("###theMonth###", theMonth)
                fileContentsStr = fileContentsStr.replace("###theYear###", theYear)
                fileContentsStr = fileContentsStr.replace("###giverSignatureImage###", "obama.png")

            # create the build directory if not existing
            if not os.path.exists(build_d):
                os.makedirs(build_d)
            
            # create the pdf directory if not existing
            if not os.path.exists(pdf_d):
                os.makedirs(pdf_d)
            
            # saves fileContentsStr to output file
            with open(out_file + ".tex", "w") as f:
                f.write(fileContentsStr)
            
            os.chdir(os.path.realpath(build_d))
            os.system("pdflatex -output-directory {0} {1}".format(os.path.realpath(build_d), os.path.realpath(out_file)))
            shutil.copy2(out_file + ".pdf", os.path.realpath(pdf_d))

            return {"Status": "Success", "Data": awardData}, 200

        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class UserEmail(Resource):
    # get user with matching email if it exists
    def post(self):
        email = emailParser.parse_args()

        userEmail = email["email"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT userID, name, email, password, passwordCode, region, startDate, accountCreationTime FROM users WHERE email = %s"
            app.cursor.execute(query, userEmail)

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["passwordCode"], 
                userInfo["region"], 
                userInfo["startDate"],
                userInfo["accountCreationTime"]) = user
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": userData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # updates user's passwordCode
    def put(self):
        email = emailParser.parse_args()
        userEmail = email["email"]

        passwordCode = passwordCodeParser.parse_args()
        userPasswordCode = passwordCode["passwordCode"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            if userPasswordCode == "":
                stmt = "UPDATE users SET passwordCode = NULL WHERE email = %s"
                app.cursor.execute(stmt, (userEmail))
            else:
                stmt = "UPDATE users SET passwordCode = %s WHERE email = %s"
                app.cursor.execute(stmt, (userPasswordCode, userEmail))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [{"email": userEmail, "passwordCode": userPasswordCode}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AdminEmail(Resource):
    # get admin with matching email if it exists
    def post(self):
        email = emailParser.parse_args()

        email = email["email"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT adminID, email, password, accountCreationTime FROM admins WHERE email = %s"
            app.cursor.execute(query, email)

            admins = list(app.cursor.fetchall())

            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": adminList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    
class FreqChart(Resource):
    # get the count of awards being given in the previous 12 months
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT y, m, Count(a.awardDate) AS count FROM
                    (SELECT y, m FROM
                    (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years,
                    (SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
                    UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12) months) ym
                    LEFT JOIN cs419.awards a ON ym.y = YEAR(a.awardDate) AND ym.m = MONTH(a.awardDate)
                    WHERE (y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE()))
                    GROUP BY y, m"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["frequency"]) = row
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AnnualAwardTypes(Resource):
    # get the award types being given in the previous 12 months
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.typeID as typeID, aTyp.name as name, aTyp.prestigeLevel as prestigeLevel, Count(a.typeID) AS count FROM
                    (SELECT y, m FROM
                    (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years,
                    (SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
                    UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12) months) ym
                    RIGHT JOIN cs419.awards a ON ym.y = YEAR(a.awardDate) AND ym.m = MONTH(a.awardDate)
					INNER JOIN cs419.awardTypes aTyp ON a.typeID = aTyp.awardTypeID
					WHERE (y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) 
                    GROUP BY typeID"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["tyepID"], 
                rowInfo["name"], 
                rowInfo["value"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

class EmployeeRank(Resource):
    # get the employee's all-time ranking based on awards received
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                    FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                    LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                    GROUP BY u.userID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z WHERE z.userID = %s"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"],
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["prestige"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["prestige"] = int(rowInfo["prestige"])
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AllEmployeeRank(Resource):
    # get the all-time ranking based on awards received
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                    FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                    LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                    GROUP BY u.userID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"],
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["prestige"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["prestige"] = int(rowInfo["prestige"])
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class EmployeePrestigePoints(Resource):
    # get the prestige points for the awards the employee has received each month over their career
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT YEAR(aDate) AS year, MONTH(aDate) AS month, COALESCE(h.points, 0) AS points FROM (
                    SELECT @maxDate - INTERVAL (a.a+(10*b.a)+(100*c.a)+(1000*d.a) + (10000*e.a)) day aDate FROM
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a, /*10 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b, /*100 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c, /*1000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d, /*10000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) e, /*100000 day range*/
                    (SELECT @minDate := (SELECT startDate FROM users WHERE userID = %s), @maxDate := CURDATE()) f
                    ) g LEFT JOIN (SELECT YEAR(a.awardDate) AS ay, MONTH(a.awardDate) AS am, SUM(atyp.prestigeLevel) AS points FROM users u 
                        INNER JOIN awards a ON u.userID = a.receiverID 
                        INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                        WHERE u.userID = %s
                        GROUP BY YEAR(a.awardDate) DESC, MONTH(a.awardDate) DESC) h ON h.ay = YEAR(aDate) AND h.am = MONTH(aDate)
                    WHERE aDate BETWEEN @minDate AND @maxDate
                    GROUP BY year DESC, month DESC"""
            app.cursor.execute(query, (int(userID), int(userID)))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["points"]) = row
                rowInfo["year"] = int(rowInfo["year"])
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowInfo["points"] = int(rowInfo["points"])
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class EmployeeAwardTypes(Resource):
    # get the award types the employee has received over their career
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT atyp.awardTypeID AS typeID, 
                    atyp.name as awardName, 
                    atyp.prestigeLevel AS value, 
                    COUNT(atyp.name) as frequency FROM users u 
                    INNER JOIN awards a ON u.userID = a.receiverID 
                    INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                    WHERE u.userID = %s
                    GROUP BY atyp.name ASC"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["tyepID"], 
                rowInfo["name"], 
                rowInfo["value"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUserReceived(Resource):
    # get all awards that userID has received
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE rec.userID = %s
					ORDER BY a.awardDate DESC"""
            app.cursor.execute(query, int(userID))

            awards = list(app.cursor.fetchall())

            awardData = []
            for award in awards:
                awardInfo = {}
                (awardInfo["awardID"], 
                awardInfo["receiverID"], 
                awardInfo["receiverName"], 
                awardInfo["giverID"], 
                awardInfo["giverName"], 
                awardInfo["awardTypeID"], 
                awardInfo["awardType"],
                awardInfo["awardDate"]) = award
                awardInfo["awardDate"] = str(awardInfo["awardDate"])
                awardData.append(awardInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUserGivenFreq(Resource):
    # get the frequency of awards that userID has given
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT YEAR(aDate) AS year, MONTH(aDate) AS month, COALESCE(h.count, 0) AS count FROM (
                    SELECT @maxDate - INTERVAL (a.a+(10*b.a)+(100*c.a)+(1000*d.a) + (10000*e.a)) day aDate FROM
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a, /*10 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b, /*100 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c, /*1000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d, /*10000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) e, /*100000 day range*/
                    (SELECT @minDate := (SELECT startDate FROM users WHERE userID = %s), @maxDate := CURDATE()) f
                    ) g LEFT JOIN (SELECT YEAR(a.awardDate) AS ay, MONTH(a.awardDate) AS am, count(a.awardDate) as count FROM users u 
                        INNER JOIN awards a ON u.userID = a.giverID 
                        WHERE u.userID = %s
                        GROUP BY YEAR(a.awardDate) DESC, MONTH(a.awardDate) DESC) h ON h.ay = YEAR(aDate) and h.am = MONTH(aDate)
                    WHERE aDate BETWEEN @minDate AND @maxDate
                    GROUP BY year DESC, month DESC"""
            app.cursor.execute(query, (int(userID), int(userID)))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["frequency"]) = row
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUserGivenTypes(Resource):
    # get the frequency of types of awards that userID has given
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = """SELECT atyp.name as awardName, COUNT(atyp.name) as frequency FROM users u 
                    INNER JOIN awards a ON u.userID = a.giverID 
                    INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                    WHERE u.userID = %s
                    GROUP BY atyp.name ASC"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["type"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class TopEmployees(Resource):
    def get(self):
        # get current month
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        year = int(year)
        monthList = []
        for i in range(12):
            monthNum = (int(month) - i) % 12
            if monthNum == 0:
                monthNum = 12
                year -= 1
            monthList.append((monthNum, year))

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            resultsList = {}

            for i in range(len(monthList)):
                queryMonth, queryYear = monthList[i]

                query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                        (SELECT x.userID, x.name, x.points, 
                        @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                        IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                        (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                        FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                        LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                        WHERE MONTH(a.awardDate) = %s AND YEAR(a.awardDate) = %s GROUP BY u.userID) x,
                        (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                        ORDER BY x.points DESC, x.userID ASC) z LIMIT 5"""
                app.cursor.execute(query, (queryMonth, queryYear))

                rows = list(app.cursor.fetchall())
                
                if len(rows) != 0:
                    rowList = []
                    for row in rows:
                        rowInfo = {}
                        (rowInfo["userID"], 
                        rowInfo["name"], 
                        rowInfo["rank"], 
                        rowInfo["points"]) = row
                        rowInfo["rank"] = int(rowInfo["rank"])
                        rowInfo["points"] = int(rowInfo["points"])
                        rowList.append(rowInfo)
                    
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = rowList
                else:
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = [0]
            
            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT z.receiverID AS userID, z.receiverName AS name, SUM(z.points) AS points FROM
					(SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.typeID, atyp.name AS awardType, atyp.prestigeLevel AS points,
                    a.awardDate FROM
					(SELECT @minDate := DATE_SUB(CURDATE(),INTERVAL 1 YEAR), @maxDate := CURDATE()) f INNER JOIN
					cs419.awards a ON a.awardDate > @minDate AND a.awardDate <= @maxDate INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID
					ORDER BY a.awardDate DESC) z
					GROUP BY z.receiverID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z LIMIT 5"""

            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"], 
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["points"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["points"] = int(rowInfo["points"])
                rowList.append(rowInfo)
            
            resultsList["Year"] = rowList

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": resultsList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class MostGenerous(Resource):
    def get(self):
        # get current month
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        year = int(year)
        monthList = []
        for i in range(12):
            monthNum = (int(month) - i) % 12
            if monthNum == 0:
                monthNum = 12
                year -= 1
            monthList.append((monthNum, year))

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            resultsList = {}

            for i in range(len(monthList)):
                queryMonth, queryYear = monthList[i]

                query = """SELECT z.userID, z.name, z.rank, z.frequency FROM 
                    (SELECT x.userID, x.name, x.frequency, 
                    @prev := @curr, @curr := x.frequency, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.frequency, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID AS userID, u.name AS name, COUNT(a.awardDate) AS frequency FROM
					users u INNER JOIN awards a ON u.userID = a.giverID 
                    WHERE MONTH(a.awardDate) = %s AND YEAR(a.awardDate) = %s GROUP BY u.userID) x,
					(SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
					ORDER BY x.frequency DESC, x.userID ASC) z LIMIT 5"""
                app.cursor.execute(query, (queryMonth, queryYear))

                rows = list(app.cursor.fetchall())
                
                if len(rows) != 0:
                    rowList = []
                    for row in rows:
                        rowInfo = {}
                        (rowInfo["userID"], 
                        rowInfo["name"], 
                        rowInfo["rank"], 
                        rowInfo["frequency"]) = row
                        rowInfo["rank"] = int(rowInfo["rank"])
                        rowInfo["frequency"] = int(rowInfo["frequency"])
                        rowList.append(rowInfo)
                    
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = rowList
                else:
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = [0]
            
            query = """SELECT z.userID, z.name, z.rank, z.frequency FROM 
                    (SELECT x.userID, x.name, x.frequency, 
                    @prev := @curr, @curr := x.frequency, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.frequency, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT z.giverID AS userID, z.giverName AS name, COUNT(z.awardDate) AS frequency FROM
					(SELECT a.awardID, a.giverID, giv.name AS giverName, a.awardDate FROM
					(SELECT @minDate := DATE_SUB(CURDATE(),INTERVAL 1 YEAR), @maxDate := CURDATE()) f INNER JOIN
					cs419.awards a ON a.awardDate > @minDate AND a.awardDate <= @maxDate INNER JOIN 
                    users giv ON a.giverID = giv.userID ORDER BY a.awardDate DESC) z
					GROUP BY z.giverID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.frequency DESC, x.userID ASC) z LIMIT 5"""

            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"], 
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["frequency"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["frequency"] = int(rowInfo["frequency"])
                rowList.append(rowInfo)
            
            resultsList["Year"] = rowList

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Results": resultsList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


# create routes for API
api.add_resource(AdminsList, '/admins')
api.add_resource(Admin, '/admins/<int:adminID>')
api.add_resource(UsersList, '/users')
api.add_resource(User, '/users/<int:userID>')
api.add_resource(AwardTypesList, '/awardTypes')
api.add_resource(AwardType, '/awardTypes/<int:awardTypeID>')
api.add_resource(AwardsList, '/awards')
api.add_resource(Award, '/awards/<int:awardID>')
api.add_resource(AwardUser, '/userAwards/<int:userID>')
api.add_resource(ResetTables, '/resetTables')
api.add_resource(AddDummyData, '/resetTablesWithDummyData')
api.add_resource(CreateAward, '/getAwardCreationInfo/<int:awardID>')
api.add_resource(UserEmail, '/getUserByEmail')
api.add_resource(AdminEmail, '/getAdminByEmail')
api.add_resource(TopEmployees, '/getTopEmployees')
api.add_resource(MostGenerous, '/getGenerousEmployees')
api.add_resource(FreqChart, '/getFrequencyChart')
api.add_resource(AnnualAwardTypes, '/getAwardTypes')
api.add_resource(AllEmployeeRank, '/getRanking')
api.add_resource(EmployeeRank, '/getRanking/<int:userID>')
api.add_resource(EmployeePrestigePoints, '/getPrestigePoints/<int:userID>')
api.add_resource(EmployeeAwardTypes, '/getAwardTypes/<int:userID>')
api.add_resource(AwardUserReceived, '/getAwardsReceived/<int:userID>')
api.add_resource(AwardUserGivenFreq, '/getAwardsGivenFrequency/<int:userID>')
api.add_resource(AwardUserGivenTypes, '/getAwardTypesGiven/<int:userID>')


if __name__ == "__main__":
    # context = ("cert.crt", "key.key")
    # app.run(ssl_context=context, debug=False, port=5600, host="0.0.0.0")
    app.run(debug=False, port=5600, host="0.0.0.0")