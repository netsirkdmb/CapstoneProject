###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This is the award types portion of the employee recognition system API.        #
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