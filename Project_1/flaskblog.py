
import pyrebase
from flask import Flask


config = {
    "apiKey": "AIzaSyCCSwHNk4GoIJjIsE26CxE38-ZikAY5qcc",
    "authDomain": "flasktest-a0a4d.firebaseapp.com",
    "databaseURL": "https://flasktest-a0a4d.firebaseio.com",
    "projectId": "flasktest-a0a4d",
    "storageBucket": "flasktest-a0a4d.appspot.com",
    "messagingSenderId": "505357466043"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

db = firebase.database()
pyre_company = db.child("prof/oka/comp struc/class").get()#lel
ref ="Oka's class: "
for company in pyre_company.each():
    print(company.val())
    ref +="  " + str(company.val())

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():

    return "Hello !"+str(ref)



@app.route("/about")
def about():
    return "<h1>about !<h1>"


if __name__ == '__main__':
    app.run(debug=True)