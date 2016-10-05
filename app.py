from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/")
@app.route("/login/")
def home():
    return render_template("form.html")

@app.route("/authenticate/", methods = ["POST"])
def auth():
    if(request.form['Choice'] == 'Login'):
        return  authen(request.form)
    elif(request.form['Choice'] == 'Register'):
        return regis(request.form)
    else:
        return home()

def authen(form):
    credentials = open("./data/credentials.csv", "r")
    usernames = []
    passwords = []
    for i in credentials.readlines():
        splitData = i.split(",")
        usernames.append(splitData[0])
        passwords.append(splitData[1])
    credentials.close()
    user = form['user']
    pw = form['pass']
    if(user in usernames):
        if(hash(pw) == passwords[usernames.find(user)]):
            return render_template("success.html")
        else:
            return render_template("form.html", message="Bad Password")
    else:
        return render_template("form.html", message="Bad Username")
    
    #return render_template("failure.html", result="Bad Result")

def regis(form):
    credentials = open("./data/credentials.csv", "r")
    usernames = []
    passwords = []
    for i in credentials.readlines():
        splitData = i.split(",")
        usernames.append(splitData[0])
        passwords.append(splitData[1])
    credentials.close();
    user = form['user']
    if(user in usernames):
        credentials.close()
        return render_template("form.html", message="Username Already Taken")
    else:
        usernames.append(user)
        passwords.append(hash(form['pass']))
        credentials = open("./data/credentials.csv", "w")
        for i in range(len(usernames)):
            credentials.write(usernames[i] + "," + passwords[i] + "\n")
        credentials.close()
        return render_template("form.html", message="Account Registration Successful")

def hash(string):
    return hashlib.md5(string).hexdigest()

    
    
if(__name__ == "__main__"):
    app.debug = True;
    app.run()
