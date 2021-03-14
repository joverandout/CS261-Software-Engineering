#pip install flask
#pip install flask_socketio
#pip install flask-cors
#pip install flair (might need anaconda)

from flask import Flask, url_for, render_template, jsonify, send_file
from flask_socketio import SocketIO, emit, send
from flask import request
from flask_cors import CORS
from markupsafe import escape

from Meeting import Meeting
from Host import Host
from Attendee import Attendee
from datetime import datetime, timedelta
from Template import Template
from fpdf import FPDF
import random

from matplotlib import pyplot as plt
import numpy as np

import time
import base64
import hashlib

import re

import sqlite3
from sqlite3 import Error

import random

import template_db_fethcer
from Semantic import Semantic
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

#create the dictionaries to hold the currently live meeting objects and
#meetings not currently live but still collecting feedback
currently_live_meetings = {}
still_collecting_feedback_meetings = {}

#here we initialise the stack and push onto it all the valid meeting codes
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

#test route never used
@app.route('/')
def index():
    return 'MEETING APP PLS GIVE US A FIRST'

@app.route('/sendsocketmessage', methods=["POST"])  
def sendsocketmessage():
    data = request.get_json()
    print("\nSending Message to frontend: ",data)
    
    socketio.emit("femessage",data)
    return "Sent!"

#main page after logging in as the host
@app.route('/hostmain', methods=["POST"])
def hostmain():
    info = request.get_json()
    if info == None:
        #if there are no host id passed to the backend
        #return an error
        return "No hostID provided"
    print(info)
    try:
        #otherwise collect the host id of the host who is logged in
        hostID = info["hostid"]
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            #get all the meeting data for all of the meetings that have the
            #current hosts id as a foreign key
            query = "SELECT * FROM MEETING WHERE MEETING.HostID = " + hostID
            cur.execute(query)
            row_headers=[x[0] for x in cur.description]
            data = cur.fetchall()
            returnData = []
            for each in data:
                #turn the data into a dictionary of the information
                returnData.append(dict(zip(row_headers, each)))
            print(data)
            #and then turn it into a json object.
            return jsonify(returnData)
    except Exception as e:
        print(e)
        return ("nope not working",400)



