#pip install flask
#pip install flask_socketio
#pip install flask-cors
#pip install flair (might need anaconda)

from flask import Flask, url_for, render_template, jsonify
from flask_socketio import SocketIO, emit, send
from flask import request
from flask_cors import CORS
from markupsafe import escape

from Meeting import Meeting
from Host import Host
from Attendee import Attendee
from datetime import datetime, timedelta
from Template import Template

import hashlib


import sqlite3
from sqlite3 import Error

import template_db_fethcer
#from Semantic import Semantic
#from Offensive import Offensive
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dolphin'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

#socket stuff but the functions wont work since the 
#python throws an error when trying to import the 
#paclets cors and socketio

currently_live_meetings = {}
still_collecting_feedback_meetings = {}

stack_of_available_codes = []
for i in range(10000, 15000):
    stack_of_available_codes.append(i)


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


@app.route('/postmeetingfeed', methods=["POST"])
def postmeetingfeed():
    info = request.get_json()
    if info == None:
        return "No feedback there"
    print(info)
    try:
        meetingID = info["meetingid"]
        postquestions = info["questionresponses"]
        timeSent = info["ftime"]
        companyID = info["companyid"]
        print(postquestions)
        if (meetingID in still_collecting_feedback_meetings):
            print("meetign collecting post feedback")
        else:
            print("NO takine feedbakc")
            #return "no longer taking feedback"
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            for each in postquestions:
                part1 = """INSERT INTO FEEDBACK VALUES(NULL, " """ + each
                part2 = """ ", '"""
                part3 = "Post' , '" + timeSent + "' , NULL, NULL)"
                print(part1+part2+part3)
                cur.execute(part1+part2+part3)
            
            return "SUCCESS??"
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

        # offEval = Offensive(generaltext)
        # offEval.update_rating()
        # howOffensive = offEval.get_scores()
        # print(howOffensive)

        # send to the sentiment analysis 
        # feedbackEval = Semantic(generaltext)
        # feedbackEval.update_semValues_and_confScores()
        # s = feedbackEval.get_scores()

        # going to get back an array
        #print(s)
        semanticAnalysis = [-0.999987,0.989999]

        #write swear word and filter them out 
        swearWords = ['fuck', 'shit', 'bollocks', 'wanker', 'asshat', 'prick','bellend','crap', 'bugger', 'dick','knob','twat', 'bitch', 'cunt']

        abusive = False
        for each in swearWords:
            if each in generaltext:
                abusive = True 

        # for each in howOffensive:
        #     if each > 0.5:
        #         abusive = True
                
        timeConstraint = True
        if abusive == False :

            # need to chech here that the meetin is live DO THIS
            #need joe to make the list of meetings 
            if(meetingID in currently_live_meetings):
                print("this meeting is still accepting feedback")
            else:
                return "MEETING NO LONGER LIVE"
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
                print(timeConstraint)
                print(str(semanticAnalysis))
                semanticsAsString = ""
                print(semanticsAsString)
                for each in semanticAnalysis:
                    print(each)
                    semanticsAsString = semanticsAsString + str(each) + ","
                print(semanticsAsString)
                semanticsAsString = semanticsAsString[:-1]
                print(semanticsAsString)
                if timeConstraint == True:
                    print("here")
                    #query = """INSERT INTO FEEDBACK VALUES(NULL, " """+ generaltext +""" ", '""" + emotion + """', '""" + timeSent + """', '"""+ rating +"""', ' """ + semanticAnalysis + ""')"""
                    part1 = """INSERT INTO FEEDBACK VALUES(NULL, " """ + generaltext
                    part2 = """ ", '""" + emotion 
                    part3 = "' , '" + timeSent + "' , '"+rating + "', '" + semanticsAsString + "')"
                    # print("here1.5")
                    print(part1 + part2 + part3)
                    #print(query)
                    cur.execute(part1 + part2 + part3)
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
                        if each[2] == "Technical":
                            print("its technical")
                            newDict = dict()
                            newDict[each[2]] = each[1]
                            print(newDict)
                            returnData.append(newDict)
                        else:
                            print(each)
                            emotions = each[2].split(",")
                            ratings = each[4].split(",")
                            semanticsList = each[5].split(",")
                            semanticsTotal = 0
                            for num in semanticAnalysis:
                                print(num)
                                type(num)
                                semanticsTotal += num
                                print(semanticsTotal)
                            print(emotions)
                            print(ratings)
                            print(semanticsList)
                            # for emo in emotions:
                            #     #print()
                            #newDict = dict(zip(emotions,ratings))
                            newDict = dict()
                            print("here before")
                            newDict["semantics"] = semanticsTotal
                            print("here")
                            newDict["emotions"] = emotions
                            newDict["ratings"] = ratings
                            newDict["generaltext"] = each[1]
                            print(newDict)
                            returnData.append(newDict)
                    #print(data)
                    #print("Success")
                    con.commit()
                    # i think this should work but cant properly test 
                    socketio.emit("feedback",jsonify(returnData))

                    return jsonify(returnData)
                else:
                    return "we dont want your feedback - take it easy"
        else:
            return "abusive message was sent- be nice"
    except:
        return ("nope not working",400)


