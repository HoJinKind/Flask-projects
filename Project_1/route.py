import Modify
import ModifyOneConstraint
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


@app.route("/room", methods=['GET','POST'])
def room():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    rooms=readwritefromFB.readfromfbRoom()
    if request.method == 'POST':

        if request.form['add'] == 'add':
            roomtype=request.form['roomType']
            roomName=request.form['roomName']

            readwritefromFB.AddRoom([roomName,roomtype])

            return redirect(url_for('room'))
    return render_template('room.html', title='Room',rooms=rooms)

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
        return redirect(url_for('constraints_view'))
    return render_template('constraint_OneTime.html', title='Constraint_OneTime')


@app.route("/constraint_Prof", methods=['GET','POST'])
def modify_public():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    #add into firebase, if data is legit
    if request.method == 'POST':
        profName = request.form['profName']
        DayOfWeek = request.form['dayOfWeek']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        fmt = '%H:%M'
        time1  = datetime.strptime(startTime, fmt)
        time2  = datetime.strptime(endTime, fmt)
        firstClass= datetime.strptime('08:30', fmt)
        st=(time1-firstClass).total_seconds()/(60*30)
        duration= (time2-time1).total_seconds()/(60*30)
        if duration<0:
            print('failed')
            return render_template('constraint_Prof.html', title='Constraint_Prof')
        dataDict =[profName,{DayOfWeek:{'startTime':unicode(str(int(st)), "utf-8"),'duration':unicode(str(int(duration)), "utf-8")}}]
        readwritefromFB.appendToProfConstraint(dataDict) 
        return redirect(url_for('constraints_view'))
    return render_template('constraint_Prof.html', title='Constraint_Prof')

@app.route("/constraints_View", methods=['GET','POST'])
def constraints_view():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
        #convert time to date time
    profConstraints = readwritefromFB.readfromfbProfConstraints()
    for prof in profConstraints:
        for day in profConstraints[prof]:
            profConstraints[prof][day]['startTime'],profConstraints[prof][day]['endTime']=convertTimeUnitsToRealTime(profConstraints[prof][day])
    
        #convert time to date time
    oneTimeConstraints=readwritefromFB.readfromfbOneTimeConstraints()
    for week in oneTimeConstraints:
        for day in oneTimeConstraints[week]:
            oneTimeConstraints[week][day]['startTime'],oneTimeConstraints[week][day]['endTime']=convertTimeUnitsToRealTime(oneTimeConstraints[week][day])
    genericConstraints,hassConstraints= readwritefromFB.readHassAndWeeklyConstraints()
    lsHardConstraints=[]
    for day in hassConstraints:    
        tempdict={'event':'hass','day':day}
        tempdict['startTime'],tempdict['endTime']= convertTimeUnitsToRealTime(hassConstraints[day])
        lsHardConstraints.append(tempdict)
    for day in genericConstraints:    
        tempdict={'event':'generic','day':day}
        tempdict['startTime'],tempdict['endTime']= convertTimeUnitsToRealTime(genericConstraints[day])
        lsHardConstraints.append(tempdict)

    if request.method == 'POST':
        if 'modify' in request.form:
            if request.form['modify'] == 'Modify':
                #this works
                if Modify.gen():
                    return redirect(url_for('view'))
                else:
                    return redirect(url_for('constraints_view'))
        for prof in profConstraints:
            for day in profConstraints[prof]:
                if '%s,%s'%(prof,day) in request.form:
                    if request.form['%s,%s'%(prof,day)] == 'Remove':
                        #do smth
                        readwritefromFB.eraseOneProfConstraint([prof,day])
                        return redirect(url_for('constraints_view'))
        for week in oneTimeConstraints:
            for day in oneTimeConstraints[week]:
                if '%s,%s'%(week,day) in request.form:
                    if request.form['%s,%s'%(week,day)] == 'Remove':
                        #this works
                        readwritefromFB.eraseOneTimeConstraint([week,day])
                        return redirect(url_for('constraints_view'))
                    elif request.form['%s,%s'%(week,day)] == 'Generate':
                        dict_one_constraint=readwritefromFB.readfromfbOneTimeConstraints()[week][day]
                        dict_one_constraint['day']=day
                        dict_one_constraint['week']=week
                        dict_one_constraint['eventName']=oneTimeConstraints[week][day]['eventName']
                        ModifyOneConstraint.gen(dict_one_constraint)
                        #dosmth] == 'Generate':
                        #dosmth
                        return redirect(url_for('view'))
                    
    return render_template('constraints_View.html', title='Constraint_View', profConstraints=profConstraints,oneTimeConstraints=oneTimeConstraints,hardConstraints=lsHardConstraints)

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
