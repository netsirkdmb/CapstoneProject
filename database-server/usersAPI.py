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


from flask import Flask, request, current_app as app
from flask_restful import Resource, reqparse, inputs
import traceback
import os
from werkzeug.utils import secure_filename

# parser for creating users
userAccountParser = reqparse.RequestParser(bundle_errors=True)
userAccountParser.add_argument("name", type=str, help="Name for user.", required=True)
userAccountParser.add_argument("email", type=str, help="Email address for user.", required=True)
userAccountParser.add_argument("password", type=str, help="Password for user.", required=True)
userAccountParser.add_argument("salt", type=str, help="Salt for password.", required=True)
userAccountParser.add_argument("region", type=str, help="Region for new user.", required=True)
userAccountParser.add_argument("startDate", type=inputs.date, help="User's start date.", required=True)

# parser for email
emailParser = reqparse.RequestParser(bundle_errors=True)
emailParser.add_argument("email", type=str, help="User's email address.", required=True)

# parser for passwordCode
passwordCodeParser = reqparse.RequestParser(bundle_errors=True)
passwordCodeParser.add_argument("passwordCode", type=str, help="User's password code.", required=True)
passwordCodeParser.add_argument("salt", type=str, help="Salt for password.", required=True)


def uploadSignatureImage(request, userID):
    if "image" not in request.files:
        return {"Status": "Fail", "Error": "Image not received."}
    
    image = request.files["image"]

    if image.filename == "":
        return {"Status": "Fail", "Error": "Image must have a filename."}
    
    filename = secure_filename(image.filename)
    base, f_extension = os.path.splitext(filename)

    signatureImage = str(userID) + f_extension

    try:
            stmt = "UPDATE users SET signatureImage = %s WHERE userID = %s"
            app.cursor.execute(stmt, (signatureImage, userID))

            app.conn.commit()
    
    except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    filePath = "/api/src/upload/" + signatureImage

    image.save(filePath)

    message = filename + " has been uploaded."

    return {"Status": "Success", "Message": message}, 200


class SignatureImage(Resource):
    def post(self, userID):
        try:
            result = uploadSignatureImage(request, userID)

            return result
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class UsersList(Resource):
    # get a list of all of the users in the database
    def get(self):
        try:
            query = "SELECT userID, name, email, password, salt, passwordCode, region, startDate, accountCreationTime FROM users"
            app.cursor.execute(query)

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["salt"], 
                userInfo["passwordCode"], 
                userInfo["region"], 
                userInfo["startDate"], 
                userInfo["accountCreationTime"]) = user
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

            return {"Status": "Success", "Data": userData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new user in the database
    def post(self):
        user = userAccountParser.parse_args()

        userName = user["name"]
        userEmail = user["email"]
        userPassword = user["password"]
        userSalt = user["salt"]
        userRegion = user["region"]
        userStartDate = user["startDate"]

        try:
            stmt = "INSERT INTO users (name, email, password, salt, region, startDate) VALUES (%s, %s, %s, %s, %s, %s)"
            app.cursor.execute(stmt, (userName, userEmail, userPassword, userSalt, userRegion, userStartDate))

            app.conn.commit()

            query = "SELECT userID FROM users WHERE email = %s"
            app.cursor.execute(query, userEmail)

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                userInfo["userID"] = user
                userData.append(userInfo)
            
            imageMessage = uploadSignatureImage(request, userData[0]["userID"])

            return {"Status": "Success", "Data": [{"name": userName, "email": userEmail, "password": userPassword, "salt": userSalt, "region": userRegion, "startDate": str(userStartDate)[:-9]}], "Image": imageMessage}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update user without userID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all users."}, 400
    
    # delete all of the users in the database
    def delete(self):
        try:
            stmt = "DELETE FROM users"
            app.cursor.execute(stmt)

            app.conn.commit()

            return {"Status": "Success", "Message": "users table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class User(Resource):
    # get user with matching userID if it exists
    def get(self, userID):
        try:
            query = "SELECT userID, name, email, password, salt, passwordCode, signatureImage, region, startDate, accountCreationTime FROM users WHERE userID = %s"
            app.cursor.execute(query, int(userID))

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["salt"], 
                userInfo["passwordCode"], 
                userInfo["signatureImage"], 
                userInfo["region"], 
                userInfo["startDate"],
                userInfo["accountCreationTime"]) = user
                userInfo["signatureImage"] = "http://ec2-52-42-152-172.us-west-2.compute.amazonaws.com:5600/images/" + userInfo["signatureImage"]
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

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
        userSalt = user["salt"]
        userRegion = user["region"]
        userStartDate = user["startDate"]

        try:
            stmt = "UPDATE users SET name = %s, email = %s, password = %s, region = %s, startDate = %s WHERE userID = %s"
            app.cursor.execute(stmt, (userName, userEmail, userPassword, userSalt, userRegion, userStartDate, userID))
            
            app.conn.commit()

            imageMessage = uploadSignatureImage(request, userID)

            return {"Status": "Success", "Data": [{"name": userName, "email": userEmail, "password": userPassword, "salt": userSalt, "region": userRegion, "startDate": str(userStartDate)}], "Image": imageMessage}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a user from the database, errors if the user does not exist in the database
    def delete(self, userID):
        try:
            stmt = "DELETE FROM users WHERE userID = %s"
            app.cursor.execute(stmt, userID)

            app.conn.commit()

            message = str(userID) + " has now been deleted from users table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class UserEmail(Resource):
    # get user with matching email if it exists
    def post(self):
        email = emailParser.parse_args()

        userEmail = email["email"]

        try:
            query = "SELECT userID, name, email, password, salt, passwordCode, region, startDate, accountCreationTime FROM users WHERE email = %s"
            app.cursor.execute(query, userEmail)

            users = list(app.cursor.fetchall())

            userData = []
            for user in users:
                userInfo = {}
                (userInfo["userID"], 
                userInfo["name"], 
                userInfo["email"], 
                userInfo["password"], 
                userInfo["salt"], 
                userInfo["passwordCode"], 
                userInfo["region"], 
                userInfo["startDate"],
                userInfo["accountCreationTime"]) = user
                userInfo["startDate"] = str(userInfo["startDate"])
                userInfo["accountCreationTime"] = str(userInfo["accountCreationTime"])
                userData.append(userInfo)

            return {"Status": "Success", "Data": userData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # updates user's passwordCode
    def put(self):
        email = emailParser.parse_args()
        userEmail = email["email"]

        passwordCode = passwordCodeParser.parse_args()
        userPasswordCode = passwordCode["passwordCode"]
        userSalt = passwordCode["salt"]

        try:
            if userPasswordCode == "":
                stmt = "UPDATE users SET passwordCode = NULL, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (userSalt, userEmail))
            else:
                stmt = "UPDATE users SET passwordCode = %s, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (userPasswordCode, userSalt, userEmail))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"email": userEmail, "passwordCode": userPasswordCode, "salt": userSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400