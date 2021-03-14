# CS261-Software-Engineering
Group 7's CS261 Software Engineering project for Deutsche Bank

A meeting feedback system to provide real-time feedback to a meeting organiser using semantic text analysis.

Frontend - Create React App Project
Backend - Python Flask Web Server (Rest API)
Sentiment Analysis - Flair API sentiment analysis tool

To run follow the below instructions:

clone the repository to your local device using:
```
git clone https://github.com/joverandout/CS261-Software-Engineering/
```

From there navigate into the backend folder in order to run the backend python flask needs to be installed on your machine. Follow the following instructions to do that, https://flask.palletsprojects.com/en/1.1.x/installation/.

Once flask is installed within the `/backend` folder run the following commands:
```
$ pip install flask-cors
$ pip install flask_socketio
$ pip insall fpdf
$ pip install mathplotlib 
```
These commands will install the information to send data via sockets and also to create and format the pdf for the host to view the feedback. 
Then the following commands need to be run: 
```
$ python3 -m venv venv
$ . venv/bin/activate
$ export FLASK_APP="helloworld.py"
```
These commands will only work on Unix based operating systems (Linux or MacOs) for Windows use :
```
$ python -m venv venv
$ . venv/Scripts/activate
$ $env:FLASK_APP = "helloworld.py"
```
HERE NEED TO INSTALL FLAIR how to do this?? i have no idea 
To install flair for sentiment analysis ensure you at least have python version 6.6/ 3.7, then run the following commands:
```
$ pip install pytorch
$ pip install flair 
```

Once these commands are executed the back end can be run with the command:
```
$ flask run 
```
This should start the backend (this may also require the running of `pip install flask` to be able to initialise the local environment).

You should be able to tell the backend is running with the following message:

```
 * Serving Flask app "helloworld.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now to start the frontend, install npm (node package manager), navigate to `/frontend` and run:
```
$ npm install
$ npm start

Host User Details:
username:"John"
password:"pa$$word"

To access the attendee point of view, go to localhost:[port]/JoinMeeting
usernames: Tom, Linda, Bert, Jenny, Adam
```

This should (provided the backend was already running) startup the website and automatically open it in your default browser. To verify this is working you will see this in your console:

```
You can now view dbsep in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.0.29:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```
If it doesn't automatically open you can then click on the local link here in order to open it (in failing that it can be copied and pasted into your browser directly)
