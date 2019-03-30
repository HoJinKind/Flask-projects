import readwritefromFB
import chromosome
import copy
from random import random, choice, randint
#generates the finalised timetable, given all the constraints. if it fails, return all avail, unfiled timetable
class ModifyOneConstraint:
    def __init__(self,raw_rooms_timetable,prof_constraints,dict_one_constraint,dictOfRooms):
        self.dictOfRooms = dictOfRooms
        self.profConstraints =prof_constraints
        self.dict_one_constraint =dict_one_constraint
        self.lsOfSessions=[]
        self.hasscount=0
        self.eventName = dict_one_constraint['eventName']
        self.constraint_duration = int(dict_one_constraint['duration'])
        self.rooms_timetable = self.generate_rooms_timetable(raw_rooms_timetable)

        self.constraint_day = dict_one_constraint['day']
        self.constraint_startTime = int(dict_one_constraint['startTime'])
        self.week = dict_one_constraint['week']
        self.rooms_timetable=self.consolidate_clashes(self.rooms_timetable)
        self.fillInNewHass()
        
        success = self.populate_timetable()#if fail?
        
        if success:
            self.prepareForFirebase()#if fail, wont change
            self.success = True
        else:
            print('failed')
            self.success = False

    #converts object chromosome to dictionary, to store in database
    def prepareForFirebase(self):
        #transform all session objects to dictionary
        tempTimeTable= copy.deepcopy(self.rooms_timetable)
        for day in tempTimeTable:
            for room in tempTimeTable[day]:
                for index in range(len(tempTimeTable[day][room])):
                    if not( tempTimeTable[day][room][index] in ['available','generic','hass',self.eventName]  ):
                        tempTimeTable[day][room][index] = vars(tempTimeTable[day][room][index])
        readwritefromFB.updateTimetable(tempTimeTable,self.week)


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


    def fillInNewHass(self):
        a=0
        fufilled=False
        while not fufilled:
            a+=1
            if a==10000:
                return False
            tempStartTime,dayOfWeek=self.findRandomTimeSlot(self.hasscount)
            fufilled = self.check_all_room_clear(tempStartTime,dayOfWeek)
        self.insertNewHassTiming(dayOfWeek,self.hasscount,tempStartTime)
        return True


    def check_all_room_clear(self,startTime,day):
    #check if all rooms  clear , for the block, then we can put in hass
        for room in self.dictOfRooms.keys():
            for period in range(self.hasscount):
                if not self.rooms_timetable[day][room][startTime+period] in ['available','generic'] :
                    return False
        return True

    def insertNewHassTiming(self,day,duration,startTime):

        for room in self.dictOfRooms.keys():
                #for each class room , for that day, block out the timing
                #print(self.rooms_timetable['friday']['2.505'])
            for durations in range(duration):
                print(durations)
                self.rooms_timetable[day][room][durations+startTime]=u"hass"
                print('inserting for' +room)
                   
    
    def  check_room_available(self,room,duration,startTime,day):
        #check if for a specific day, time, room is available,m else, run the check for plus minus timing
        #make sure start not too late
        for i in range(duration):
            if not self.rooms_timetable[day][room][startTime+i] in ['available','generic']:
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
                if self.rooms_timetable[day][room][starttime+time] in ['available','generic']:
                    pass
                elif self.rooms_timetable[day][room][starttime+time]==self.rooms_timetable[day][room][starttime+time] in [self.eventName,'hass']:
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
                if self.rooms_timetable[day][key][starttime+time] in ['available','generic']:
                    pass
                #sneak in event name here
                elif self.rooms_timetable[day][key][starttime+time] in [self.eventName,'hass']:
                    return False
                else:
                    for cohort in self.rooms_timetable[day][key][starttime+time].cohortID:
                    #cycle thru list of cohorts
                        for cohortInQuestion in cohortsInQuestion:
                            if cohort == cohortInQuestion:
                                return False
        return True


    #purpose is to remove all classes which have clash now
    def consolidate_clashes(self,fbData): 
        print(str(self.constraint_duration)+"blabla")
        for index in range(self.constraint_duration):
            print(str(self.constraint_duration)+"blabla")
            for room in fbData[self.constraint_day].keys():
            
                #check if session, if yes, remove
                if self.check_if_session(fbData[self.constraint_day][room][index]):
                    currentTimeSlot=fbData[self.constraint_day][room][index]
                        
                    self.lsOfSessions.append(currentTimeSlot)
                    for duration in range(currentTimeSlot.duration):#remove from master copy
                        fbData[self.constraint_day][room][duration+index]=u"available"
                
                if fbData[self.constraint_day][room][index] == 'hass':
                    currentTimeSlot=fbData[self.constraint_day][room][index]
                    #have to remove entire hass block
                    while currentTimeSlot=='hass':
                        #check if next timeslot is also hass
                        try:
                            print(index+1000000)
                            currentTimeSlot=fbData[self.constraint_day][room][index+self.hasscount]
                            
                            for layer_two_room in self.dictOfRooms.keys():     
                                #set to avail for all rooms           
                                fbData[self.constraint_day][layer_two_room][self.hasscount+index]=u"available"
                            self.hasscount+=1   
                            #increase by 1
                            
                            currentTimeSlot=fbData[self.constraint_day][room][index+self.hasscount]
                        except IndexError as error:
                            #breaking more than once
                            break

                fbData[self.constraint_day][room][index]=self.eventName
                   
        print(str(self.hasscount)+'blablabla')               
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
        if data == 'available' or data == 'generic' or data == 'hass' or data == self.eventName:
            return False
        return True

def gen(dict_one_constraint):
    #get data required from firebase, then run.
    room_dict=readwritefromFB.readfromfbRoom()
    dict_prof_constraints= readwritefromFB.readfromfbProfConstraints()
    raw_rooms_timetable= readwritefromFB.readfromfbTimeTable()[1][0]
    modifier=ModifyOneConstraint(raw_rooms_timetable,dict_prof_constraints,dict_one_constraint,room_dict)
    return modifier.success