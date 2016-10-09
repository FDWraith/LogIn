from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
 
app = Flask(__name__)
app.secret_key = "hello"


@app.route("/")
def home():
    credentials = open("./data/credentials.csv", "r")
    usernames = []
    for i in credentials.readlines():
        if( i != '\n'):
            splitData = i.strip('\n').split(",")
            usernames.append(splitData[0])
    credentials.close()
    if('user' not in session.keys() or  session['user'] not in usernames):
        return redirect(url_for('login'))
    else:
        return render_template("home.html")

    
@app.route("/login/")
def login():
    return render_template("form.html")

@app.route("/authenticate/", methods = ["POST"])
def auth():
    if(request.form['Choice'] == 'Login'):
        return authen(request.form)
    elif(request.form['Choice'] == 'Register'):
        return regis(request.form)
    else:
        return login()

@app.route("/logout/")
def logout():
    session['user'] = ''
    return redirect(url_for("home"))

    
def authen(form):
    data = extractData()
    usernames = data[0]
    passwords = data[1]
    user = form['user']
    pw = form['pass']
    if user in usernames:
        if(hash(pw) == passwords[usernames.index(user)]):
            session['user'] = user
            return redirect(url_for('home'))
        else:
            return render_template("form.html", message="Bad Password")
    else:
        return render_template("form.html", message="Bad Username")

def regis(form):
    data = extractData()
    usernames = data[0]
    user = form['user']
    if user in usernames:
        credentials.close()
        return render_template("form.html", message="Username Already Taken")
    else:
        addUser(user,data)
        return render_template("form.html", message="Account Registration Successful")

def hash(string):
    return hashlib.md5(string).hexdigest()
def extractData():
    credentials = open("./data/credentials.csv", "r")
    usernames = []
    passwords = []
    for i in credentials.readlines():
        if( i != '\n'):
            splitData = i.strip("\n").split(",")
            usernames.append(splitData[0])
            passwords.append(splitData[1])
    credentials.close();
    data = [usernames, passwords ]
    return data;
def addUser(user,dataList):
    usernames = dataList[0];
    passwords = dataList[1];
    usernames.append(user)
    passwords.append(hash(form['pass']))
    credentials = open("./data/credentials.csv", "w")
    for i in range(len(usernames)):
        credentials.write(usernames[i] + "," + passwords[i] + "\n")
    credentials.close()
    
if(__name__ == "__main__"):
    app.debug = True;
    app.run()

