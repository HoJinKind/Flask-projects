import Modify
from flask import Flask , request, jsonify, render_template,redirect,url_for,session
import pandas as pd
import readwritefromFB
import generate1
from flask_nav import Nav
from flask_nav.elements import Navbar,Subgroup,View,Link,Text,Separator
import re
from DataProcessing import *
from datetime import *
pd.set_option('display.max_colwidth', -1)
app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/", methods=['GET','POST'])
def login():
    session['loggedIn']= None
    if request.method == 'POST':
        usrname = request.form['username']
        pd = request.form['pd']

        auth(usrname,pd)
    if session['loggedIn']== True:
        return redirect(url_for('home'))

    return render_template('login.html', title='Log in')

@app.route("/home", methods=['GET','POST'])
def home():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))

    return render_template('home.html', title='Home')

@app.route("/generate", methods=['GET','POST'])
def generate():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    if request.method == 'POST':
        generate1.gen()
        return redirect(url_for('view'))
    return render_template('generate.html', title='Generate')



def auth(username,pd):
    if readwritefromFB.auth(username,pd):
        session['loggedIn']= True

def goToGenerate():
   redirect(url_for('generate'))



@app.route("/modify", methods=['GET','POST'])
def modify():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    return render_template('modify.html', title='Modify')


@app.route("/constraints", methods=['GET','POST'])
def constraints():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    return render_template('constraints.html', title='Constraints')


@app.route("/constraint_OneTime", methods=['GET','POST'])
def modify_event():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    #add into firebase, if data is legit
    if request.method == 'POST':
        eventName = request.form['eventName']
        WeekNo = request.form['weekNo']
        DayOfWeek = request.form['dayOfWeek']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        print(type(endTime))
        fmt = '%H:%M'
        time1  = datetime.strptime(startTime, fmt)
        time2  = datetime.strptime(endTime, fmt)
        firstClass= datetime.strptime('08:30', fmt)
        st=(time1-firstClass).total_seconds()/(60*30)
        duration= (time2-time1).total_seconds()/(60*30)
        if duration<0:
            print('failed')
            return render_template('constraint_OneTime.html', title='Constraint_OneTime')
        dataDict =[WeekNo,{DayOfWeek:{'startTime':unicode(str(int(st)), "utf-8"),'duration':unicode(str(int(duration)), "utf-8"),'eventName':eventName}}]
        readwritefromFB.appendToSingleConstraint(dataDict)
        return render_template('constraints.html', title='Constraint_OneTime')
    
    return render_template('constraint_OneTime.html', title='Constraint_OneTime')


@app.route("/constraint_Prof", methods=['GET','POST'])
def modify_public():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    return render_template('constraint_Prof.html', title='Constraint_Prof')



@app.route("/view", methods=['GET','POST'])
def view():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    ls_names,ls_dictionary_day_class_list = readwritefromFB.readfromfbTimeTable();
    list_of_week_type=[]
    for i in range(len(ls_names)):
        dictionary_day_class_list = convertSessionToStrings(ls_dictionary_day_class_list[i])
    #needs triple for loop for day of wk and class, and hr,
        ls_timeTable_in_pdframe,ls_rooms =create_list_pdFrame(dictionary_day_class_list)
    
        list_of_week_type.append(convertPandasToHTML(ls_timeTable_in_pdframe))

    #need to make a list of them.
    return render_template('view.html', title='View',list_of_week_type=list_of_week_type,ls_rooms=ls_rooms,ls_names=ls_names)


if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')
