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
    # get admin with matching adminID if it exists
    def get(self, adminID):
        try:
            query = "SELECT adminID, email, password, salt, accountCreationTime FROM admins WHERE adminID = %s"
            app.cursor.execute(query, int(adminID))

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
            stmt = "UPDATE admins SET email = %s, password = %s, salt = %s WHERE adminID = %s"
            app.cursor.execute(stmt, (adminEmail, adminPassword, adminSalt, adminID))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"email": adminEmail, "password": adminPassword, "salt": adminSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete an admin from the database, errors if the admin does not exist in the database
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
            query = "SELECT adminID, email, password, salt, accountCreationTime FROM admins WHERE email = %s"
            app.cursor.execute(query, email)

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
    
    # updates admin's passwordCode
    def put(self):
        email = emailParser.parse_args()
        adminEmail = email["email"]

        passwordCode = passwordCodeParser.parse_args()
        adminPasswordCode = passwordCode["passwordCode"]
        adminSalt = passwordCode["salt"]

        try:
            if adminPasswordCode == "":
                stmt = "UPDATE admins SET passwordCode = NULL, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (adminSalt, adminEmail))
            else:
                stmt = "UPDATE admins SET passwordCode = %s, salt = %s WHERE email = %s"
                app.cursor.execute(stmt, (adminPasswordCode, adminSalt, adminEmail))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"email": adminEmail, "passwordCode": adminPasswordCode, "salt": adminSalt}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400