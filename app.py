from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/login/")
def home():
    return render_template("form.html")

@app.route("/authenticate/", methods = ["POST"])
def auth():
    if(request.form['user'] == 'admin' and request.form['pass'] == 'admin'):
        return render_template("success.html")
    else:
        return render_template("failure.html")

if(__name__ == "__main__"):
    app.debug = True;
    app.run()
