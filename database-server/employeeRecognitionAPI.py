###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This API is hosted on Amazon Web Services and allows the user and admin sites
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
###############################################################################################


from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL
import bson
import json

app = Flask(__name__)
api = Api(app)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = "dhusek"
app.config['MYSQL_DATABASE_PASSWORD'] = "oX^an26CROYrtfIcv!6LtVotx^GwRP"
app.config['MYSQL_DATABASE_DB'] = "cs419"
app.config['MYSQL_DATABASE_HOST'] = "cs419-employee-recognition.cquogdmskuf6.us-west-2.rds.amazonaws.com"

# request parsers to validate input
# parser for creating admins
adminAccountParser = reqparse.RequestParser(bundle_errors=True)
adminAccountParser.add_argument("uuID", type=str, help="uuID for new admin.", required=True)
adminAccountParser.add_argument("email", type=str, help="Email address for new admin.", required=True)
adminAccountParser.add_argument("password", type=str, help="Password for new admin.", required=True)

# parser for creating users
userAccountParser = reqparse.RequestParser(bundle_errors=True)
userAccountParser.add_argument("uuID", type=str, help="uuID for new user.", required=True)
userAccountParser.add_argument("name", type=str, help="Name for new user.", required=True)
userAccountParser.add_argument("email", type=str, help="Email address for new user.", required=True)
userAccountParser.add_argument("password", type=str, help="Password for new user.", required=True)
userAccountParser.add_argument("signatureImage", type=str, help="Signature for new user.", required=True)
userAccountParser.add_argument("region", type=str, help="Region for new user.", required=True)

# parser for creating awardTypes
awardTypeParser = reqparse.RequestParser(bundle_errors=True)
awardTypeParser.add_argument("name", type=str, help="Name for new award type.", required=True)
awardTypeParser.add_argument("prestigeLevel", type=int, help="Prestige level for new award type.", required=True)

