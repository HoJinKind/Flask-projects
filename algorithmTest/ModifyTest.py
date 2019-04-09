import readwritefromFB
import chromosome
import copy
from random import random, choice, randint
#generates the finalised timetable, given all the constraints. if it fails, return all avail, unfiled timetable
class modify:
    def __init__(self,raw_rooms_timetable,new_prof_constraints,dictOfRooms):
        self.dictOfRooms = dictOfRooms
        self.profConstraints =new_prof_constraints
        self.lsOfSessions=[]
        self.rooms_timetable = self.generate_rooms_timetable(raw_rooms_timetable)

        self.rooms_timetable=self.consolidate_clashes(self.rooms_timetable)
        print(self.lsOfSessions)

        success = self.populate_timetable()#if fail?
        
        if success:
            self.success = True
        else:
            print('failed')
            self.success = False


    def populate_timetable(self):
        for session in self.lsOfSessions:
            fufilled = False
            a=0
            while not fufilled:
                print(session.profs)
                a+=1
                if a==10000:
                    print(session.profs)
                    return False
                #type of room has to be chosen
                tempRoom=self.findRandomRoom(self.dictOfRooms,session.roomtype)
                tempStartTime,dayOfWeek=self.findRandomTimeSlot(session.duration)
                #this is where the checks are
                fufilled = (self.check_prof_available(session.duration,
                                tempStartTime,
                                dayOfWeek,
                                session.profs) and
                            self.check_room_available(tempRoom,
                                session.duration,
                                tempStartTime,
                                dayOfWeek) and
                            self.check_students_available(session.duration,
                                tempStartTime,
                                dayOfWeek,
                                session.cohortID) and
                            self.check_prof_constraints(session.profs,
                                session.duration,
                                dayOfWeek,
                                tempStartTime))
                session.startTime= tempStartTime
            self.insertSession(session,tempStartTime,session.duration,dayOfWeek,tempRoom)
        return True


    


    def insertSession(self,session,startTime,duration,day,room):
        print('impt! inserting sessionID',session.sessionid,session.subject)
        print(duration,'This is duration',startTime)
        for half_hour_block in range(duration):
            print('input into table',half_hour_block,room)
            print(room in self.rooms_timetable[day].keys())
            self.rooms_timetable[day][room][startTime+half_hour_block]=session
            print(123,self.rooms_timetable[day][room])
            print(vars(session))


    def findRandomRoom(self,dict_room,room_needed):
        #pick a eligible random room
        while True:
            key = choice(list(dict_room))
            if dict_room[key] == room_needed:
                return key
    #TODO change to earliest timeslot, since picking, have to get latest?
    def findRandomTimeSlot(self,duration):
        #find random timeslot for session
        days=['monday','tuesday','wednesday','thursday','friday']
        return (randint(0,19-duration-1),choice(days))







    
    def  check_room_available(self,room,duration,startTime,day):
        #check if for a specific day, time, room is available,m else, run the check for plus minus timing
        #make sure start not too late
        for i in range(duration):
            if not self.rooms_timetable[day][room][startTime+i] == 'available':
                print('room return false')
                return False
        print('room return true')
        return True

    def check_prof_constraints(self,profsInQuestion,duration,day,startTime):
        for classTiming in range(startTime,startTime+duration):
            for profInQuestion in profsInQuestion:
                if profInQuestion in self.profConstraints.keys():
                    if day in self.profConstraints[profInQuestion].keys():
                        constraintStartTime=int(self.profConstraints[profInQuestion][day]['startTime'])
                        constraintDuration=int(self.profConstraints[profInQuestion][day]['duration'])
                        for constraintTiming in range(constraintStartTime,constraintDuration+constraintStartTime):
                            if constraintTiming == classTiming:
                                return False
        return True



    
    def check_prof_available(self,duration,starttime,day,profsInQuestion):
        #check if prf is in any of these locations at the point in time
        for time in range(duration):
            #cycle thru time
            for room in self.rooms_timetable[day].keys():
                #cycle thru rooms
                if self.rooms_timetable[day][room][starttime+time]=='available':
                    pass
                elif self.rooms_timetable[day][room][starttime+time]=='generic' or  self.rooms_timetable[day][room][starttime+time]=='hass':
                    return False
                else:
                    #for list of profs, teaching in the same  hr
                    for prof in self.rooms_timetable[day][room][starttime+time].profs:
                    #cycle thru list of profs
                        for profInQuestion in profsInQuestion:
                            #cycle thru list of profs in current session
                            if prof == profInQuestion:
                                print('prof return false')
                                return False
        return True




    def check_students_available(self,duration,starttime,day,cohortsInQuestion):

        for time in range(duration):
            #cycle thru time
            for key in self.rooms_timetable[day]:
                #cycle thru rooms
                if self.rooms_timetable[day][key][starttime+time]=='available':
                    pass
                elif self.rooms_timetable[day][key][starttime+time]=='generic' or  self.rooms_timetable[day][key][starttime+time]=='hass':
                    return False
                else:
                    for cohort in self.rooms_timetable[day][key][starttime+time].cohortID:
                    #cycle thru list of cohorts
                        for cohortInQuestion in cohortsInQuestion:
                            if cohort == cohortInQuestion:
                                print('stu return false')
                                return False
        return True


    #purpose is to remove alll classes which have clash now
    def consolidate_clashes(self,fbData): 
        for day in fbData.keys():
            for room in fbData[day].keys():
                for index in range(len(fbData[day][room])):
                    if self.check_if_session(fbData[day][room][index]):
                        currentTimeSlot=fbData[day][room][index]
                    
                        if not self.check_prof_constraints(currentTimeSlot.profs,currentTimeSlot.duration,day,currentTimeSlot.startTime):
                           
                            self.lsOfSessions.append(currentTimeSlot)
                            for duration in range(currentTimeSlot.duration):#remove from master copy
                                fbData[day][room][duration+index]=u"available"
                                
        return fbData

    #purpose is to CONVERT to session again
    def generate_rooms_timetable(self,fbData):
        for day in fbData.keys():
            for room in fbData[day].keys():
                for index in range(len(fbData[day][room])):
                    if self.check_if_session(fbData[day][room][index]):
                        fbData[day][room][index]= chromosome.session(fbData[day][room][index])
        return fbData
        
    def check_if_session(self,data):
        if data == 'available' or data == 'generic' or data == 'hass':
            return False
        return True

def gen(room_dict,dict_prof_constraints,raw_rooms_timetable):
    #get data required from firebase, then run.
    #room_dict=readwritefromFB.readfromfbRoom()
    #dict_prof_constraints= readwritefromFB.readfromfbProfConstraints()#needed
    #raw_rooms_timetable= readwritefromFB.readTestingTimeTable()
    modifier=modify(raw_rooms_timetable,dict_prof_constraints,room_dict)
    return modifier.success