
from flask import Flask , request, jsonify, render_template,redirect,url_for
import pandas as pd
import firebaseConnect

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
ref=str(firebaseConnect.firebaseCall())

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('upload_file'))

    ref=str(firebaseConnect.firebaseCall())
    print(ref)
    return render_template("home.html",ref=ref)

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

@app.route("/about", methods=['GET','POST'])
def about():

    return render_template('about.html', title='Login', form=form)



if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')

