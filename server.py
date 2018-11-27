import json
from flask import Flask, request, session
from flask_cors import CORS
from argon2 import PasswordHasher
import sqlite3
app = Flask(__name__)
CORS(app)

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<your key here>',
    consumer_secret='<your secret here>'
)

# endpoint for login, a post method
@app.route('/login', methods=['POST'])
def loginRequest():
    # gets data passed in request - username & password
    data = json.loads(request.data);
    userVal = data['username'];
    passVal = data['password'];
    try:
        # gets password from database and check they are equal to what was entered
        existingPassHash = getStoredPassForUser(userVal); #If this throws exception, there is no username, drop into except block
        verified = verifyPassword(existingPassHash, passVal)
        if (verified):
            name = getNameForUser(userVal) #gets their name to welcome them nicely
        # if successful, greet, otherwise tell them the password was incorrect
        result = 'Login successful. Welcome ' + name + '!' if verified else 'Incorrect password';
        success = True;
    except:
        # if the username wasn't in the database
        result = 'Username not found';
        success = False;
    # returns information about the result/success of the login 
    return json.dumps({'result':result, 'success': success});

# endpoint for a signup request, post method
@app.route('/signup', methods=['POST'])
def signupRequest():
    # gets data from client request, name, username and pass
    data = json.loads(request.data);
    name = data['name'];
    userVal = data['username'];
    passVal = data['password'];
    try:
        # store user and pass in database
        storeUserAndPass(userVal, name, ph.hash(passVal))
        result = 'Account creation successful';
    except:
        result = 'Failure!';
    #return result of signup
    return json.dumps({'result':result});

# method to verify a password, true if match, false otherwise
def verifyPassword(saved_hash, input_password_attempt):
    try:
        # verify by checking the hashed password to the entered password
        ph.verify(saved_hash, input_password_attempt);
        return True;
    except:
        return False;

# method to store new username and password
def storeUserAndPass(username, name, password):
    try:
        # check if username already exists in database
        getStoredPassForUser(username);
        usernameExists = True;
    except:
        usernameExists = False;
    if not usernameExists:
        # connect to the database
        conn = sqlite3.connect(sqlite_file);
        c = conn.cursor();
        # insert statement to add new user with given values (hashed password already)
        c.execute("insert into users values ('{}', '{}', '{}')".format(username, name, password));
        # closing connection
        conn.commit();
        conn.close();

# simple method to get only the name of a user
def getNameForUser(username):
    conn = sqlite3.connect(sqlite_file);
    c = conn.cursor();
    c.execute("select name from users where username = '{}'".format(username));
    result = c.fetchall()[0][0];
    conn.close();
    return result;

# simple method to get only the username of a user
def getStoredPassForUser(username):
    conn = sqlite3.connect(sqlite_file);
    c = conn.cursor();
    c.execute("select password from users where username = '{}'".format(username));
    result = c.fetchall()[0][0];
    conn.close();
    return result;

# method to remove a user from the database - not currently used but helpful if we want to have
# "deactivate account" or something similar
def removeUser(username):
    conn = sqlite3.connect(sqlite_file);
    c = conn.cursor();
    c.execute("delete from users where username = '{}'".format(username));
    conn.commit();
    conn.close();

# initializes the databases when the server starts
def initDB():
    try:
        # setup connection to a sqlite database
        conn = sqlite3.connect(sqlite_file);
        conn.close();
        success = True;
    # just in case it couldn't create the database - shouldn't be a problem
    except Exception as e:
        print(e);
        print("Invalid db path");
        success = False;
    if success:
        # connect to database
        conn = sqlite3.connect(sqlite_file);
        c = conn.cursor();
        try:
            # check if there is a database called users
            c.execute("select * from users");
        except:
            #if not, create it
            c.execute("create table users (username TEXT PRIMARY KEY, name TEXT, password TEXT)");
            c.execute("select * from users");
        try:
            # check if there is a database of calendar events
            c.execute("select * from calevents");
        except:
            #if not, create it
            c.execute("create table calevents (eventid INT PRIMARY KEY, username TEXT, name TEXT, date TEXT, starttime TEXT, endtime TEXT, eventname TEXT)");
            c.execute("select * from calevents");
        conn.close(); #close connection to db
    return success

# main method - starts server and creates database
if __name__ == '__main__':
    sqlite_file = './test_db.db';
    ph = PasswordHasher();
    dbInitialized = initDB();
    if (dbInitialized):
	    app.run(debug=True, port=5000) #run app in debug mode on port 5000
