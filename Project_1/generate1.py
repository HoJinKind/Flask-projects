import readwritefromFB
import chromosome
import copy
from random import random, choice, randint
#generates the finalised timetable, given all the constraints. if it fails, return all avail, unfiled timetable
class generate1:
    def __init__(self,lsOfSessions,dictOfRooms,dict_prof_constraints):
        self.dictOfRooms = dictOfRooms
        self.lsOfSessions = lsOfSessions
        self.profConstraints =dict_prof_constraints
        self.profsPriority={}
        self.nineteentAvail = [u'available' for i in range(19)]
        self.rooms_timetable={}
        self.SetPriorityOfProfs()
        self.setPriorityValueForSession()
        self.generate_rooms_timetable()
        self.fill_in_hass_and_weekly()
        self.success = self.populate_timetable()
        if self.success:
            self.prepareForFirebase()
        else:
            self.nineteentAvail = [u'available' for i in range(19)]
            self.rooms_timetable={}
            self.generate_rooms_timetable()
            self.prepareForFirebase()
        
    #converts object chromosome to dictionary, to store in database
    def prepareForFirebase(self):
        #transform all session objects to dictionary
        tempTimeTable= copy.deepcopy(self.rooms_timetable)
        for day in tempTimeTable:
            for room in tempTimeTable[day]:
                for index in range(len(tempTimeTable[day][room])):
                    if not( tempTimeTable[day][room][index] == 'available' or tempTimeTable[day][room][index] == 'generic' or tempTimeTable[day][room][index] == 'hass'  ):
                        tempTimeTable[day][room][index] = vars(tempTimeTable[day][room][index])
        readwritefromFB.updateTimetable(tempTimeTable)
    #this is for setting priority of profs, so we can then set priority of sessions
    def SetPriorityOfProfs(self):
        for prof in self.profConstraints.keys():
            for day in self.profConstraints[prof].keys():
                if prof in self.profsPriority:
                    self.profsPriority[prof]+=int(self.profConstraints[prof][day]["duration"])
                else:
                    self.profsPriority[prof]=int(self.profConstraints[prof][day]["duration"])

    
    def setPriorityValueForSession(self):
        for session in self.lsOfSessions:
            for prof in session.profs:
                if prof in self.profsPriority.keys():
                    session.priority=max(session.priority,self.profsPriority[prof])
        self.lsOfSessions.sort(key=lambda x: x.priority, reverse = True) 
    def populate_timetable(self):
        for session in self.lsOfSessions:
            fufilled = False
            count=0
            while fufilled == False:
                tempRoom=self.findRandomRoom(self.dictOfRooms,session.roomtype)
                count+=1
                if count==10:
                    return False
                for tempStartTime in range(19-session.duration):
                    for dayOfWeek in self.rooms_timetable.keys():
                        #type of room has to be chosen
                        #tempStartTime,dayOfWeek=self.findRandomTimeSlot(session.duration)
                        print(tempStartTime,dayOfWeek,fufilled)
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
                        if fufilled ==True:
                            break
                    if fufilled == True:
                        break
            self.insertSession(session,tempStartTime,session.duration,dayOfWeek,tempRoom)
           
        return True


    


    def insertSession(self,session,startTime,duration,day,room):
        session.startTime = startTime
        for half_hour_block in range(duration):
            self.rooms_timetable[day][room][startTime+half_hour_block]=session
          


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





    def generate_rooms_timetable(self):
        for room in self.dictOfRooms:
            if 'monday' not in self.rooms_timetable.keys():
                self.rooms_timetable['monday']= {room:copy.deepcopy(copy.deepcopy(self.nineteentAvail))}
            else:
                self.rooms_timetable['monday'][room]=copy.deepcopy(self.nineteentAvail)

            if 'tuesday' not in self.rooms_timetable.keys():
                self.rooms_timetable['tuesday']= {room:copy.deepcopy(self.nineteentAvail)}
            else:
                self.rooms_timetable['tuesday'][room]=copy.deepcopy(self.nineteentAvail)

            if 'wednesday' not in self.rooms_timetable.keys():
                self.rooms_timetable['wednesday']= {room:copy.deepcopy(self.nineteentAvail)}
            else:
                self.rooms_timetable['wednesday'][room]=copy.deepcopy(self.nineteentAvail)

            if 'thursday' not in self.rooms_timetable.keys():
                self.rooms_timetable['thursday']= {room:copy.deepcopy(self.nineteentAvail)}
            else:
                self.rooms_timetable['thursday'][room]=copy.deepcopy(self.nineteentAvail)

            if 'friday' not in self.rooms_timetable.keys():
                self.rooms_timetable['friday'] = {room:copy.deepcopy(self.nineteentAvail)}
            else:
                self.rooms_timetable['friday'][room]=copy.deepcopy(self.nineteentAvail)


                       
     



    def fill_in_hass_and_weekly(self):
        genericConstraint,hassConstraint=readwritefromFB.readHassAndWeeklyConstraints()
        for key in genericConstraint:
            for room in self.rooms_timetable[key]:
            #for each class room , for that day, block out the timing
            #print(self.rooms_timetable['friday']['2.505'])
                for timeSlot in range(int(genericConstraint[key][u"duration"])):
                    self.rooms_timetable[key][room][timeSlot+int(genericConstraint[key][u"startTime"])]=u"generic"
        for key in hassConstraint:
            for room in self.rooms_timetable[key]:
            #for each class room , for that day, block out the timing
            #print(self.rooms_timetable['friday']['2.505'])
                for timeSlot in range(int(hassConstraint[key][u"duration"])):
                    self.rooms_timetable[key][room][timeSlot+int(hassConstraint[key][u"startTime"])]=u"hass"
                       



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
                        print(self.rooms_timetable[day][room][starttime+time].profs)
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


            
        
        
def gen():
    ls_chromosome=chromosome.createSession()
    room_dict=readwritefromFB.readfromfbRoom()
    dict_prof_constraints= readwritefromFB.readfromfbProfConstraints()
    print(dict_prof_constraints)
    firstGeneration=generate1(ls_chromosome,room_dict,dict_prof_constraints)
    return firstGeneration.success