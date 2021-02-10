from flask import Flask, url_for, render_template, jsonify
from flask import request
from flask_cors import CORS
from markupsafe import escape

import sqlite3
from sqlite3 import Error

import template_db_fethcer

app = Flask(__name__)
CORS(app)

@app.route('/')

def index():
    return 'MEETING APP PLS GIVE US A FIRST'



@app.route('/hostmain', methods=["POST"])
def hostmain():
    info = request.get_json()
    if info == None:
        return "No hostID provided"
    print(info)
    try:
        hostID = info["hostid"]
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            #get all the 
            query = "SELECT * FROM MEETING WHERE MEETING.HostID = " + hostID
            cur.execute(query)
            row_headers=[x[0] for x in cur.description]
            data = cur.fetchall()
            returnData = []
            for each in data:
                returnData.append(dict(zip(row_headers, each)))
            print(data)

            return jsonify(returnData)
    except:
        return ("nope not wokring",400)



@app.route('/meetingview', methods=["POST"])
def meetingview():
    #variable for each emotion 
    #add the totals? maybe? idk
    # dont care about technical problems after the meeting 
    # need to decide what info we want to present
    info = request.get_json()
    if info == None:
        return "No meeitn ID"
    print(info)
    try:
        meetingID = info["meetingid"]
        print(meetingID)
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = "select GeneralText, Emotion, FTime, Rating, UF.CompanyID, A.Anonymous, AT.Username from FEEDBACK INNER JOIN USERFEEDBACK as UF on UF.FeedbackID = FEEDBACK.FeedbackID INNER JOIN ATTENDANCE as A on A.MeetingID = UF.MeetingID and A.CompanyID = UF.CompanyID LEFT JOIN ATTENDEE as AT on AT.CompanyID = A.CompanyID and A.Anonymous = 0 where UF.MeetingID = " + meetingID
            cur.execute(query)
            row_headers=[x[0] for x in cur.description]
            data = cur.fetchall()
            returnData = []
            for each in data:
                if each[1] != "Technical":
                    x = each[1].split(",")
                    y = each[3].split(",")
                    print(x)
                    print(y)
                returnData.append(dict(zip(row_headers, each)))
            print(data)
            return jsonify(returnData)
    except:
        return ("nope not wokring",400)


@app.route('/userfeedback', methods=["POST"])
def userfeedback():
    info = request.get_json()
    if info == None:
        return "No feedback there"
    print(info)
    try:
        generaltext = info["generaltext"]
        emotion = info["emotion"]
        timeSent = info["ftime"]
        rating = info["rating"]
        meetingID = info["meetingid"]
        companyID = info["companyid"]
        print("here")
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            # we probs want to make a sequence
            query = "INSERT INTO FEEDBACK VALUES(NULL, '" + generaltext + "', '" + emotion + "', '" + timeSent + "', '"+ rating +"')"
            #query = "INSERT into FEEDBACK values(?, ?, ?, ?, ?)", 
            #query = "SELECT * FROM FEEDBACK"
            print("here1.5")
            print(query)
            cur.execute(query)
            query2 = "INSERT INTO USERFEEDBACK VALUES(last_insert_rowid(), "+ meetingID +", "+ companyID +") "
            cur.execute(query2)

            print("Success")
            con.commit()
            return "SUCCESS???"
    except:
        return ("nope not wokring",400)


@app.route('/newmeeting', methods=["POST"])
def newmeeting():
    info = request.get_json()
    if info == None:
        return "No feedback there"
    print(info)
    try:
        hostID = info["hostid"]
        templateID = info["templateid"]
        meetingname = info["meetingname"]
        duration = info["duration"]
        category = info["category"]
        startTime = info["starttime"]
        print(startTime)
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = "INSERT INTO MEETING VALUES(NULL, " + hostID + ", " + templateID + ", '" + meetingname + "', "+ duration +", '" + category + "' , DATETIME('"+startTime +"') )"
            print(query)
            cur.execute(query)
            print("Success")
            con.commit()
            return "SUCCESS???"
    except:
        return ("nope not wokring",400)





@app.route('/login', methods=["POST"])

def login():
    info = request.get_json()
    if info == None:
        return "No login information was provided"
    print("Info")
    print(info)
    #Dont actually know what to do if parsing fails. info will be an error
    try:
        username = info["username"]
        password = info["password"]

        #logic to determine if the user is in the database,
        if username in ["Nkosi", "Vita", "Caleb", "Dominika", "Megan", "Joe"]:
            return "Successful Login"# automatic 200 status code
        else:
            return ("User not found", 401) # tuples in this form are automatically (Response, status code)
    except:
        #Likely error is that the request did not have the fields we wanted from it
        return ("Bad Request, probably missing the data we want", 400)
    

@app.route('/dataprinter', methods=["POST"])

def dataPrintyer():
    info = request.get_json()
    if info == None:
        return "No login information was provided"

    #Dont actually know what to do if parsing fails. info will be an error
    for field in info:
        print("{} : {}".format(str(field), str(info[field])))
    return "Printed!"

@app.route('/datagetter', methods=["GET"])
def dataGetter():
    #imagine we do some authentification here, by looking at cookies, or the header
    return {
	"text":"This is different text",
	"boolean":True,
	"extra":"could be anything really",
	"morejson":{
		"mj1":"nested json",
		"mj2":3
	},
	"id":124
}

@app.route('/user/<username>')

def profile(username):
    if username == 'Susan':
        return 'lol meme'
    if username == 'template':
        rows = template_db_fethcer.get_template_from_database('database.db')
        for row in rows:
            return(str(row))
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('profile', username='Susan'))
    print(url_for('profile', username='template'))