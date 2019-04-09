
import firebase_admin
from firebase_admin import credentials,firestore
import bcrypt 
cred = credentials.Certificate("flasktest-a0a4d-firebase-adminsdk-5dtv7-c2f201dc8a.json")
default_app = firebase_admin.initialize_app(cred)

dbfs = firestore.client()

def readfromfbHardConstraints():
    
    doc_ref1 = dbfs.collection(u'hard_constraints').document('hass').get().to_dict()
    doc_ref2 = dbfs.collection(u'hard_constraints').document('generic').get().to_dict()
    return doc_ref1,doc_ref2

        
def readfromfbProfConstraints():
    doc_ref = dbfs.collection(u'prof_constraints').get()

    dict_prof_constraints={}
    for doct in doc_ref:
        temp_dict = doct.to_dict()
        dict_prof_constraints[doct.id]=temp_dict
    return dict_prof_constraints


def readfromfbOneTimeConstraints():
    doc_ref = dbfs.collection(u'single_constraints').get()

    single_constraints={}
    for doct in doc_ref:
        temp_dict = doct.to_dict()
        single_constraints[doct.id]=temp_dict
    return single_constraints


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
def readfromfbTimeTable():
    doc_ref = dbfs.collection(u'timetable').get()
    ls_timetable=[]
    ls_name=[]
    for doct in doc_ref:

        ls_timetable.append(doct.to_dict())

        print(len(ls_timetable))
        ls_name.append(doct.id)
    
    # for doct in doc_ref:
    #     print(doct.id,"{}".format(doct.to_dict()))

    return (ls_name,ls_timetable)

def readHassAndWeeklyConstraints():
    generic = dbfs.collection(u'hard_constraints').document(u'generic').get().to_dict()
    hass = dbfs.collection(u'hard_constraints').document(u'hass').get().to_dict()
    return generic,hass

def auth(username,password):
    usr_details_ref = dbfs.collection(u'Course_coordinator').document('cc1').get().to_dict()
    return usr_details_ref['username']==username and bcrypt.checkpw(password.encode('utf8'),usr_details_ref['password'].encode('utf8'))



def readTestingTimeTable():
    doc_ref2 = dbfs.collection(u'testing').document('timetable1').get()
    return doc_ref2.to_dict()

def readprofConstraintsTest():
    doc_ref = dbfs.collection(u'prof_constraints_test').get()

    dict_prof_constraints={}
    for doct in doc_ref:
        temp_dict = doct.to_dict()
        dict_prof_constraints[doct.id]=temp_dict
    return dict_prof_constraints

#updating firebase stuff

def updateTimetable(data,table=u'finalised'):
    if table==u'finalised':
        docs=dbfs.collection(u'timetable').get()
        for doc in docs:
            doc.reference.delete()
    doc_ref = dbfs.collection(u'timetable').document(table)
    doc_ref.set(data)

def appendToSingleConstraint(data):
    doc_ref=dbfs.collection('single_constraints').document('week_'+data[0])
    doc_ref.set(data[1],merge=True)

def appendToProfConstraint(data):
    doc_ref=dbfs.collection('prof_constraints').document(data[0])
    doc_ref.set(data[1],merge=True)         


def eraseOneTimeConstraint(data):
    doc_ref = dbfs.collection(u'single_constraints').document(data[0])
    doc_ref.update({
        data[1]: firestore.DELETE_FIELD
    })
    if dbfs.collection(u'timetable').document(data[0]).get().exists:
        dbfs.collection(u'timetable').document(data[0]).delete()

def eraseOneProfConstraint(data):
    doc_ref = dbfs.collection(u'prof_constraints').document(data[0])
    doc_ref.update({
        data[1]: firestore.DELETE_FIELD
    })

def AddRoom(data):
    doc_ref = dbfs.collection(u'rooms').document('ISTDT4')
    doc_ref.set({data[0]:data[1]},merge=True)



# def copyProfconst():
#     doc_ref = dbfs.collection(u'prof_constraints').get()
    
#     for doct in doc_ref:
#         doc_ref2= dbfs.collection(u'prof_constraints_test').document(doct.id)
#         doc_ref2.set(doct.to_dict())
    