
import firebase_admin
from firebase_admin import credentials,firestore
import bcrypt 
cred = credentials.Certificate("flasktest-a0a4d-firebase-adminsdk-5dtv7-c2f201dc8a.json")
default_app = firebase_admin.initialize_app(cred)

dbfs = firestore.client()


def readfromfb():
    doc_ref = dbfs.collection(u'dummy').get()

    # for doct in doc_ref:
    #     print(doct.id,"{}".format(doct.to_dict()))
    return doc_ref

def readfromfbRoom():

    doc_ref = dbfs.collection(u'rooms').document('ISTDT4').get()

    # for doct in doc_ref:
    #     print(doct.id,"{}".format(doct.to_dict()))
    return doc_ref.to_dict()

#readfromfb()

def updateTimetable(data):
    doc_ref = dbfs.collection(u'timetable').document(u'finalised')
    doc_ref.set(data)

def auth(username,password):
    usr_details_ref = dbfs.collection(u'Course_coordinator').document('cc1').get().to_dict()
    return usr_details_ref['username']==username and bcrypt.checkpw(password.encode('utf8'),usr_details_ref['password'].encode('utf8'))