@app.route('/meetinglogin', methods=["POST"])
def meetinglogin():
    info = request.get_json()
    if info == None:
        return "No meeting code"
    print(info)
    try:
        meetingcode = info["meetingcode"]
        print(meetingcode)
        # DO THIS - NEED TO CHECK IF THE MEETING IS LIVE FROM THE MEETING LIST 
        # this will be the meeting id that we extract from the list of live meetings from login code
        # need to add this user to the meetign count or somethingf 
        meetinglive = False
        print(currently_live_meetings)
        for meeting in currently_live_meetings:
            print("in loop")
            print(meeting)
            print(currently_live_meetings[meeting].code)
            print(meetingcode)
            if str(currently_live_meetings[meeting].code) == str(meetingcode):
                print("meeting is live ")
                meetinglive = True
        if meetinglive:
            return "SUCCESS???"
            # DO THIS mayve also return JSON with the meeting ID
        else:
            return "FAILURE - meetin not live"
    except:
        return ("nope not working",400)


@app.route('/userlogin', methods=["POST"])
def userlogin():
    info = request.get_json()
    if info == None:
        return "No feedback there"
    print(info)
    try:
        username = info["username"]
        meetingid = info["meetingid"]
        anonymous = info["anonymous"]
        print("here")
        # how am i supposed to get the company id ??? 
        companyid = 0
        # if the meeting is live then i need to add this user as an attendee 
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            print("here 1.5")
            print("SELECT CompanyID FROM ATTENDEE where username = ''")
            print(username)
            userq = "SELECT CompanyID FROM ATTENDEE where username = '" + username + "'"
            print(userq)
            cur.execute(userq)
            print("here2")
            data = cur.fetchall()
            for each in data:
                print(each[0])
                companyid = each[0]
            #print(data)
            print("here3")
            print(companyid)
            print(str(companyid))
            print("INSERT INTO ATTENDANCE VALUES("+ meetingid +", " + str(companyid)  +" ,"+ anonymous +")")
            # attendance = "INSERT INTO ATTENDANCE VALUES("+ meetingid +", " + str(companyid) + ", "+ anonymous + ")"
            # print(attendance)
            # cur.execute(attendance)

            #idk if this is right
            currently_live_meetings[meetingid].update_participants(companyid)

            getTemplate = "Select TemplateName, EmotionsSelected, Question from TEMPLATES INNER JOIN MEETING ON MEETING.TemplateID = TEMPLATES.TemplateID WHERE MEETING.MeetingID =" + meetingid
            cur.execute(getTemplate)
            row_headers=[x[0] for x in cur.description]
            print(row_headers)
            data = cur.fetchall()

            returnData = []
            for each in data:
                returnData.append(dict(zip(row_headers, each)))
            #print("out")
            print(returnData)
            print("success")
            con.commit()
            
            return jsonify(returnData)
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


@app.route('/endmeeting', methods=["POST"])
def endmeeting():
    info = request.get_json()
    if info == None:
        return "No meeting information was provided"
    try:
        meetingID = info["meetingid"]
        if(meetingID in currently_live_meetings):
            meeting = currently_live_meetings.get(meetingID)
            meeting.end_meeting()
            newly_available_code = meeting.code
            stack_of_available_codes.append(newly_available_code)
            still_collecting_feedback_meetings[meetingID] = meeting
            del currently_live_meetings[meetingID]
            # JOE DO THIS
            
            socketio.emit("feedback",jsonify("OK"))

            return "SUCCESS???"
        else:
            socketio.emit("feedback",jsonify("not-OK"))
    except:
        return ("nope not working",400)