"""
This is the view where the meeting is displayed and as such it fetches information
Based off of a meeting id passed via json from the front end. This information allows
the correct questions and emotions to be displayed and the appropriate information
in relation to this specific meeting to be returned to the front end in the form of a
pdf.
"""
@app.route('/meetingview', methods=["POST"])
def meetingview():
    info = request.get_json()
    if info == None:
        return "No meeting ID"
    print(info)
    # try:
    #     with open("Test.pdf", "rb") as pdf_file:
    #         encoded_string = base64.b64encode(pdf_file.read())
    #         print(encoded_string)
    #         return encoded_string
    # except Exception as e:
    #     print(e)
    try:
        meetingID = info["meetingid"]
        print(meetingID)
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            #Get the questions from the template of the meeting that corresponds to the meeting id passed via json
            postQ = "SELECT Question FROM TEMPLATES INNER JOIN MEETING as M on M.TemplateID = TEMPLATES.TemplateID AND M.MeetingID = " + meetingID
            cur.execute(postQ)
            ques = cur.fetchall()
            print(ques)
            elem = ques[0]
            print(elem)
            elemIn = elem[0]
            print(elemIn)
            splitQues = str(elemIn).split('?')
            print(splitQues)
            #del splitQues[-1]
            print(splitQues)
            dictTest = dict()
            print("DEFINED")
            for q in splitQues:
                print(q)
                if q != "":
                    dictTest[q] = []
            # for each in ques:
            #     for quest in each:
            #         print(quest)
            #         for tmp in splitQues:
            #             print(tmp)
            #             dictTest[tmp] = []

            #Select the infomartion such as the emotions time rating etc of each piece of feedback that corresponds to the meeting id originally passed
            query = "select GeneralText, Emotion, FTime, Rating, UF.CompanyID, A.Anonymous, AT.Username from FEEDBACK INNER JOIN USERFEEDBACK as UF on UF.FeedbackID = FEEDBACK.FeedbackID INNER JOIN ATTENDANCE as A on A.MeetingID = UF.MeetingID and A.CompanyID = UF.CompanyID LEFT JOIN ATTENDEE as AT on AT.CompanyID = A.CompanyID and A.Anonymous = 0 where UF.MeetingID = " + meetingID
            cur.execute(query)
            #turn the values from the query into values in a data array
            row_headers=[x[0] for x in cur.description]
            data = cur.fetchall()
            returnData = []
            generaltext = []
            postfeed = []
            usernames = []
            emotionsWithRatings = []
            meetingName = ""
            meetingCat = ""
            emotDict = dict()
            print("Defined all values")
            for each in data:
                print(each[1])
                #place the feedback into a dictionary 
                if (each[1] != "Technical" and each[1] != "Post"):
                    x = each[1].split(",")
                    y = each[3].split(",")
                    for emo in x:
                        numDict = dict()
                        numDict["5"] = 0
                        numDict["4"] = 0
                        numDict["3"] = 0
                        numDict["2"] = 0
                        numDict["1"] = 0
                        emotDict[emo] = numDict
                    print(x)
                    print(y)
                    for j in range(len(x)):
                        #add each of the emotions from the database and their rating to the emotions
                        #in the format emotion:number so the array is formatted for example like,
                        #[happy:5, sad:2, confused:3] etc.
                        emotionsWithRatings.append(x[j] + ":"+ y[j])
                    returnData.append(dict(zip(row_headers, each)))
                    generaltext.append(each[0])
                    #if the anonymous value is set to 1 then the username for the individual feedback object is set to anonymous
                    #else the username is appended to the dictionary
                    if each[5] == 0:
                        usernames.append(each[6])
                    else:
                        usernames.append("Anonymous")
                elif each[1] == "Post":
                    print("ITS POSTTTTTTTTTTTTT")
                    #if its a post meeting split it on the tildas
                    splt = each[0].split("~")
                    print(splt)
                    k = 0 
                    #this gets the questions individually
                    for question in dictTest:
                        print(question)
                        print(splt[k])
                        #append each questions response to the dictest
                        dictTest[question].append(splt[k])
                        k+=1 #incrementing the counter afterwards
                    for feed in splt:
                        #for each split question append it to the feed
                        postfeed.append(feed)
                    print(each[1])
            print(dictTest)
            #print("MADE THROUGH FIRDST LOOP")
            for each in data:
                #for each feedback check it isnt technical or a post
                if (each[1] != "Technical" and each[1] != "Post"):
                    #that makes it an emotion
                    #therefore we split on the commas to get the rating and the emotion
                    x = each[1].split(",")
                    y = each[3].split(",")
                    #then for each of the emotions upddate the counter in the correct dictionary
                    for j in range(len(x)):
                        print(j)
                        print(emotDict[x[j]])
                        val = emotDict[x[j]]
                        if y[j] != 0:
                            print(y[j])
                            print(val[y[j]])
                            val[y[j]] = val[y[j]] + 1
                            print(val[y[j]])
            #get the meeting information like the name and category to display in the webpage for the meeting view
            query = "select MeetingName, Category from MEETING where MeetingID = " + meetingID
            cur.execute(query)
            data = cur.fetchall()
            for meet in data:
                meetingName = meet[0]
                meetingCat = meet[1]

            print(generaltext)
            print(postfeed)
            #turn all of this infomation we have collected like the name and values into the pdf format
            makepdf(generaltext, usernames, emotionsWithRatings, meetingName, meetingCat, emotDict, dictTest)
            print(data)
            with open("Test.pdf", "rb") as pdf_file:
                #with the pdf open turn it into bsae64 in order to return it to the front end
                encoded_string = base64.b64encode(pdf_file.read())
                print(encoded_string)
            return encoded_string
    except Exception as e: #otherwise return an error
        print("pdf conversion error")
        print(e)
        print("\n\n")
        return ("nope not working",400)

