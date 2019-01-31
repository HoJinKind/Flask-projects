
import pyrebase
from flask import Flask , request, jsonify, render_template
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
ref=firebaseConnect.firebaseCall()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():

    return "Hello ! this is our project! please upload your first excel!"+str(ref)

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

@app.route("/export", methods=['GET'])
def export_records():
    return 

@app.route("/about")
def about():
    return render_template("about.html",posts=posts)


if __name__ == '__main__':
    app.run(debug=True)

