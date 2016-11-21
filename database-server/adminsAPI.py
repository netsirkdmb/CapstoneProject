###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This is the admins portion of the employee recognition system API.             #
###############################################################################################


from flask import Flask, request, current_app as app
from flask_restful import Resource, reqparse, inputs
import traceback
from validation import *

# parser for creating admins
adminAccountParser = reqparse.RequestParser(bundle_errors=True)
adminAccountParser.add_argument("email", type=str, help="Email address for new admin.", required=True)
adminAccountParser.add_argument("password", type=str, help="Password for new admin.", required=True)
adminAccountParser.add_argument("salt", type=str, help="Salt for password.", required=True)

# parser for email
emailParser = reqparse.RequestParser(bundle_errors=True)
emailParser.add_argument("email", type=str, help="Admin's email address.", required=True)

# parser for passwordCode
passwordCodeParser = reqparse.RequestParser(bundle_errors=True)
passwordCodeParser.add_argument("passwordCode", type=str, help="Admin's password code.", required=True)
passwordCodeParser.add_argument("salt", type=str, help="Salt for password.", required=True)


class AdminsList(Resource):
    # get a list of all of the admins in the database
    def get(self):
        try:
            query = "SELECT adminID, email, password, salt, accountCreationTime FROM admins"
            app.cursor.execute(query)

            admins = list(app.cursor.fetchall())

            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["salt"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

            return {"Status": "Success", "Data": adminList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new admin in the database
    def post(self):
        admin = adminAccountParser.parse_args()

        adminEmail = admin["email"]
        adminPassword = admin["password"]
        adminSalt = admin["salt"]

        try:
            if not emailValidation(adminEmail):
                raise Exception("Email is not valid.")
            
            stmt = "INSERT INTO admins (email, password, salt) VALUES (%s, %s, %s)"
            app.cursor.execute(stmt, (adminEmail, adminPassword, adminSalt))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"email": adminEmail, "password": adminPassword, "salt": adminSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update admin without adminID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all admins."}, 400
    
    # delete all of the admins in the database
    def delete(self):
        try:
            stmt = "DELETE FROM admins"
            app.cursor.execute(stmt)

            app.conn.commit()

            return {"Status": "Success", "Message": "admins table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class Admin(Resource):
    # get admin with matching adminID if it exists, error if admin doesn't exist
    def get(self, adminID):
        try:
            query = "SELECT adminID, email, password, salt, accountCreationTime FROM admins WHERE adminID = %s"
            app.cursor.execute(query, int(adminID))

            admins = list(app.cursor.fetchall())

            if app.cursor.rowcount == 0:
                raise Exception("Admin does not exist in the database.") 

            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["salt"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

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
        adminSalt = admin["salt"]

        try:
            if not emailValidation(adminEmail):
                raise Exception("Email is not valid.")
            
            stmt = "UPDATE admins SET email = %s, password = %s, salt = %s WHERE adminID = %s"
            app.cursor.execute(stmt, (adminEmail, adminPassword, adminSalt, adminID))
            
            app.conn.commit()
            
            if app.cursor.rowcount == 0:
                raise Exception("Admin cannot be updated because it does not exist in the database.")         

            return {"Status": "Success", "Data": [{"email": adminEmail, "password": adminPassword, "salt": adminSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete an admin from the database, database is not changed if admin doesn't exist
    def delete(self, adminID):
        try:
            stmt = "DELETE FROM admins WHERE adminID = %s"
            app.cursor.execute(stmt, adminID)

            app.conn.commit()

            message = str(adminID) + " has now been deleted from admins table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AdminEmail(Resource):
    # get admin with matching email if it exists
    def post(self):
        email = emailParser.parse_args()

        email = email["email"]

        try:
            if not emailValidation(email):
                raise Exception("Email is not valid.")
            
            query = "SELECT adminID, email, password, salt, accountCreationTime FROM admins WHERE email = %s"
            app.cursor.execute(query, email)

            admins = list(app.cursor.fetchall())

            if app.cursor.rowcount == 0:
                raise Exception("Admin does not exist in the database.")
            
            adminList = []
            for admin in admins:
                adminInfo = {}
                (adminInfo["adminID"], 
                adminInfo["email"], 
                adminInfo["password"], 
                adminInfo["salt"], 
                adminInfo["accountCreationTime"]) = admin
                adminInfo["accountCreationTime"] = str(adminInfo["accountCreationTime"])
                adminList.append(adminInfo)

            return {"Status": "Success", "Data": adminList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # updates admin's passwordCode
    def put(self):
        email = emailParser.parse_args()
        adminEmail = email["email"]

        passwordCode = passwordCodeParser.parse_args()
        adminPasswordCode = passwordCode["passwordCode"]
        adminSalt = passwordCode["salt"]

        try:
            if not emailValidation(email):
                raise Exception("Email is not valid.")

            if adminPasswordCode == "":
                stmt = "UPDATE admins SET passwordCode = NULL, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (adminSalt, adminEmail))
            else:
                stmt = "UPDATE admins SET passwordCode = %s, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (adminPasswordCode, adminSalt, adminEmail))

            app.conn.commit()

            if app.cursor.rowcount == 0:
                raise Exception("Admin does not exist in the database.")
            
            return {"Status": "Success", "Data": [{"email": adminEmail, "passwordCode": adminPasswordCode, "salt": adminSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400