"""
this functiont akes key information on a meeting previoulsy taken from the database and formatted
into dictionaries adn arrays specifically for use in this function. From there it constructs a pdf
by creating graphs based on emotion selection whilst also then listing all personalised feedback
and which suer sumbitted it
"""
def makepdf(generalText, usernames,emoR, MN, MC, emoDict, postfeed):
    pdf = FPDF()
    #add a page and set the font size
    pdf.add_page()
    pdf.set_font("Arial", size = 20)
    #pdf.set_fill_color(r=51,g=153,b=255)
    pdf.cell(200,10,txt = MC + " : "+ MN, ln = 1, align = 'C')
    pdf.set_font("Arial", size = 12)
    print(len(generalText))
    print(usernames[0])
    #The below forloop takes all of the personalised comment feedback and 
    #turns it into the original table by drawing each row one after another
    #at the top of the page
    for i in range(len(generalText)):
        print(i)
        print(usernames[i])
        textThing = str(usernames[i]) + ": " + str(generalText[i])
        print(textThing)
        pdf.set_fill_color(r=230,g=242,b=255)
        pdf.set_text_color(r=0,g=0,b=0)
        #setFillColor(204,229,255)
        pdf.cell(100,10, txt = textThing,border = 1,ln = 1, align = 'L', fill = True)
    pdf.cell(200,10,txt = "", ln = 1, align = 'C')
    pdf.set_fill_color(r=230,g=255,b=249)
    # for j in range(len(emoR)):
    #     pdf.cell(100,10, txt = emoR[j],border = 1,ln = 1, align = 'L', fill = True)
    for each in postfeed:
        #creat the create the cells 
        pdf.set_fill_color(r=255,g=255,b=255)
        pdf.cell(100,10, txt = str(each),border = 1,ln = 1, align = 'L', fill = True)
        pdf.set_fill_color(r=230,g=255,b=249)
        for rep in postfeed[each]:
            pdf.cell(100,10, txt = str(rep),border = 1,ln = 1, align = 'L', fill = True)
 
    pdf.cell(200,10,txt = "", ln = 1, align = 'C')

    print("here")
    #pdf.BarDiag(200, 100, ["happy", "sad"])
    i = 0
    #for each emotion of the meeting create the graph
    for emotion in emoDict:
        #each rating for that emotion is treated as an object
        objects = ('5','4','3','2','1')
        yAxis = np.arange(5)
        values = []
        print(emotion)
        print(emoDict[emotion])
        for each in emoDict[emotion]:
            print(each)
            print(emoDict[emotion][each])
            values.append(emoDict[emotion][each])
            print(values)
        #use the built in plot function to create the graphs, aligning them centrally in the page
        plt.bar(yAxis, values, align='center', alpha=0.5)
        plt.xticks(yAxis, objects)
        plt.ylabel('Times Recorded')
        plt.xlabel('Rating')
        plt.title(emotion+" rating during meeting")
        plt.savefig(emotion + ".jpg")
        plt.clf()
        i += 1
        #add the image each time after its creation
        pdf.image(emotion + ".jpg", x = None, y = None, w = 140, h = 100, type = 'JPG', link = '')
    #once the graphs have all been created we simply exit the for loop and return the pdf as a json object
    pdf.output("Test.pdf")
    files = {'file': open('Test.pdf', 'rb')}
    print(jsonify())

