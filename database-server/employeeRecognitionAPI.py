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
# - for help with defining variables in LaTeX                                                 #
#       http://latex-community.org/forum/viewtopic.php?t=21390                                #
# - for help with MySQL queries between two dates                                             #
#       http://stackoverflow.com/questions/9511409/creating-a-list-of-month-names-between-two-dates-in-mysql
# - for help with MySQL queries and ranking                                                   #
#       http://stackoverflow.com/questions/24118393/mysql-rank-with-ties                      #
# - for help copying files from one directory to another                                      #
#       http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
# - for help running Apache with https                                                        #
#       http://superuser.com/questions/915356/proper-apache-redirection-from-http-to-https    #
###############################################################################################


from flask import Flask, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
import os
import shutil
import yaml
import traceback
from adminsAPI import *
from usersAPI import *
from awardTypesAPI import *
from awardsAPI import *
from businessIntelligenceAPI import *
from flask_mail import Mail, Message

app = Flask(__name__, static_folder="upload", static_url_path="/images")
api = Api(app)
app.mysql = MySQL()

# MySQL configurations
f = open("/api/src/MySQLPasswords.yaml")
mysqlConfigDict = yaml.load(f)
app.config.update(mysqlConfigDict)

app.mysql.init_app(app)

# Email configuration
f = open("/api/src/EmailPasswords.yaml")
emailConfigDict = yaml.load(f)
app.config.update(emailConfigDict)

# create mail object
app.mail = Mail()
app.mail.init_app(app)


@app.after_request
def after_request(response):
    app.cursor.close()
    app.conn.close()

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.before_request
def before_request():
    app.conn = app.mysql.connect()
    app.cursor = app.conn.cursor()


def clearTables():
    app.cursor.callproc('spResetTables')
    data = app.cursor.fetchall()
    if len(data) == 0:
        app.conn.commit()

        project = "/api/src/"

        # delete all images from upload folder
        upload_d = os.path.join(project, "upload")
        for item in os.listdir(upload_d):
            f = os.path.join(upload_d, item)
            os.remove(f)
        
        # delete any remaining temporary certificate files in build and pdf folders
        build_d = os.path.join(project, "build")
        f = "certificate"
        for item in os.listdir(build_d):
            if item.startswith(f):
                item = os.path.join(build_d, item)
                os.remove(item)
        pdf_d = os.path.join(project, "pdf")
        for item in os.listdir(pdf_d):
            if item.startswith(f):
                item = os.path.join(pdf_d, item)
                os.remove(item)

        return {"Status": "Success"}, 200
    else:
        return {"Status": "Fail", "Message": data}, 400


class ResetTables(Resource):
    def post(self):
        try:
            result = clearTables()

            return result
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


# copy all files in src directory to dst directory
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        shutil.copy2(s, d)


class AddDummyData(Resource):
    def post(self):
        data = None

        try:
            clearTables()
            app.cursor.callproc('spAddDummyData')
            data = app.cursor.fetchall()

        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400
        
        if len(data) == 0:
            app.conn.commit()

            project = "/api/src/"
            dummyFiles_d = os.path.join(project, "dummyFiles")
            upload_d = os.path.join(project, "upload")
            copytree(dummyFiles_d, upload_d)

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
api.add_resource(AwardUser, '/userAwards/<int:userID>')
api.add_resource(ResetTables, '/resetTables')
api.add_resource(AddDummyData, '/resetTablesWithDummyData')
api.add_resource(CreateAward, '/createAwardPDF/<int:awardID>')
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
api.add_resource(SignatureImage, '/uploadSignatureImage/<int:userID>')


if __name__ == "__main__":
    # context = ("/api/src/keys/cert.pem", "/api/src/keys/key.pem")
    # app.run(ssl_context=context, debug=False, port=5600, host="0.0.0.0")
    app.run(debug=False, port=5600, host="0.0.0.0")