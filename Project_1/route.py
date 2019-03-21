
from flask import Flask , request, jsonify, render_template,redirect,url_for,session
import pandas as pd
import readwritefromFB
import generate1

posts =[
   {
        'prof': 'oka',
        'class': 'CS',
        'quantity':'3'
    } ,
       {
        'prof': 'gemma',
        'class': 'algo',
        'quantity':'3'
    },
       {
        'prof': 'datta',
        'class': 'algo',
        'quantity':'4'
    }
]

app = Flask(__name__)

app.secret_key = "super secret key"

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)
        return data_xls.to_html()
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''

@app.route("/export", methods=['GET','POST'])
def export_records():
    return

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

def create_pdFrame(dictionary_day_class_list,roomID):
    room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday'][roomID],
                                        'tuesday':dictionary_day_class_list['tuesday'][roomID],
                                        'wednesday':dictionary_day_class_list['wednesday'][roomID],
                                        'thursday':dictionary_day_class_list['thursday'][roomID],
                                        'friday':dictionary_day_class_list['friday'][roomID]})
    return room_example




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



@app.route("/view", methods=['GET','POST'])
def view():
    if not session['loggedIn']== True:
        return redirect(url_for('login'))
    dictionary_day_class_list = readwritefromFB.readfromfbTimeTable();
    room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday']['2.506'],
                                'tuesday':dictionary_day_class_list['tuesday']['2.506'],
                                'wednesday':dictionary_day_class_list['wednesday']['2.506'],
                                'thursday':dictionary_day_class_list['thursday']['2.506'],
                                'friday':dictionary_day_class_list['friday']['2.506']})
    room_example_html = room_example.to_html()
    return render_template('view.html', title='View',room_example=room_example_html)


if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')