"""
Once the meeting is over taking in the final feedback int erms of the questions
It performs checks to ensure the meeting is still taking feedback and if so will
accept the users feedback and return the values to the database. So the attendance
is tracked and will appear in the pdf for examples
"""
@app.route('/postmeetingfeed', methods=["POST"])
def postmeetingfeed():
    info = request.get_json()
    if info == None:
        return ("No feedback there",400)
    print(info)
    try:
        #collect the id and question responses as well as the time submitted for the feedback 
        meetingID = info["meetingid"]
        postquestions = info["questionresponses"]
        timeSent = info["ftime"]
        companyID = info["companyid"]
        print(postquestions)
        #check the meeting object exists in the still collecting feedback dictionary of currently 
        #live meetinfs and if its doesn't do not allow it to collect feedback
        """
        For the sake of the demo we will not check if the meeting is still running
        if (meetingID in still_collecting_feedback_meetings):
            print("meeting collecting post feedback")
        else:
            return ("no longer taking feedback",400)"""
        with sqlite3.connect("database.db") as con:
            #insert the feedback values into the dictionary for permanent storage
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

"""
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
        print("here")

        # Remove emojis from text feedback
        generaltext = deEmojify(generaltext)

        # offEval = Offensive(generaltext)
        # offEval.update_rating()
        # howOffensive = offEval.get_scores()
        # print(howOffensive)

        # send to the sentiment analysis 
        feedbackEval = Semantic(generaltext)
        feedbackEval.update_semValues_and_confScores()
        s = feedbackEval.get_scores()

        # going to get back an array
        print(s)
        x = random.uniform(-1,1)
        semanticAnalysis = [s[0]]
        #x = random.uniform(-1,1)
        print(x)
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
            print("Abusinve")
            # need to chech here that the meetin is live DO THIS
            #need joe to make the list of meetings 
            if(meetingID in currently_live_meetings):
                print("this meeting is still accepting feedback")
            else:
                return ("MEETING NO LONGER LIVE", 400)
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
                print("Meme")
                #ratList = 
                #emotsList = emotion.split(",")
                
                if True == True:
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
                            newDict["semantics"] = semanticAnalysis[0]#random.randint(-100,100)/100 #semanticsTotal
                            print("here")
                            newDict["emotions"] = emotions
                            newDict["ratings"] = ratings
                            newDict["generaltext"] = each[1]
                            print(newDict)
                            returnData.append(newDict)
                    #print(data)
                    
                    con.commit()
                    print(returnData[0])
                    # i think this should work but cant properly test 
                    print("Success!")
                    socketio.emit("feedback",returnData[0])
                    print("Success")
                    return jsonify(returnData)
                else:
                    return ("we dont want your feedback - take it easy", 400)
        else:
            return "abusive message was sent- be nice"
    except Exception as e:
        print(e)
        return ("nope not working",400)


# A function to remove emojis from textual feedback
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

"""
This is the function called when an attendee trys to enter into a meeting
This is performed by checking the meeting is currently live and if so creating
and attendance object IF the user trying to connect is one who already exists
it also handles anonymity
"""
@app.route('/meetinglogin', methods=["POST"])
def meetinglogin():
    info = request.get_json()
    if info == None:
        #if no meeting code is provided in that json object then say that
        return "No meeting code"
    print(info)
    try:
        #otherwise if the json object contains information extract the meetingid alongside
        #the username of the user trying to attned the meeting as well as whether or not
        #they were trying to stay anonymous
        meetingcode = info["meetingcode"]
        username = info["username"]
        anonymous = info["anonymous"]
        meetinglive = False
        MeetingFound = None
        #fore ach meeting in the currently live meetinfs
        for meeting in currently_live_meetings:
            print("in loop")
            print(meeting)
            print(currently_live_meetings[meeting].code)
            print(meetingcode)
            #if the code given by json matches a code of currently matched meeting
            if str(currently_live_meetings[meeting].code) == str(meetingcode):
                print("meeting is live ")
                meetinglive = True
                #set the meeting live boolean to true as this means the meeting is live
                print(currently_live_meetings[meeting].meetingid)
                #set the meeting id to the id of the meeting in the list
                meetingid = currently_live_meetings[meeting].meetingid
                MeetingFound = currently_live_meetings[meeting]
        if meetinglive:
            #if it is possible to connect to the meeting
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                print("here 1.5")
                #whilst connected to the database, we create a new attendance object
                print("SELECT CompanyID FROM ATTENDEE where username = ''")
                print(username)
                userq = "SELECT CompanyID FROM ATTENDEE where username = '" + username + "'"
                print(userq)
                cur.execute(userq)
                print("here2")
                #here we select the id of the company from the attendee so we can use it as a foreign
                #key in the database when we create our attendance entry in the database
                data = cur.fetchall()
                for each in data:
                    print(each[0])
                    companyid = each[0]
                print("here3")
                print(companyid)
                print(str(companyid))
                #with all the correct infomation selected we then insert into the attendance the object to represent each
                #users attendance created from the data fetched from the database just before 
                print("INSERT INTO ATTENDANCE VALUES("+ str(meetingid) +", " + str(companyid)  +" ,"+ anonymous +")")
                attendance = "INSERT INTO ATTENDANCE VALUES("+ str(meetingid) +", " + str(companyid) + ", "+ anonymous + ")"
                print(attendance)
                #execute the query
                cur.execute(attendance)
                print(currently_live_meetings)
                print(MeetingFound)
                print(MeetingFound.get_number_of_participants())
                MeetingFound.update_participants(companyid)
                print(MeetingFound.get_number_of_participants())
                #selected the template naem emeotions questions etc from the templates table whilst joining it to the meetings table tog et the meeting name
                #this is so it can be returned to the front end so the correct questions and available emotions can be displayed to the attendee
                getTemplate = "Select TemplateName, EmotionsSelected, Question, MeetingName from TEMPLATES INNER JOIN MEETING ON MEETING.TemplateID = TEMPLATES.TemplateID WHERE MEETING.MeetingID =" + str(meetingid)
                print(getTemplate)
                #execute the query to get the template and meeting specific data
                cur.execute(getTemplate)
                row_headers=[x[0] for x in cur.description]
                print(row_headers)
                data = cur.fetchall()
                #fetch all of it

                returnData = []
                for each in data:
                    #for every piece of data create a temporary dictionary
                    #returnData.append(dict(zip(row_headers, each)))
                    emotions = each[1].split(',')
                    postquestions = each[2].split('?')
                    secondquestions = []
                    for question in postquestions:
                        if(not (question == "")):
                            secondquestions.append(question)
                    tempDict = dict()
                    #fill each of the fields in the dictionary with the values from
                    #the sql query in order to return to the front end
                    tempDict["meetingid"] = str(meetingid)
                    tempDict["emotionsselected"] = emotions
                    tempDict["templatename"] = each[0]
                    tempDict["question"] = secondquestions
                    tempDict["companyid"] = companyid
                    tempDict["meetingname"] = each[3]
                    #append this new dictionary onto the data we are going to append
                    returnData.append(tempDict)
                #print("out")
                print(returnData)
                print("success")
                con.commit()
                #return the returdata in the form of a json object to the frontend
                return jsonify(returnData)
        else:
            return ("nope not working",400)
    except:
        return ("nope not working",400)

"""
Called when a user logins to the application. This is then used to create an attendance
entry in the database
"""
@app.route('/userlogin', methods=["POST"])
def userlogin():
    info = request.get_json()
    if info == None:
        #return an error if no information is passed in json
        return "No feedback there"
    print(info)
    try:
        #collect the username and the meetingid they are trying to connect to
        #as well as whether or not they want to be anonymous or not
        username = info["username"]
        meetingid = info["meetingid"]
        anonymous = info["anonymous"]
        print("here")
        companyid = 0
        # if the meeting is live then i need to add this user as an attendee 
        with sqlite3.connect("database.db") as con:
            #with the database open as a connection
            cur = con.cursor()
            print("here 1.5")
            #get the userid of the attendee where the username matches the value in the database
            userq = "SELECT CompanyID FROM ATTENDEE where username = '" + username + "'"
            cur.execute(userq)
            #execute the query
            data = cur.fetchall()
            for each in data:
                print(each[0])
                #set the variable companyid to the value returned from the sql query
                companyid = each[0]
            #print(data)
            print("here3")
            print(companyid)
            print(str(companyid))
            print("INSERT INTO ATTENDANCE VALUES("+ meetingid +", " + str(companyid)  +" ,"+ anonymous +")")
            # attendance = "INSERT INTO ATTENDANCE VALUES("+ meetingid +", " + str(companyid) + ", "+ anonymous + ")"
            # print(attendance)
            # cur.execute(attendance)

            #update the participants of the currently live meeting that shares and id with the meeting we are trying to connect to
            currently_live_meetings[meetingid].update_participants(companyid)
            
            #here we select all the values associated with a template and a meeting so as the return them to the front end and
            #allow the correct information to be displayed to the front end
            getTemplate = "Select TemplateName, EmotionsSelected, Question from TEMPLATES INNER JOIN MEETING ON MEETING.TemplateID = TEMPLATES.TemplateID WHERE MEETING.MeetingID =" + meetingid
            cur.execute(getTemplate)
            #the row headers are then initialised
            row_headers=[x[0] for x in cur.description]
            print(row_headers)
            #and data is all fetched
            data = cur.fetchall()

            returnData = []
            for each in data:
                #each piece of data is appended to the return data
                returnData.append(dict(zip(row_headers, each)))
            #print("out")
            print(returnData)
            #and it it returned as a json object below
            print("success")
            con.commit()
            
            return jsonify(returnData)
    except:
        return ("nope not working",400)

"""
This is the creation page for a new meeting where the values are created and placed into the database
once the user has made their new meeting using the webpage
"""
@app.route('/newmeeting', methods=["POST"])
def newmeeting():
    info = request.get_json()
    if info == None:
        #if no meeting info is return send an error
        return "No feedback there"
    print(info)
    try:
        #otherwise collect the things about the meeting that need to be entered into the database
        #like host id template id (as foreign keys) duration category and start time
        hostID = info["hostid"]
        templateID = info["templateid"]
        meetingname = info["meetingname"]
        duration = info["duration"]
        category = info["category"]
        startTime = info["starttime"]
        #the start time is collected as the number of mili seconds since the utf time in 1970s
        print(startTime)
        intstartTime = int(startTime) / 1000
        #therefore we convert it to seconds by dividing by 1000
        #and then convert using the below formula to a timestamp format
        timeStampStartTime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(intstartTime))
        print(timeStampStartTime)
        with sqlite3.connect("database.db") as con:
            #from there we connect to the database and insert all the values
            cur = con.cursor()
            query = "INSERT INTO MEETING VALUES(NULL, " + hostID + ", " + templateID + ", '" + meetingname + "', '"+ duration +"', '" + category + "' , DATETIME('"+timeStampStartTime +"') )"
            print(query)
            cur.execute(query)
            print("Success")
            con.commit()
            return "SUCCESS???"
    except:
        return ("nope not working",400)

"""
This is called similarly to new meeting however in the instance where the user wants to create a new template
"""
@app.route('/newtemplate', methods=["POST"])
def newtemplate():
    info = request.get_json()
    if info == None:
        return "No feedback there"
        #if no meeting info is return send an error
    print(info)
    try:
        #otherwise collect the things about the meeting that need to be entered into the database for a template
        #like host id (as a foreign key) the emotions and the questions
        hostID = info["hostid"]
        templateName = info["templatename"]
        emotionsSelected = info["emotionsselected"]
        question = info["question"]
        with sqlite3.connect("database.db") as con:
            print("Here")
            #once these are all collected we then insert them into the database
            cur = con.cursor()
            #we use NULL as the database schema then creates a meeting id that is new and not used before
            query = "INSERT INTO TEMPLATES VALUES(NULL, " + hostID + ", '" + templateName + "', '" + emotionsSelected + "', '"+ question +"')"
            print(query)
            cur.execute(query)
            print("Success")
            con.commit()
            return "SUCCESS???"
    except:
        return ("nope not working",400)

"""
End meeting is called when a meeting is no longer live but is still receiving feedback. For this we have to
remove it from the list of live meetings and add it to the list of meetings that aren't live but are still taking
feedback.
"""
@app.route('/endmeeting', methods=["POST"])
def endmeeting():
    info = request.get_json()
    if info == None:
        #if no json data is received send an error
        return ("nope not working",400)
    try:
        #get the meeting id of the meeting we want to end
        meetingID = info["meetingid"]
        #if the meeting id is shared with a meeting in the dictionary then 
        #we have a valid meeting to end 
        if(meetingID in currently_live_meetings):
            #get the meeting object and sotre it in a seperate variable 
            meeting = currently_live_meetings.get(meetingID)
            #end the meeting
            meeting.end_meeting()
            #get its code
            newly_available_code = meeting.code
            #and pop it back on the stack of available meeting codes
            stack_of_available_codes.append(newly_available_code)
            #add it to the new list of meetings that can take feedback but aren't live
            still_collecting_feedback_meetings[meetingID] = meeting
            del currently_live_meetings[meetingID]
            #finally delete it from the dictionary
            socketio.emit("endmeeting","ok")

            return jsonify("OK")
        else:
            #this meeting doesnt exist so we can't end it, therefore we return an error
            socketio.emit("endmeeting","not ok")
            return ("nope not working",400)
    except Exception as e:
        print(e)
        return ("nope not working",400)

"""
Stop meeting is called when a host no longer wants a meeting to receive any feedback. It must be called
after the meeting has ended and then destroys the entry of the meeting from the dictionary
"""
@app.route('/stopmeeting', methods=["POST"])
def stopmeeting():
    info = request.get_json()
    if info == None:
        #throws an error if no json is received
        return ("nope not working",400)
    try:
        meetingID = info["meetingid"]
        #collect the meeting id from the json object
        if(meetingID in still_collecting_feedback_meetings):
            #if the meeting is in the list, i.e. it is allowed to be stopped as 
            #it has already been ended but not yet stopped then we deleted it from
            #the dictionary
            del still_collecting_feedback_meetings[meetingID]
            socketio.emit("stopmeeting",jsonify("OK"))
            #return that to the host
            return jsonify("OK")
        else:
            #otherwise return an error as the meeting cannot be ended
            socketio.emit("stopmeeting",jsonify("not-OK"))
            return ("nope not working",400)
    except:
        return ("nope not working",400)

"""
Start meeting is used when a host wishes to begin a meeting they have prevoiusly created and therefore allow it to
collect feedback. This is done by creating the meeting object from the entries in teh database and then adding it to
the dictionary of live meetinfs
"""
@app.route('/startmeeting', methods=["POST"])
def startmeeting():
    info = request.get_json()
    if info == None:
        #return an error if no json is received
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
        #select the meeting id from the json
        with sqlite3.connect("database.db") as con:
            #open the database
            cur = con.cursor()
            #get the hsot and template ids that correspond to the meeting we want to start
            query = "SELECT HostID, TemplateID FROM MEETING WHERE MeetingID = "+ meetingID
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            hostid = each[0]
            templateid = each[1]
            #get all the host infomation from the database of that host id
            query = "SELECT * FROM HOSTS WHERE HostID = "+ str(hostid)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            #create a new host object with this infomation we have gathered
            host = Host(each[1], each[0], each[2], each[3], each[4])
            cur = con.cursor()
            #get all the relevant template information to make a template object
            query = "SELECT * FROM TEMPLATES WHERE TemplateID = "+ str(templateid)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            emotions = each[3].split(',')
            #split the emotions so they form an array and then create a new template object
            #splitting the questions into an array too 
            template = Template(each[2], emotions, each[4].split(','))
            cur = con.cursor()
            #select all the meeting information aswell from the database
            query = "SELECT * FROM MEETING WHERE MeetingID = "+ str(meetingID)
            cur.execute(query)
            data = cur.fetchall()
            each = data[0]
            #get a meeting code that can be used by popping it off the stuff
            meeting_code = stack_of_available_codes.pop()
            #crete a new meeting from the template object we previously created
            meeting = template.make_new_meetings(each[0], each[3], each[5], meeting_code, each[6], each[4], host, True)
            currently_live_meetings[meetingID] = meeting
            #return the meeting code so it can be displayed
            return jsonify(meeting_code)
    except:
        return ("nope not working",400)

"""
host login is called when a host tries to login in order to verify their password in before returning the successful login in it is.
It also returns the value of the host id of the newly logged in user
"""
@app.route('/hostlogin', methods=["POST"])
def hostlogin():
    info = request.get_json()
    if info == None:
        #return an error if there are no json passed
        return "No login information was provided"
    print("Info")
    print(info)
    
    try:
        #get the username and password from the json object
        username = info["username"]
        password = info["password"]

        #hash the password
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(hashed_password)
        succesful_login = False

        #logic to determine if the user is in the database,
        with sqlite3.connect("database.db") as con:
            print(hashed_password)
            print("Here")
            cur = con.cursor()
            #select the host id and the password from the database where the username matches
            query = "SELECT HostID, Password FROM HOSTS WHERE username = '" + username + "'"
            cur.execute(query)
            data = cur.fetchall()
            for each in data:
                #if the password matches our hashed password
                if each[1] == hashed_password:
                    succesful_login = True
                    #set the lgin as true and get the host id of the newly logged in user
                    logged_in_id = each[0]

                    #DO THIS RETURN HOST ID 
                    returnDict = dict()
                    returnDict["hostid"] = logged_in_id
                    return jsonify(returnDict)
        
        if(not succesful_login):
            #otherwise return a wrong password error
            return ("wrong password",400)
    except:
        #Likely error is that the request did not have the fields we wanted from it
        return ("Bad Request, probably missing the data we want", 400)
    
"""
Get templates is used to retrieve all of a hosts templates so the front end can display the correct information to the user
so that the users templates are available for them to create new meetings and by which to filter their existing meetings
on their home screen.
"""
@app.route('/gettemplates', methods=["POST"])
def gettemplates():
    info = request.get_json()
    if info == None:
        #return the error message if no json is provided
        return "No login information was provided"
    print("Info")
    print(info)
    
    #Dont actually know what to do if parsing fails. info will be an error
    try:
        #get the host id fromt eh jsn
        hostid = info["hostid"]
        with sqlite3.connect("database.db") as con:
            #connect to the database
            cur = con.cursor()
            #get all of the name and ids of the templates that share a host id with our host
            query = "SELECT TemplateName, TemplateID FROM TEMPLATES WHERE HostID = " + hostid
            cur.execute(query)
            data = cur.fetchall()
            templateinfo = []
            for each in data:
                #add each of the info we got from the database 
                #to the template array in the form of an array with name
                #and id such as below:
                #[[name,0], [template2,1], [othername, 3]]
                templateinfo.append([each[0], each[1]])
            cur = con.cursor()
            #get all the categories of the meetings where the hosts id is also the same as our host
            query = "SELECT Category FROM MEETING WHERE HostID = " + hostid + " GROUP BY Category"
            cur.execute(query)
            data = cur.fetchall()
            category = []
            for each in data:
                #add each of these categories to an array
                category.append(each[0])
        #put both the categories array and the templates array into a dictionary and return it as a json
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
    