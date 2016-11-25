###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This is the awards portion of the employee recognition system API.             #
# References:                                                                                 #
# - for help with LaTeX in Python                                                             #
#       http://akuederle.com/Automatization-with-Latex-and-Python-1                           #
# - for help with defining variables in LaTeX                                                 #
#       http://latex-community.org/forum/viewtopic.php?t=21390                                #
# - for help with Flask-mail                                                                  #
#       https://pythonhosted.org/Flask-Mail/                                                  #
###############################################################################################


from flask import Flask, request, current_app as app
from flask_restful import Resource, reqparse, inputs
import traceback
import arrow
import shutil
import os
import random
import sys
from validation import *
from flask_mail import Mail, Message


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
            if not datetimeValidation(awardDate):
                raise Exception("Award Date is not a valid datetime.")
            
            stmt = "INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (%s, %s, %s, %s)"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate))

            app.conn.commit()

            if app.cursor.rowcount == 0:
                raise Exception("Award not added to database due to invalid foreign keys for giver, receiver, or type.")

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

            if app.cursor.rowcount == 0:
                raise Exception("Award does not exist in the database.") 

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
            if not datetimeValidation(awardDate):
                raise Exception("Award Date is not a valid datetime.")
            
            stmt = "UPDATE awards SET receiverID = %s, giverID = %s, typeID = %s, awardDate = %s WHERE awardID = %s"
            app.cursor.execute(stmt, (awardReceiverID, awardGiverID, awardTypeID, awardDate, awardID))

            app.conn.commit()

            if app.cursor.rowcount == 0:
                raise Exception("Award cannot be updated because it does not exist in the database.")

            return {"Status": "Success", "Data": [{"receiverID": awardReceiverID, "giverID": awardGiverID, "typeID": awardTypeID, "awardDate": awardDate}]}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

    # delete a award from the database, database is not changed if the award does not exist in the database
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

            if app.cursor.rowcount == 0:
                raise Exception("Award does not exist in the database.")

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
            tempFile = "certificate"
            out_file = build_d + tempFile

            rnd = random.SystemRandom()
            randomNum = str(rnd.randint(1, sys.maxint))
            out_file = out_file + randomNum
            tempFile = tempFile + randomNum

            ## code to do certificate with variables
            base_file = "{0}templateCertificate.tex".format(build_d)

            theDay, theMonth, theYear = convertDate(awardData[0]["awardDate"])
            signature = "/api/src/upload/" + awardData[0]["giverSignatureImage"]

            # open certificate.tex for reading and replace variables
            with open(base_file, "r") as rf:
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

            emailFileName = pdf_d + tempFile + ".pdf"
            fileName = tempFile + ".pdf"

            receiverEmail = awardData[0]["receiverEmail"]
            bodyText = "<p>Congratulations on receiving the " + awardData[0]["awardType"] + " award! Here is a copy of your award certificate!</p>"

            # message to send to the recipient
            msg = Message(subject="You have received an award for your hard work at Angama!", sender="noreply@employeerecognitionangama.co.uk", recipients=[receiverEmail], bcc=["dhusek@oregonstate.edu"], html=bodyText)
            
            with app.open_resource(emailFileName) as fp:
                msg.attach(fileName, "application/pdf", fp.read())
            
            # send
            app.mail.send(msg)
        
            # delete temp certificate files from build directory
            for item in os.listdir("."):
                if item.startswith(tempFile):
                    item = os.path.join(build_d, item)
                    os.remove(item)
            
            # delete temp certificate files from pdf directory
            for item in os.listdir(pdf_d):
                if item.startswith(tempFile):
                    item = os.path.join(pdf_d, item)
                    os.remove(item)


            return {"Status": "Success", "Data": awardData}, 200

        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400