import readwritefromFB

class chromosome:

    def __init__(self,data,template):
        print(123)

class session:
    session_count=0
    def __init__(self,dicti,prof):
    #def __init__(self,prof,sessionID,startTime,duration,classID,roomtype):
        self.roomtype = dicti['location']
        duration_holder= int(float(dicti['duration'])*2)
        self.duration = duration_holder
        self.subject = dicti['subject']
        self.cohortID=dicti['cohorts']
        self.startTime = None
        if 'shared' in dicti.keys():
            self.profs = dicti['shared']
            self.profs.append(prof)
        else:
            self.profs = [prof]

        self.sessionid =session.session_count
        session.session_count+=1

    def __str__(self):
        return ' '.join(str(v) for v in ["sessionid:",self.sessionid,
                   "profs:",self.profs,
                   "cohorts",self.cohortID,
                   'subject:',self.subject])

def createSession():
    doc_ref = readwritefromFB.readfromfb()
    Allsessionslist = []
    ls_of_completed = []
    already_added=False
    dictionary_ofProfs = dict()
    for doct in doc_ref:
        # dictionary_ofProfs[doct.id]=doct.to_dict()
        temp_dict = doct.to_dict()
        for key, value in temp_dict.items():
            already_added = False
            if 'shared' in value.keys():
                for prof in value['shared']:
                    if prof in ls_of_completed:
                        # we have added this class already
                        already_added = True
            if not already_added:
                Allsessionslist.append(session(value, doct.id))
        ls_of_completed.append(doct.id)
    return Allsessionslist

        #     print(doct.id,"{}".format(doct.to_dict()))
