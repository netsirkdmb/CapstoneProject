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


from flask import Flask, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
import yaml
import traceback
from adminsAPI import *
from usersAPI import *
from awardTypesAPI import *
from awardsAPI import *
from businessIntelligenceAPI import *

app = Flask(__name__, static_folder="upload", static_url_path="/images")
api = Api(app)
app.mysql = MySQL()

# MySQL configurations
f = open("/api/src/MySQLPasswords.yaml")
configDict = yaml.load(f)
app.config.update(configDict)

app.mysql.init_app(app)


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
api.add_resource(CreateAward, '/getAwardCreationInfo/<int:awardID>')
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
    # context = ("cert.crt", "key.key")
    # app.run(ssl_context=context, debug=False, port=5600, host="0.0.0.0")
    app.run(debug=False, port=5600, host="0.0.0.0")