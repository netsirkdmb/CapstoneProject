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
adminAccountParser.add_argument("email", type=str, help="Email address to create admin.", required=True)
adminAccountParser.add_argument("password", type=str, help="Password for new admin.", required=True)

# parser for get admins/users request
pageParser = reqparse.RequestParser(bundle_errors=True)
pageParser.add_argument("offset", type=inputs.natural)
pageParser.add_argument("limit", type=inputs.positive)

mysql.init_app(app)
app.conn = mysql.connect()
app.cursor = app.conn.cursor()


class AdminsList(Resource):
    # get a list of all of the admins in the database
    def get(self):
        try:
            query = "SELECT adminID, email, password FROM admins"
            app.cursor.execute(query)

            admins = list(app.cursor.fetchall())

            return {"Status": "Success", "Data": admins}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
    # create a new admin in the database
    def post(self):
        admin = adminAccountParser.parse_args()

        adminEmail = admin["email"]
        adminPassword = admin["password"]

        try:
            stmt = "INSERT INTO admins (email, password) VALUES (%s, %s)"
            app.cursor.execute(stmt, (adminEmail, adminPassword))

            app.conn.commit()

            return {"Status": "Success", "Data": [adminEmail, adminPassword]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
    
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
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class Admin(Resource):
    # get admin with matching adminID if it exists
    def get(self, adminID):
        try:
            query = "SELECT email, password FROM admins WHERE adminID = %s"
            app.cursor.execute(query, int(adminID))

            admins = list(app.cursor.fetchall())

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
            stmt = "UPDATE admins SET email = %s, password = %s WHERE adminID = %s"
            app.cursor.execute(stmt, (adminEmail, adminPassword, adminID))

            app.conn.commit()

            return {"Status": "Success", "Data": [adminEmail, adminPassword]}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400

    # delete an admin from the database, errors if the admin does not exist in the database
    def delete(self, adminID):
        try:
            stmt = "DELETE FROM admins WHERE adminID = %s"
            app.cursor.execute(stmt, adminID)

            app.conn.commit()

            message = str(adminID) + " has now been deleted from admins table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class ResetTables(Resource):
    def post(self):
        try:
            return clearTables()
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400


class AddDummyData(Resource):
    def post(self):
        data = None
        try:
            clearTables()
            app.cursor.callproc('spAddDummyData')
            data = app.cursor.fetchall()
        except Exception as e:
            return {"Status": "Fail", "Error": str(e)}, 400
        if len(data) == 0:
            app.conn.commit()
            return {"Status": "Success"}, 200
        else:
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
api.add_resource(ResetTables, '/resetTables')
api.add_resource(AddDummyData, '/resetTablesWithDummyData')


if __name__ == "__main__":
    app.run(debug=False, port=5600, host='0.0.0.0')
