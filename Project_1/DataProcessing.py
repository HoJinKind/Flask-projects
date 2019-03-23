import pandas as pd
def create_list_pdFrame(fbDataTimeTable):
    list_pdFrame=[]
    ls_rooms=[]
    for i in fbDataTimeTable['monday'].keys():
        list_pdFrame.append(create_pdFrame(fbDataTimeTable,i))
        ls_rooms.append(i)
        print(i)
    return list_pdFrame,ls_rooms

def create_pdFrame(dictionary_day_class_list,roomID):
    room_example=pd.DataFrame({'monday':dictionary_day_class_list['monday'][roomID],
                                        'tuesday':dictionary_day_class_list['tuesday'][roomID],
                                        'wednesday':dictionary_day_class_list['wednesday'][roomID],
                                        'thursday':dictionary_day_class_list['thursday'][roomID],
                                        'friday':dictionary_day_class_list['friday'][roomID]})
    return room_example


def convertSessionToStrings(dictionary_day_class_list):
    for day in dictionary_day_class_list.keys():
        for classroom in dictionary_day_class_list[day].keys():
            for timeSlot in range(0,19):
                temp_dict =dictionary_day_class_list[day][classroom][timeSlot]

                if type(temp_dict) == dict :
                    tempstr= ""
                    #convert to str, take name
                    tempstr=tempstr +'cohorts:' +str(temp_dict[u'cohortID'])

                    tempstr=tempstr +'  profs:' +str(temp_dict[u'profs'])
                    tempstr=tempstr +'  subject:' +str(temp_dict[u'subject'])
                    dictionary_day_class_list[day][classroom][timeSlot]=tempstr
    return dictionary_day_class_list