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
from flask_restful import Resource
import traceback
import datetime


def convertMonth(mon):
    if mon == 1:
        return "January"
    elif mon == 2:
        return "February"
    elif mon == 3:
        return "March"
    elif mon == 4:
        return "April"
    elif mon == 5:
        return "May"
    elif mon == 6:
        return "June"
    elif mon == 7:
        return "July"
    elif mon == 8:
        return "August"
    elif mon == 9:
        return "September"
    elif mon == 10:
        return "October"
    elif mon == 11:
        return "November"
    else:
        return "December"


class FreqChart(Resource):
    # get the count of awards being given in the previous 12 months
    def get(self):
        try:
            query = """SELECT y, m, Count(a.awardDate) AS count FROM
                    (SELECT y, m FROM
                    (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years,
                    (SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
                    UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12) months) ym
                    LEFT JOIN cs419.awards a ON ym.y = YEAR(a.awardDate) AND ym.m = MONTH(a.awardDate)
                    WHERE (y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE()))
                    GROUP BY y, m"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["frequency"]) = row
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AnnualAwardTypes(Resource):
    # get the award types being given in the previous 12 months
    def get(self):
        try:
            query = """SELECT a.typeID as typeID, aTyp.name as name, aTyp.prestigeLevel as prestigeLevel, Count(a.typeID) AS count FROM
                    (SELECT y, m FROM
                    (SELECT YEAR(CURDATE()) y UNION ALL SELECT YEAR(CURDATE())-1) years,
                    (SELECT 1 m UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 
                    UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12) months) ym
                    RIGHT JOIN cs419.awards a ON ym.y = YEAR(a.awardDate) AND ym.m = MONTH(a.awardDate)
					INNER JOIN cs419.awardTypes aTyp ON a.typeID = aTyp.awardTypeID
					WHERE (y=YEAR(CURDATE()) AND m<=MONTH(CURDATE())) OR (y<YEAR(CURDATE()) AND m>MONTH(CURDATE())) 
                    GROUP BY typeID"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["tyepID"], 
                rowInfo["name"], 
                rowInfo["value"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400

class EmployeeRank(Resource):
    # get the employee's all-time ranking based on awards received
    def get(self, userID):
        try:
            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                    FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                    LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                    GROUP BY u.userID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z WHERE z.userID = %s"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"],
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["prestige"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["prestige"] = int(rowInfo["prestige"])
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AllEmployeeRank(Resource):
    # get the all-time ranking based on awards received
    def get(self):
        try:
            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                    FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                    LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                    GROUP BY u.userID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z"""
            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"],
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["prestige"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["prestige"] = int(rowInfo["prestige"])
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class EmployeePrestigePoints(Resource):
    # get the prestige points for the awards the employee has received each month over their career
    def get(self, userID):
        try:
            query = """SELECT YEAR(aDate) AS year, MONTH(aDate) AS month, COALESCE(h.points, 0) AS points FROM (
                    SELECT @maxDate - INTERVAL (a.a+(10*b.a)+(100*c.a)+(1000*d.a) + (10000*e.a)) day aDate FROM
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a, /*10 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b, /*100 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c, /*1000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d, /*10000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) e, /*100000 day range*/
                    (SELECT @minDate := (SELECT startDate FROM users WHERE userID = %s), @maxDate := CURDATE()) f
                    ) g LEFT JOIN (SELECT YEAR(a.awardDate) AS ay, MONTH(a.awardDate) AS am, SUM(atyp.prestigeLevel) AS points FROM users u 
                        INNER JOIN awards a ON u.userID = a.receiverID 
                        INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                        WHERE u.userID = %s
                        GROUP BY YEAR(a.awardDate) DESC, MONTH(a.awardDate) DESC) h ON h.ay = YEAR(aDate) AND h.am = MONTH(aDate)
                    WHERE aDate BETWEEN @minDate AND @maxDate
                    GROUP BY year DESC, month DESC"""
            app.cursor.execute(query, (int(userID), int(userID)))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["points"]) = row
                rowInfo["year"] = int(rowInfo["year"])
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowInfo["points"] = int(rowInfo["points"])
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class EmployeeAwardTypes(Resource):
    # get the award types the employee has received over their career
    def get(self, userID):
        try:
            query = """SELECT atyp.awardTypeID AS typeID, 
                    atyp.name as awardName, 
                    atyp.prestigeLevel AS value, 
                    COUNT(atyp.name) as frequency FROM users u 
                    INNER JOIN awards a ON u.userID = a.receiverID 
                    INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                    WHERE u.userID = %s
                    GROUP BY atyp.name ASC"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["tyepID"], 
                rowInfo["name"], 
                rowInfo["value"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            return {"Status": "Success", "Results": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUserReceived(Resource):
    # get all awards that userID has received
    def get(self, userID):
        try:
            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE rec.userID = %s
					ORDER BY a.awardDate DESC"""
            app.cursor.execute(query, int(userID))

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


class AwardUserGivenFreq(Resource):
    # get the frequency of awards that userID has given
    def get(self, userID):
        try:
            query = """SELECT YEAR(aDate) AS year, MONTH(aDate) AS month, COALESCE(h.count, 0) AS count FROM (
                    SELECT @maxDate - INTERVAL (a.a+(10*b.a)+(100*c.a)+(1000*d.a) + (10000*e.a)) day aDate FROM
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a, /*10 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b, /*100 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c, /*1000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) d, /*10000 day range*/
                    (SELECT 0 AS a UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL
                    SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) e, /*100000 day range*/
                    (SELECT @minDate := (SELECT startDate FROM users WHERE userID = %s), @maxDate := CURDATE()) f
                    ) g LEFT JOIN (SELECT YEAR(a.awardDate) AS ay, MONTH(a.awardDate) AS am, count(a.awardDate) as count FROM users u 
                        INNER JOIN awards a ON u.userID = a.giverID 
                        WHERE u.userID = %s
                        GROUP BY YEAR(a.awardDate) DESC, MONTH(a.awardDate) DESC) h ON h.ay = YEAR(aDate) and h.am = MONTH(aDate)
                    WHERE aDate BETWEEN @minDate AND @maxDate
                    GROUP BY year DESC, month DESC"""
            app.cursor.execute(query, (int(userID), int(userID)))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["year"], 
                rowInfo["month"], 
                rowInfo["frequency"]) = row
                rowInfo["month"] = convertMonth(rowInfo["month"])
                rowList.append(rowInfo)

            return {"Status": "Success", "Data": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUserGivenTypes(Resource):
    # get the frequency of types of awards that userID has given
    def get(self, userID):
        try:
            query = """SELECT atyp.name as awardName, COUNT(atyp.name) as frequency FROM users u 
                    INNER JOIN awards a ON u.userID = a.giverID 
                    INNER JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID
                    WHERE u.userID = %s
                    GROUP BY atyp.name ASC"""
            app.cursor.execute(query, int(userID))

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["type"], 
                rowInfo["frequency"]) = row
                rowList.append(rowInfo)

            return {"Status": "Success", "Data": rowList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class TopEmployees(Resource):
    def get(self):
        # get current month
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        year = int(year)
        monthList = []
        for i in range(12):
            monthNum = (int(month) - i) % 12
            if monthNum == 0:
                monthNum = 12
                year -= 1
            monthList.append((monthNum, year))

        try:
            resultsList = {}

            for i in range(len(monthList)):
                queryMonth, queryYear = monthList[i]

                query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                        (SELECT x.userID, x.name, x.points, 
                        @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                        IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                        (SELECT u.userID, u.name AS name, COALESCE(SUM(atyp.prestigeLevel), 0) AS points 
                        FROM users u LEFT JOIN awards a ON u.userID = a.receiverID 
                        LEFT JOIN awardTypes atyp ON a.typeID = atyp.awardTypeID 
                        WHERE MONTH(a.awardDate) = %s AND YEAR(a.awardDate) = %s GROUP BY u.userID) x,
                        (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                        ORDER BY x.points DESC, x.userID ASC) z LIMIT 5"""
                app.cursor.execute(query, (queryMonth, queryYear))

                rows = list(app.cursor.fetchall())
                
                if len(rows) != 0:
                    rowList = []
                    for row in rows:
                        rowInfo = {}
                        (rowInfo["userID"], 
                        rowInfo["name"], 
                        rowInfo["rank"], 
                        rowInfo["points"]) = row
                        rowInfo["rank"] = int(rowInfo["rank"])
                        rowInfo["points"] = int(rowInfo["points"])
                        rowList.append(rowInfo)
                    
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = rowList
                else:
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = [0]
            
            query = """SELECT z.userID, z.name, z.rank, z.points FROM 
                    (SELECT x.userID, x.name, x.points, 
                    @prev := @curr, @curr := x.points, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.points, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT z.receiverID AS userID, z.receiverName AS name, SUM(z.points) AS points FROM
					(SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.typeID, atyp.name AS awardType, atyp.prestigeLevel AS points,
                    a.awardDate FROM
					(SELECT @minDate := DATE_SUB(CURDATE(),INTERVAL 1 YEAR), @maxDate := CURDATE()) f INNER JOIN
					cs419.awards a ON a.awardDate > @minDate AND a.awardDate <= @maxDate INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID
					ORDER BY a.awardDate DESC) z
					GROUP BY z.receiverID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.points DESC, x.userID ASC) z LIMIT 5"""

            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"], 
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["points"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["points"] = int(rowInfo["points"])
                rowList.append(rowInfo)
            
            resultsList["Year"] = rowList

            return {"Status": "Success", "Results": resultsList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class MostGenerous(Resource):
    def get(self):
        # get current month
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        year = int(year)
        monthList = []
        for i in range(12):
            monthNum = (int(month) - i) % 12
            if monthNum == 0:
                monthNum = 12
                year -= 1
            monthList.append((monthNum, year))

        try:
            resultsList = {}

            for i in range(len(monthList)):
                queryMonth, queryYear = monthList[i]

                query = """SELECT z.userID, z.name, z.rank, z.frequency FROM 
                    (SELECT x.userID, x.name, x.frequency, 
                    @prev := @curr, @curr := x.frequency, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.frequency, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT u.userID AS userID, u.name AS name, COUNT(a.awardDate) AS frequency FROM
					users u INNER JOIN awards a ON u.userID = a.giverID 
                    WHERE MONTH(a.awardDate) = %s AND YEAR(a.awardDate) = %s GROUP BY u.userID) x,
					(SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
					ORDER BY x.frequency DESC, x.userID ASC) z LIMIT 5"""
                app.cursor.execute(query, (queryMonth, queryYear))

                rows = list(app.cursor.fetchall())
                
                if len(rows) != 0:
                    rowList = []
                    for row in rows:
                        rowInfo = {}
                        (rowInfo["userID"], 
                        rowInfo["name"], 
                        rowInfo["rank"], 
                        rowInfo["frequency"]) = row
                        rowInfo["rank"] = int(rowInfo["rank"])
                        rowInfo["frequency"] = int(rowInfo["frequency"])
                        rowList.append(rowInfo)
                    
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = rowList
                else:
                    monthYear = "{0}-{1}".format(queryMonth, queryYear)
                    resultsList[monthYear] = [0]
            
            query = """SELECT z.userID, z.name, z.rank, z.frequency FROM 
                    (SELECT x.userID, x.name, x.frequency, 
                    @prev := @curr, @curr := x.frequency, @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
                    IF(@prev <> x.frequency, @i:=1, @i:=@i+1) AS counter FROM
                    (SELECT z.giverID AS userID, z.giverName AS name, COUNT(z.awardDate) AS frequency FROM
					(SELECT a.awardID, a.giverID, giv.name AS giverName, a.awardDate FROM
					(SELECT @minDate := DATE_SUB(CURDATE(),INTERVAL 1 YEAR), @maxDate := CURDATE()) f INNER JOIN
					cs419.awards a ON a.awardDate > @minDate AND a.awardDate <= @maxDate INNER JOIN 
                    users giv ON a.giverID = giv.userID ORDER BY a.awardDate DESC) z
					GROUP BY z.giverID) x,
                    (SELECT @curr := null, @prev := null, @rank := 1, @i := 0) tmp_tbl
                    ORDER BY x.frequency DESC, x.userID ASC) z LIMIT 5"""

            app.cursor.execute(query)

            rows = list(app.cursor.fetchall())

            rowList = []
            for row in rows:
                rowInfo = {}
                (rowInfo["userID"], 
                rowInfo["name"], 
                rowInfo["rank"], 
                rowInfo["frequency"]) = row
                rowInfo["rank"] = int(rowInfo["rank"])
                rowInfo["frequency"] = int(rowInfo["frequency"])
                rowList.append(rowInfo)
            
            resultsList["Year"] = rowList

            return {"Status": "Success", "Results": resultsList}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400


class AwardUser(Resource):
    # get all awards that userID has given
    def get(self, userID):
        try:
            query = """SELECT a.awardID, 
                    a.receiverID, 
                    rec.name AS receiverName, 
                    a.giverID, giv.name AS giverName, 
                    a.typeID, atyp.name AS awardType, 
                    a.awardDate FROM cs419.awards a INNER JOIN 
                    users rec ON a.receiverID = rec.userID INNER JOIN 
                    users giv ON a.giverID = giv.userID INNER JOIN 
                    awardTypes atyp ON a.typeID = atyp.awardTypeID WHERE giv.userID = %s"""
            app.cursor.execute(query, int(userID))

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

    # insert award with userID error
    def post(self, userID):
        return {"Status": "Fail", "Message": "To create an award that this user has given, please send a post request to /awards."}, 400

    # update awards given by user with userID error
    def put(self, userID):
        return {"Status": "Fail", "Message": "You are not allowed to do a bulk update of all the awards that the user has given."}, 400

    # delete a award from the database, errors if the award does not exist in the database
    def delete(self, userID):
        try:
            stmt = "DELETE FROM awards WHERE giverID = %s"
            app.cursor.execute(stmt, userID)

            app.conn.commit()

            message = "All awards given by " + str(userID) + " have now been deleted from awards table."

            return {"Status": "Success", "Message": message}, 200
        
        except Exception:
            return {"Status": "Fail", "Error": traceback.format_exc()}, 400