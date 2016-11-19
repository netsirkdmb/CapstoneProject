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

# parser for creating awardTypes
awardTypeParser = reqparse.RequestParser(bundle_errors=True)
awardTypeParser.add_argument("name", type=str, help="Name for new award type.", required=True)
awardTypeParser.add_argument("prestigeLevel", type=int, help="Prestige level for new award type.", required=True)


class AwardTypesList(Resource):
    # get a list of all of the award types in the database
    def get(self):
        try:
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

            return {"Status": "Success", "Data": awardTypesData}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # create a new award type in the database
    def post(self):
        awardType = awardTypeParser.parse_args()

        awardTypeName = awardType["name"]
        awardTypePrestige = awardType["prestigeLevel"]

        try:
            stmt = "INSERT INTO awardTypes (name, prestigeLevel) VALUES (%s, %s)"
            app.cursor.execute(stmt, (awardTypeName, awardTypePrestige))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"name": awardTypeName, "prestigeLevel": awardTypePrestige}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update award type without awardTypeID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all award types."}, 400
    
    # delete all of the award types in the database
    def delete(self):
        try:
            stmt = "DELETE FROM awardTypes"
            app.cursor.execute(stmt)

            app.conn.commit()

            return {"Status": "Success", "Message": "awardTypes table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardType(Resource):
    # get award type with matching awardTypeID if it exists
    def get(self, awardTypeID):
        try:
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
            stmt = "UPDATE awardTypes SET name = %s, prestigeLevel = %s WHERE awardTypeID = %s"
            app.cursor.execute(stmt, (awardTypeName, awardTypePrestige, awardTypeID))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"name": awardTypeName, "prestigeLevel": awardTypePrestige}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a award type from the database, errors if the award type does not exist in the database
    def delete(self, awardTypeID):
        try:
            stmt = "DELETE FROM awardTypes WHERE awardTypeID = %s"
            app.cursor.execute(stmt, awardTypeID)

            app.conn.commit()

            message = str(awardTypeID) + " has now been deleted from awardTypes table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400