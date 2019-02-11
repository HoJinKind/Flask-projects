
import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("flasktest-a0a4d-firebase-adminsdk-5dtv7-c2f201dc8a.json")
deafult_app=firebase_admin.initialize_app(cred)
dbfs = firestore.client()
def firebaseCall():

    doc_ref =dbfs.collection(u'class').document(u'YLOJ8PzfUsz0U2gSundW')
    doc_ref.update({'comp_struc.class.test':True})
    doc =doc_ref.get()
    print("{}".format(doc.to_dict()))
    config = {
        "apiKey": "AIzaSyCCSwHNk4GoIJjIsE26CxE38-ZikAY5qcc",
        "authDomain": "flasktest-a0a4d.firebaseapp.com",
        "databaseURL": "https://flasktest-a0a4d.firebaseio.com",
        "projectId": "flasktest-a0a4d",
        "storageBucket": "flasktest-a0a4d.appspot.com",
        "messagingSenderId": "505357466043"
    };
    dic = doc.to_dict()
    print(dic['comp struc']['prof'])#able to get data from firestore

    return "{}".format(doc.to_dict())