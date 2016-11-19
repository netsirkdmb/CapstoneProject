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
import arrow
import shutil
import os

# parser for creating/updating awards
awardParser = reqparse.RequestParser(bundle_errors=True)
awardParser.add_argument("receiverID", type=int, help="The user that is getting the award.", required=True)
awardParser.add_argument("giverID", type=int, help="The user that is giving the award.", required=True)
awardParser.add_argument("typeID", type=int, help="The type of award being given.", required=True)
awardParser.add_argument("awardDate", type=str, help="The date award is being given.", required=True)


class AwardsList(Resource):
    # get a list of all of the awards in the database
    def get(self):
        try:
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
            stmt = "INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (%s, %s, %s, %s)"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"receiverID": awardReceiverID, "giverID": awardGiverID, "typeID": awardTypeID, "awardDate": awardDate}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
    
    # update award without awardID error
    def put(self):
        return {"Status": "Fail", "Message": "You are not allowed do a bulk update of all awards."}, 400
    
    # delete all of the awards in the database
    def delete(self):
        try:
            stmt = "DELETE FROM awards"
            app.cursor.execute(stmt)

            app.conn.commit()

            return {"Status": "Success", "Message": "awards table is now empty."}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class Award(Resource):
    # get award with matching awardID if it exists
    def get(self, awardID):
        try:
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
            stmt = "UPDATE awards SET receiverID = %s, giverID = %s, typeID = %s, awardDate = %s WHERE awardID = %s"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate, awardID))

            app.conn.commit()

            return {"Status": "Success", "Data": [{"receiverID": awardReceiverID, "giverID": awardGiverID, "typeID": awardTypeID, "awardDate": awardDate}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a award from the database, errors if the award does not exist in the database
    def delete(self, awardID):
        try:
            stmt = "DELETE FROM awards WHERE awardID = %s"
            app.cursor.execute(stmt, awardID)

            app.conn.commit()

            message = str(awardID) + " has now been deleted from awards table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


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
            
            project = "/api/src/"
            pdf_d = "{0}pdf/".format(project)
            
            build_d = "{0}build/".format(project)
            out_file = "{0}tempFile".format(build_d)
            ## code to do certificate with variables
            test_file = "{0}certificate.tex".format(build_d)

            theDay, theMonth, theYear = convertDate(awardData[0]["awardDate"])
            signature = "/api/src/upload/" + awardData[0]["giverSignatureImage"]

            # open certificate.tex for reading and replace variables
            with open(test_file, "r") as rf:
                fileContentsStr = rf.read()
                fileContentsStr = fileContentsStr.replace("###awardType###", awardData[0]["awardType"])
                fileContentsStr = fileContentsStr.replace("###giverName###", awardData[0]["giverName"])
                fileContentsStr = fileContentsStr.replace("###receiverName###", awardData[0]["receiverName"])
                fileContentsStr = fileContentsStr.replace("###theDay###", theDay)
                fileContentsStr = fileContentsStr.replace("###theMonth###", theMonth)
                fileContentsStr = fileContentsStr.replace("###theYear###", theYear)
                fileContentsStr = fileContentsStr.replace("###giverSignatureImage###", signature)

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