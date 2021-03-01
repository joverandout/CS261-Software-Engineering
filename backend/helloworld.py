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

stack_of_available_codes = [10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10041, 10042, 10043, 10044, 10045, 10046, 10047, 10048, 10049, 10050, 10051, 10052, 10053, 10054, 10055, 10056, 10057, 10058, 10059, 10060, 10061, 10062, 10063, 10064, 10065, 10066, 10067, 10068, 10069, 10070, 10071, 10072, 10073, 10074, 10075, 10076, 10077, 10078, 10079, 10080, 10081, 10082, 10083, 10084, 10085, 10086, 10087, 10088, 10089, 10090, 10091, 10092, 10093, 10094, 10095, 10096, 10097, 10098, 10099, 10100, 10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109, 10110, 10111, 10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120, 10121, 10122, 10123, 10124, 10125, 10126, 10127, 10128, 10129, 10130, 10131, 10132, 10133, 10134, 10135, 10136, 10137, 10138, 10139, 10140, 10141, 10142, 10143, 10144, 10145, 10146, 10147, 10148, 10149, 10150, 10151, 10152, 10153, 10154, 10155, 10156, 10157, 10158, 10159, 10160, 10161, 10162, 10163, 10164, 10165, 10166, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10175, 10176, 10177, 10178, 10179, 10180, 10181, 10182, 10183, 10184, 10185, 10186, 10187, 10188, 10189, 10190, 10191, 10192, 10193, 10194, 10195, 10196, 10197, 10198, 10199, 10200, 10201, 10202, 10203, 10204, 10205, 10206, 10207, 10208, 10209, 10210, 10211, 10212, 10213, 10214, 10215, 10216, 10217, 10218, 10219, 10220, 10221, 10222, 10223, 10224, 10225, 10226, 10227, 10228, 10229, 10230, 10231, 10232, 10233, 10234, 10235, 10236, 10237, 10238, 10239, 10240, 10241, 10242, 10243, 10244, 10245, 10246, 10247, 10248, 10249, 10250, 10251, 10252, 10253, 10254, 10255, 10256, 10257, 10258, 10259, 10260, 10261, 10262, 10263, 10264, 10265, 10266, 10267, 10268, 10269, 10270, 10271, 10272, 10273, 10274, 10275, 10276, 10277, 10278, 10279, 10280, 10281, 10282, 10283, 10284, 10285, 10286, 10287, 10288, 10289, 10290, 10291, 10292, 10293, 10294, 10295, 10296, 10297, 10298, 10299, 10300, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10313, 10314, 10315, 10316, 10317, 10318, 10319, 10320, 10321, 10322, 10323, 10324, 10325, 10326, 10327, 10328, 10329, 10330, 10331, 10332, 10333, 10334, 10335, 10336, 10337, 10338, 10339, 10340, 10341, 10342, 10343, 10344, 10345, 10346, 10347, 10348, 10349, 10350, 10351, 10352, 10353, 10354, 10355, 10356, 10357, 10358, 10359, 10360, 10361, 10362, 10363, 10364, 10365, 10366, 10367, 10368, 10369, 10370, 10371, 10372, 10373, 10374, 10375, 10376, 10377, 10378, 10379, 10380, 10381, 10382, 10383, 10384, 10385, 10386, 10387, 10388, 10389, 10390, 10391, 10392, 10393, 10394, 10395, 10396, 10397, 10398, 10399, 10400, 10401, 10402, 10403, 10404, 10405, 10406, 10407, 10408, 10409, 10410, 10411, 10412, 10413, 10414, 10415, 10416, 10417, 10418, 10419, 10420, 10421, 10422, 10423, 10424, 10425, 10426, 10427, 10428, 10429, 10430, 10431, 10432, 10433, 10434, 10435, 10436, 10437, 10438, 10439, 10440, 10441, 10442, 10443, 10444, 10445, 10446, 10447, 10448, 10449, 10450, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 10476, 10477, 10478, 10479, 10480, 10481, 10482, 10483, 10484, 10485, 10486, 10487, 10488, 10489, 10490, 10491, 10492, 10493, 10494, 10495, 10496, 10497, 10498, 10499, 10500, 10501, 10502, 10503, 10504, 10505, 10506, 10507, 10508, 10509, 10510, 10511, 10512, 10513, 10514, 10515, 10516, 10517, 10518, 10519, 10520, 10521, 10522, 10523, 10524, 10525, 10526, 10527, 10528, 10529, 10530, 10531, 10532, 10533, 10534, 10535, 10536, 10537, 10538, 10539, 10540, 10541, 10542, 10543, 10544, 10545, 10546, 10547, 10548, 10549, 10550, 10551, 10552, 10553, 10554, 10555, 10556, 10557, 10558, 10559, 10560, 10561, 10562, 10563, 10564, 10565, 10566, 10567, 10568, 10569, 10570, 10571, 10572, 10573, 10574, 10575, 10576, 10577, 10578, 10579, 10580, 10581, 10582, 10583, 10584, 10585, 10586, 10587, 10588, 10589, 10590, 10591, 10592, 10593, 10594, 10595, 10596, 10597, 10598, 10599, 10600, 10601, 10602, 10603, 10604, 10605, 10606, 10607, 10608, 10609, 10610, 10611, 10612, 10613, 10614, 10615, 10616, 10617, 10618, 10619, 10620, 10621, 10622, 10623, 10624, 10625, 10626, 10627, 10628, 10629, 10630, 10631, 10632, 10633, 10634, 10635, 10636, 10637, 10638, 10639, 10640, 10641, 10642, 10643, 10644, 10645, 10646, 10647, 10648, 10649, 10650, 10651, 10652, 10653, 10654, 10655, 10656, 10657, 10658, 10659, 10660, 10661, 10662, 10663, 10664, 10665, 10666, 10667, 10668, 10669, 10670, 10671, 10672, 10673, 10674, 10675, 10676, 10677, 10678, 10679, 10680, 10681, 10682, 10683, 10684, 10685, 10686, 10687, 10688, 10689, 10690, 10691, 10692, 10693, 10694, 10695, 10696, 10697, 10698, 10699, 10700, 10701, 10702, 10703, 10704, 10705, 10706, 10707, 10708, 10709, 10710, 10711, 10712, 10713, 10714, 10715, 10716, 10717, 10718, 10719, 10720, 10721, 10722, 10723, 10724, 10725, 10726, 10727, 10728, 10729, 10730, 10731, 10732, 10733, 10734, 10735, 10736, 10737, 10738, 10739, 10740, 10741, 10742, 10743, 10744, 10745, 10746, 10747, 10748, 10749, 10750, 10751, 10752, 10753, 10754, 10755, 10756, 10757, 10758, 10759, 10760, 10761, 10762, 10763, 10764, 10765, 10766, 10767, 10768, 10769, 10770, 10771, 10772, 10773, 10774, 10775, 10776, 10777, 10778, 10779, 10780, 10781, 10782, 10783, 10784, 10785, 10786, 10787, 10788, 10789, 10790, 10791, 10792, 10793, 10794, 10795, 10796, 10797, 10798, 10799, 10800, 10801, 10802, 10803, 10804, 10805, 10806, 10807, 10808, 10809, 10810, 10811, 10812, 10813, 10814, 10815, 10816, 10817, 10818, 10819, 10820, 10821, 10822, 10823, 10824, 10825, 10826, 10827, 10828, 10829, 10830, 10831, 10832, 10833, 10834, 10835, 10836, 10837, 10838, 10839, 10840, 10841, 10842, 10843, 10844, 10845, 10846, 10847, 10848, 10849, 10850, 10851, 10852, 10853, 10854, 10855, 10856, 10857, 10858, 10859, 10860, 10861, 10862, 10863, 10864, 10865, 10866, 10867, 10868, 10869, 10870, 10871, 10872, 10873, 10874, 10875, 10876, 10877, 10878, 10879, 10880, 10881, 10882, 10883, 10884, 10885, 10886, 10887, 10888, 10889, 10890, 10891, 10892, 10893, 10894, 10895, 10896, 10897, 10898, 10899, 10900, 10901, 10902, 10903, 10904, 10905, 10906, 10907, 10908, 10909, 10910, 10911, 10912, 10913, 10914, 10915, 10916, 10917, 10918, 10919, 10920, 10921, 10922, 10923, 10924, 10925, 10926, 10927, 10928, 10929, 10930, 10931, 10932, 10933, 10934, 10935, 10936, 10937, 10938, 10939, 10940, 10941, 10942, 10943, 10944, 10945, 10946, 10947, 10948, 10949, 10950, 10951, 10952, 10953, 10954, 10955, 10956, 10957, 10958, 10959, 10960, 10961, 10962, 10963, 10964, 10965, 10966, 10967, 10968, 10969, 10970, 10971, 10972, 10973, 10974, 10975, 10976, 10977, 10978, 10979, 10980, 10981, 10982, 10983, 10984, 10985, 10986, 10987, 10988, 10989, 10990, 10991, 10992, 10993, 10994, 10995, 10996, 10997, 10998, 10999, 11000]

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
        semanticAnalysis = '-0.999987,0.989999'

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
                if timeConstraint == True:
                    print("here")
                    #query = """INSERT INTO FEEDBACK VALUES(NULL, " """+ generaltext +""" ", '""" + emotion + """', '""" + timeSent + """', '"""+ rating +"""', ' """ + semanticAnalysis + ""')"""
                    part1 = """INSERT INTO FEEDBACK VALUES(NULL, " """ + generaltext
                    part2 = """ ", '""" + emotion 
                    part3 = "' , '" + timeSent + "' , '"+rating + "', '" + semanticAnalysis + "')"
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
            #mayve also return JSON with the meeting ID
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
            attendance = "INSERT INTO ATTENDANCE VALUES("+ meetingid +", " + str(companyid) + ", "+ anonymous + ")"
            print(attendance)
            cur.execute(attendance)

            #idk if this is right
            currently_live_meetings[meetingid].update_participants(companyid)

            print("success")
            con.commit()
            
            return "SUCCESS???"
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
            return "SUCCESS???"
        else:
            return("that meeting isn't ongoing", 400)
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
            meeting = template.make_new_meetings(each[3], each[5], 111, each[6], each[4], host, True)
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
                    return "SUCCESS???"
        
        if(not succesful_login):
            return ("wrong password",400)
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
