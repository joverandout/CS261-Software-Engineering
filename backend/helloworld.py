#pip install flask
#pip install flask_socketio
#pip install flask-cors
#pip install flair (might need anaconda)

from flask import Flask, url_for, render_template, jsonify
from flask_socketio import SocketIO, emit, send
from flask import request
from flask_cors import CORS
from markupsafe import escape

import sqlite3
from sqlite3 import Error

import template_db_fethcer
from Semantic import Semantic
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dolphin'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#socket stuff but the functions wont work since the 
#python throws an error when trying to import the 
#paclets cors and socketio

if __name__ == '__main__':
    socketio.run(app)

@socketio.on('connect')
def socket_connection():
    print("\nNew Connection!\nData: ")
    print(request.args.get("foo"))
    emit('Yay a connection!', {'info': 'rmation'})
    

@socketio.on('disconnect')
def socket_disconnect():
    print('Client disconnected... \n')

@socketio.on("hello")
def handle_hello(text):
    print("\nSocket Message: "+text+"\n")



@app.route('/')
def index():
    return 'MEETING APP PLS GIVE US A FIRST'

@app.route('/sendsocketmessage', methods=["POST"])  
def sendsocketmessage():
    data = request.get_json()
    print("\nSending Message to frontend: ",data)
    
    socketio.emit("femessage",data)
    return "Sent!"

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
        return ("nope not working",400)



"""VITA
need to pass the feedback 
i dont think it requires socket as its not live 
  """
@app.route('/meetingview', methods=["POST"])
def meetingview():
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
        return ("nope not working",400)

"""VITA
Need to pass the feedback recieved back to the front end 
Via the socket - idk how to make this work byt we gon try 
also need to filter out abusive text - start with some sewar words 
  """
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
        #print("here")

        # send to the sentiment analysis 
        feedbackEval = Semantic(generaltext)
        feedbackEval.update_semValues_and_confScores()
        s = feedbackEval.get_scores()

        # going to get back an array
        print(s)

        #write swear word and filter them out 
        abusive = False
        timeConstraint = True
        if abusive == False :

            # need to chech here that the meetin is live DO THIS

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()

                #check when the last time they submitted feedback was - non technical only 
                lastFeedback = "SELECT ftime FROM FEEDBACK INNER JOIN  USERFEEDBACK AS uf ON uf.FeedbackID = FEEDBACK.FeedbackID WHERE CompanyID = "+ companyID+ " AND MeetingID = "+ meetingID + " AND feedback.emotion != 'Technical' ORDER BY feedback.FeedbackID DESC LIMIT 1;"
                #print(lastFeedback)
                cur.execute(lastFeedback)
                recentTime = cur.fetchall()
                #print("HERE")
                #print(len(recentTime))
                for each in recentTime:
                   # print("LOOP")
                   # print(each)
                    timer = each[0]
                    #print(timer)
                    timerAsTime = datetime.strptime(timer,"%H:%M:%S")
                   # print("GOT TIME COB")
                    now = datetime.now()
                    currentTime = now.strftime("%H:%M:%S")
                    #print(currentTime)
                    difference = datetime.strptime(currentTime,"%H:%M:%S") - timerAsTime
                   # print("duifeeren")
                    #print(difference.seconds)
                    if difference.seconds < 120:
                        print("Too soon")
                        timeConstraint = False
                    else:
                        print("TIME IS K")

                if timeConstraint:

                    query = "INSERT INTO FEEDBACK VALUES(NULL, '" + generaltext + "', '" + emotion + "', '" + timeSent + "', '"+ rating +"')"
                    # print("here1.5")
                    # print(query)
                    cur.execute(query)
                    #print("executed 1")
                    query2 = "INSERT INTO USERFEEDBACK VALUES(last_insert_rowid(), "+ meetingID +", "+ companyID +") "
                    cur.execute(query2)
                    #print("here 2")
                    query3 = "SELECT * FROM FEEDBACK WHERE feedbackid = last_insert_rowid()"
                    cur.execute(query3)
                    #print("here3")
                    row_headers=[x[0] for x in cur.description]
                    #print(row_headers)
                    data = cur.fetchall()
                    returnData = []
                    for each in data:
                        returnData.append(dict(zip(row_headers, each)))
                    #print(data)
                    #print("Success")
                    con.commit()
                    # i think this should work but cant properly test 
                    socketio.emit("femessage",jsonify(returnData))

                    return jsonify(returnData)
                else:
                    return "we dont want your feedback - take it easy"
        else:
            return "abusive message was sent- be nice"
    except:
        return ("nope not working",400)


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
        return ("nope not working",400)


@app.route('/newtemplate', methods=["POST"])
def newtemplate():
    info = request.get_json()
    if info == None:
        return "No feedback there"
    print(info)
    try:
        hostID = info["hostid"]
        templateName = info["templatename"]
        emotionsSelected = info["emotionsselected"]
        question = info["question"]
        with sqlite3.connect("database.db") as con:
            print("Here")
            cur = con.cursor()
            query = "INSERT INTO TEMPLATES VALUES(NULL, " + hostID + ", '" + templateName + "', '" + emotionsSelected + "', '"+ question +"')"
            print(query)
            cur.execute(query)
            print("Success")
            con.commit()
            return "SUCCESS???"
    except:
        return ("nope not working",400)


#comment

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