@app.route('/stopmeeting', methods=["POST"])
def stopmeeting():
    info = request.get_json()
    if info == None:
        return "No meeting information was provided"
    try:
        meetingID = info["meetingid"]
        if(meetingID in currently_live_meetings):
            del still_collecting_feedback_meetings[meetingID]
            return "SUCCESS???"
        else:
            return("that meeting isn't ongoing", 400)
    except:
        return ("nope not working",400)

@app.route('/startmeeting', methods=["POST"])
def startmeeting():
    info = request.get_json()
    if info == None:
        return "No meeting information was provided"
    try:
        # #self, title, category, code, startime, duration, host, in_progress, template)
        # #def __init__(self, username, user_id, firstname, lastname, password):
        # host
        # host = Host()
        # meeting = Meeting(each[3], each[5], 1, each[6], each[4], )
        #     t1 = Template("template1", ["happy", "sad"], ["is cereal a soup?"])
        # m1 = t1.make_new_meetings("Title", "Category", "Code", datetime.now(), datetime.now(), h1, False)
        hostid = 0
        meetingID = info["meetingid"]
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = "SELECT HostID, TemplateID FROM MEETING WHERE MeetingID = "+ meetingID
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            hostid = each[0]
            templateid = each[1]
            query = "SELECT * FROM HOSTS WHERE HostID = "+ str(hostid)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            host = Host(each[1], each[0], each[2], each[3], each[4])
            cur = con.cursor()
            query = "SELECT * FROM TEMPLATES WHERE TemplateID = "+ str(templateid)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            emotions = each[3].split(',')
            template = Template(each[2], emotions, each[4].split(','))
            cur = con.cursor()
            query = "SELECT * FROM MEETING WHERE MeetingID = "+ str(meetingID)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            meeting_code = stack_of_available_codes.pop()
            meeting = template.make_new_meetings(each[3], each[5], meeting_code, each[6], each[4], host, True)
            currently_live_meetings[meetingID] = meeting
            return "SUCCESS???"
    except:
        return ("nope not working",400)


@app.route('/hostlogin', methods=["POST"])
def hostlogin():
    info = request.get_json()
    if info == None:
        return "No login information was provided"
    print("Info")
    print(info)
    
    #Dont actually know what to do if parsing fails. info will be an error
    try:
        username = info["username"]
        password = info["password"]

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(hashed_password)
        succesful_login = False

        #logic to determine if the user is in the database,
        with sqlite3.connect("database.db") as con:
            print(hashed_password)
            print("Here")
            cur = con.cursor()
            query = "SELECT HostID, Password FROM HOSTS WHERE username = '" + username + "'"
            cur.execute(query)
            data = cur.fetchall()
            for each in data:
                if each[1] == hashed_password:
                    succesful_login = True
                    logged_in_id = each[0]

                    #DO THIS RETURN HOST ID 
                    returnDict = dict()
                    returnDict["hostid"] = logged_in_id
                    return jsonify(returnDict)
        
        if(not succesful_login):
            return ("wrong password",400)
    except:
        #Likely error is that the request did not have the fields we wanted from it
        return ("Bad Request, probably missing the data we want", 400)
    

@app.route('/gettemplates', methods=["POST"])
def gettemplates():
    info = request.get_json()
    if info == None:
        return "No login information was provided"
    print("Info")
    print(info)
    
    #Dont actually know what to do if parsing fails. info will be an error
    try:
        hostid = info["hostid"]
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = "SELECT TemplateName, TemplateID FROM TEMPLATES WHERE HostID = " + hostid
            cur.execute(query)
            data = cur.fetchall()
            templateinfo = []
            for each in data:
                templateinfo.append([each[0], each[1]])
            cur = con.cursor()
            query = "SELECT Category FROM MEETING WHERE HostID = " + hostid
            cur.execute(query)
            data = cur.fetchall()
            category = []
            for each in data:
                category.append(each[0])
        
        returnDict = dict()
        returnDict["templates"] = templateinfo
        returnDict["categories"] = category
        return jsonify(returnDict)
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
    print(url_for('profile', username='John Doe'))
    print(url_for('profile', username='Susan'))
    print(url_for('profile', username='template'))
