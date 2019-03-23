
from flask import Flask , request, jsonify, render_template,redirect,url_for,session
import pandas as pd
import readwritefromFB
import generate1
from flask_nav import Nav
from flask_nav.elements import Navbar,Subgroup,View,Link,Text,Separator
import re


app = Flask(__name__)
# nav = Nav(app)
# nav.register_element('my_navbar',Navbar(
#     'theNav'),
#     View('H'))
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
            dictionary_day_class_list= generate1.gen()

            return redirect(url_for('view'))
            # room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday']['2.506'],
            #                             'tuesday':dictionary_day_class_list['tuesday']['2.506'],
            #                             'wednesday':dictionary_day_class_list['wednesday']['2.506'],
            #                             'thursday':dictionary_day_class_list['thursday']['2.506'],
            #                             'friday':dictionary_day_class_list['friday']['2.506']})
            # return room_example.to_html()
            #df = pd.DataFrame(np.array(my_list).reshape(3,3), columns = list("abc"))
    return render_template('generate.html', title='Generate')



def auth(username,pd):
    if readwritefromFB.auth(username,pd):
        session['loggedIn']= True

def goToGenerate():
   redirect(url_for('generate'))

<<<<<<< HEAD
=======


>>>>>>> 00e1ab293bf3f13e2e942930b15b029fffa2bb6c


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
    return render_template('constraint_OneTime.html', title='Constraint_OneTime')

@app.route("/constraint_Prof", methods=['GET','POST'])
def modify_public():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    return render_template('constraint_Prof.html', title='Constraint_Prof')



def create_list_pdFrame(fbDataTimeTable):
    list_pdFrame=[]
    ls_rooms=[]
    for i in fbDataTimeTable['monday'].keys():
        list_pdFrame.append(create_pdFrame(fbDataTimeTable,i))
        ls_rooms.append(i)
        print(i)
    return list_pdFrame,ls_rooms

def create_pdFrame(dictionary_day_class_list,roomID):
    room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday'][roomID],
                                        'tuesday':dictionary_day_class_list['tuesday'][roomID],
                                        'wednesday':dictionary_day_class_list['wednesday'][roomID],
                                        'thursday':dictionary_day_class_list['thursday'][roomID],
                                        'friday':dictionary_day_class_list['friday'][roomID]})
    return room_example


@app.route("/view", methods=['GET','POST'])
def view():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    dictionary_day_class_list = readwritefromFB.readfromfbTimeTable();
<<<<<<< HEAD
    
    #needs triple for loop for day of wk and class, and hr,
    for day in dictionary_day_class_list.keys():
        for classroom in dictionary_day_class_list[day].keys():
            for timeSlot in range(0,19):
                temp_dict =dictionary_day_class_list[day][classroom][timeSlot]

                if type(temp_dict) == dict :
                    tempstr= ""
                    #convert to str, take name
                    tempstr=tempstr +'cohorts:' +str(temp_dict[u'cohortID'])

                    tempstr=tempstr +'  profs:' +str(temp_dict[u'profs'])
                    tempstr=tempstr +'  subject:' +str(temp_dict[u'subject'])
                    dictionary_day_class_list[day][classroom][timeSlot]=tempstr
             

    pd.set_option('display.max_colwidth', -1)
    
    ls_timeTable_in_pdframe,ls_rooms=create_list_pdFrame(dictionary_day_class_list)
    
    #room_example.rename(index={0:'Adasda'})
    room_example_html_list=[]
    for room_example in ls_timeTable_in_pdframe:
        room_example_html_list.append(room_example.to_html())
    #need to make a list of them.

    return render_template('view.html', title='View',room_example=room_example_html_list,ls_rooms=ls_rooms)
=======
    room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday']['2.506'],
                                'tuesday':dictionary_day_class_list['tuesday']['2.506'],
                                'wednesday':dictionary_day_class_list['wednesday']['2.506'],
                                'thursday':dictionary_day_class_list['thursday']['2.506'],
                                'friday':dictionary_day_class_list['friday']['2.506']})
    room_example_html = room_example.to_html()
    return render_template('view.html', title='View',room_example=room_example_html)
>>>>>>> 00e1ab293bf3f13e2e942930b15b029fffa2bb6c


if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')