# parser for creating awards
awardParser = reqparse.RequestParser(bundle_errors=True)
awardParser.add_argument("receiverID", type=int, help="The user that is getting the award.", required=True)
awardParser.add_argument("giverID", type=int, help="The user that is giving the award.", required=True)
awardParser.add_argument("typeID", type=int, help="The type of award being given.", required=True)

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

            query = "SELECT adminID, uuID, email, password FROM admins"
            app.cursor.execute(query)

            admins = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": admins}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
    # create a new admin in the database
    def post(self):
        admin = adminAccountParser.parse_args()

        admin_uuID = admin["uuID"]
        adminEmail = admin["email"]
        adminPassword = admin["password"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO admins (uuID, email, password) VALUES (%s, %s, %s)"
            app.cursor.execute(stmt, (admin_uuID, adminEmail, adminPassword))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [admin_uuID, adminEmail, adminPassword]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class Admin(Resource):
    # get admin with matching adminID if it exists
    def get(self, adminID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT adminID, uuID, email, password FROM admins WHERE adminID = %s"
            app.cursor.execute(query, int(adminID))

            admins = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": admins}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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

            return {"Status": "Success", "Data": [adminEmail, adminPassword]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class UsersList(Resource):
    # get a list of all of the users in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT userID, uuID, name, email, password, signatureImage, region FROM users"
            app.cursor.execute(query)

            users = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": users}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
    # create a new user in the database
    def post(self):
        user = userAccountParser.parse_args()

        user_uuID = user["uuID"]
        userName = user["name"]
        userEmail = user["email"]
        userPassword = user["password"]
        userSignature = user["signatureImage"]
        userRegion = user["region"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO users (uuID, name, email, password, signatureImage, region) VALUES (%s, %s, %s, %s, %s, %s)"
            app.cursor.execute(stmt, (user_uuID, userName, userEmail, userPassword, userSignature, userRegion))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [user_uuID, userName, userEmail, userPassword, userSignature, userRegion]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class User(Resource):
    # get user with matching userID if it exists
    def get(self, userID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT userID, uuID, name, email, password, signatureImage, region FROM users WHERE userID = %s"
            app.cursor.execute(query, int(userID))

            users = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": users}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

    # insert user with userID error
    def post(self, userID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the user that you are creating."}, 400

    # update user in database, errors if the user does not exist in the database
    def put(self, userID):
        user = userAccountParser.parse_args()

        userName = user["name"]
        userEmail = user["email"]
        userPassword = user["password"]
        userSignature = user["signatureImage"]
        userRegion = user["region"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "UPDATE users SET name = %s, email = %s, password = %s, signatureImage = %s, region = %s WHERE userID = %s"
            app.cursor.execute(stmt, (userName, userEmail, userPassword, userSignature, userRegion, userID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [userName, userEmail, userPassword, userSignature, userRegion]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class AwardTypesList(Resource):
    # get a list of all of the award types in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT awardTypeID, name, prestigeLevel FROM awardTypes"
            app.cursor.execute(query)

            awardTypes = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardTypes}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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

            return {"Status": "Success", "Data": [awardTypeName, awardTypePrestige]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class AwardType(Resource):
    # get award type with matching awardTypeID if it exists
    def get(self, awardTypeID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = "SELECT awardTypeID, name, prestigeLevel FROM awardTypes WHERE awardTypeID = %s"
            app.cursor.execute(query, int(awardTypeID))

            awardTypes = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awardTypes}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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

            return {"Status": "Success", "Data": [awardTypeName, awardTypePrestige]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class AwardsList(Resource):
    # get a list of all of the awards in the database
    def get(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = ("SELECT a.awardID, "
                    "a.receiverID, "
                    "rec.name AS receiverName, "
                    "a.giverID, giv.name AS giverName, "
                    "a.typeID, atyp.name AS awardType FROM cs419.awards a INNER JOIN "
                    "users rec ON a.receiverID = rec.userID INNER JOIN "
                    "users giv ON a.giverID = giv.userID INNER JOIN "
                    "awardTypes atyp ON a.typeID = atyp.awardTypeID")
            app.cursor.execute(query)

            awards = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awards}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
    # create a new award in the database
    def post(self):
        award = awardParser.parse_args()

        awardReceiverID = award["receiverID"]
        awardGiverID = award["giverID"]
        awardTypeID = award["typeID"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "INSERT INTO awards (receiverID, giverID, typeID) VALUES (%s, %s, %s)"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [awardReceiverID, awardGiverID, awardTypeID]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class Award(Resource):
    # get award with matching awardID if it exists
    def get(self, awardID):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            query = ("SELECT a.awardID, "
                    "a.receiverID, "
                    "rec.name AS receiverName, "
                    "a.giverID, giv.name AS giverName, "
                    "a.typeID, atyp.name AS awardType FROM cs419.awards a INNER JOIN "
                    "users rec ON a.receiverID = rec.userID INNER JOIN "
                    "users giv ON a.giverID = giv.userID INNER JOIN "
                    "awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE a.awardID = %s")
            app.cursor.execute(query, int(awardID))

            awards = list(app.cursor.fetchall())

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": awards}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

    # insert award with awardID error
    def post(self, awardID):
        return {"Status": "Fail", "Message": "You are not allowed to choose the ID for the award that you are creating."}, 400

    # update award in database, errors if the award does not exist in the database
    def put(self, awardID):
        award = awardParser.parse_args()

        awardReceiverID = award["receiverID"]
        awardGiverID = award["giverID"]
        awardTypeID = award["typeID"]

        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            stmt = "UPDATE awards SET receiverID = %s, giverID = %s, typeID = %s WHERE awardID = %s"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardID))

            app.conn.commit()

            app.cursor.close()
            app.conn.close()

            return {"Status": "Success", "Data": [awardReceiverID, awardGiverID, awardTypeID]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class ResetTables(Resource):
    def post(self):
        try:
            app.conn = mysql.connect()
            app.cursor = app.conn.cursor()

            result = clearTables()

            app.cursor.close()
            app.conn.close()

            return result
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class AddDummyData(Resource):
    def post(self):
        data = None

        app.conn = mysql.connect()
        app.cursor = app.conn.cursor()

        try:
            clearTables()
            app.cursor.callproc('spAddDummyData')
            data = app.cursor.fetchall()
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
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


# create routes for API
api.add_resource(AdminsList, '/admins')
api.add_resource(Admin, '/admins/<int:adminID>')
api.add_resource(UsersList, '/users')
api.add_resource(User, '/users/<int:userID>')
api.add_resource(AwardTypesList, '/awardTypes')
api.add_resource(AwardType, '/awardTypes/<int:awardTypeID>')
api.add_resource(AwardsList, '/awards')
api.add_resource(Award, '/awards/<int:awardID>')
api.add_resource(ResetTables, '/resetTables')
api.add_resource(AddDummyData, '/resetTablesWithDummyData')


if __name__ == "__main__":
    app.run(debug=False, port=5600, host='0.0.0.0')
