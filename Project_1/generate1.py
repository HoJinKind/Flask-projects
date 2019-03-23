import readwritefromFB
import chromosome
import copy
from random import random, choice, randint

class generate1:
    def __init__(self,lsOfSessions,dictOfRooms):
        self.dictOfRooms = dictOfRooms
        self.lsOfSessions = lsOfSessions

        self.nineteentAvail = [u'available' for i in range(19)]
        self.rooms_timetable={}
        self.generate_rooms_timetable()
        
        self.fill_in_hass_and_weekly()
        success = self.populate_timetable()
        if success:
            self.prepareForFirebase()
        else:
            self.nineteentAvail = [u'available' for i in range(19)]
            self.rooms_timetable={}
            self.generate_rooms_timetable()
            self.prepareForFirebase()

    def prepareForFirebase(self):
        #transform all session objects to dictionary
        tempTimeTable= copy.deepcopy(self.rooms_timetable)
        for day in tempTimeTable:
            for room in tempTimeTable[day]:
                for index in range(len(tempTimeTable[day][room])):
                    if not( tempTimeTable[day][room][index] == 'available' or tempTimeTable[day][room][index] == 'generic' or tempTimeTable[day][room][index] == 'hass'  ):
                        tempTimeTable[day][room][index] = vars(tempTimeTable[day][room][index])
        readwritefromFB.updateTimetable(tempTimeTable)


    def populate_timetable(self):
        for session in self.lsOfSessions:
            fufilled = False
            a=0
            while not fufilled:
                a+=1
                if a==10000:
                    return False
                #type of room has to be chosen
                tempRoom=self.findRandomRoom(self.dictOfRooms,session.roomtype)
                tempStartTime,dayOfWeek=self.findRandomTimeSlot(session.duration)
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
                                                            session.cohortID,
                                                            ))
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

    def check_weekly_constraints(self,duration,startTime):
        for i in range(duration):
            if not self.rooms_timetable[day][room][startTime+i] == 'available':
                print('room return false')
                return False
        print('room return true')
        return True
    
    def check_prof_available(self,duration,starttime,day,profsInQuestion):
        #check if prf is in any of these locations at the point in time
        for time in range(duration):
            #cycle thru time
            for key in self.rooms_timetable[day]:
                #cycle thru rooms
                if self.rooms_timetable[day][key][starttime+duration]=='available':
                    pass
                elif self.rooms_timetable[day][key][starttime+duration]=='generic' or  self.rooms_timetable[day][key][starttime+duration]=='hass':
                    return False
                else:
                    for prof in self.rooms_timetable[day][key][starttime+duration].profs:
                    #cycle thru list of profs
                        for profInQuestion in profsInQuestion:
                            #cycle thru list of profs in current session
                            if prof == profsInQuestion:
                                print('prof return false')
                                return False
        return True


    def check_students_available(self,duration,starttime,day,cohortsInQuestion):

        for time in range(duration):
            #cycle thru time
            for key in self.rooms_timetable[day]:
                #cycle thru rooms
                if self.rooms_timetable[day][key][starttime+duration]=='available':
                    pass
                elif self.rooms_timetable[day][key][starttime+duration]=='generic' or  self.rooms_timetable[day][key][starttime+duration]=='hass':
                    return False
                else:
                    for cohort in self.rooms_timetable[day][key][starttime+duration].cohortID:
                    #cycle thru list of cohorts
                        for cohortInQuestion in cohortsInQuestion:
                            if cohort == cohortInQuestion:
                                print('stu return false')
                                return False
        return True


            
        
        
        

# def generateTemplateTest(dictOfRooms):
#     template = {}
#     nineteentAvail = ['available' for i in range(19)]
#     for room in dictOfRooms:
#         if 'monday' not in template.keys():
#             template['monday'] = {room: nineteentAvail}
#         else:
#             template['monday'][room] = nineteentAvail
#
#         if 'tuesday' not in template.keys():
#             template['tuesday'] = {room: nineteentAvail}
#         else:
#             template['tuesday'][room] = nineteentAvail
#
#         if 'wednesday' not in template.keys():
#             template['wednesday'] = {room: nineteentAvail}
#         else:
#             template['wednesday'][room] = nineteentAvail
#
#         if 'thursday' not in template.keys():
#             template['thursday'] = {room: nineteentAvail}
#         else:
#             template['thursday'][room] = nineteentAvail
#
#         if 'friday' not in template.keys():
#             template['friday'] = {room: nineteentAvail}
#         else:
#             template['friday'][room] = nineteentAvail
#     return template
#
#
#
#
# temp= readfromFB.readfromfbRoom()
#
# roomdict = temp.to_dict()
# x = generateTemplateTest(roomdict)
#
# print(x['tuesday'])

# if __name__ == '__main__':
#     ls_chromosome=chromosome.createSession()
#     room_dict=readfromFB.readfromfbRoom()
#     firstGeneration=generate1(ls_chromosome,room_dict)
#     print(firstGeneration.rooms_timetable)
def gen():
    ls_chromosome=chromosome.createSession()
    room_dict=readwritefromFB.readfromfbRoom()
    firstGeneration=generate1(ls_chromosome,room_dict)
    return firstGeneration.rooms_timetable