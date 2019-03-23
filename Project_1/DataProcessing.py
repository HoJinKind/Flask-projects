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
    day_order=['monday','tuesday','wednesday','thursday','friday']
    room_example = room_example.reindex(columns=day_order)
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

def convertPandasToHTML(ls_timeTable_in_pdframe):
    room_example_html_list=[]
    for room_example in ls_timeTable_in_pdframe:
        room_example.rename(index={0:'8:30',1:'9:00',2:'9:30',3:'10:00',4:'10:30',5:'11:00',6:'11:30',7:'12:00',8:'12:30',9:'13:00',10:'13:30',11:'14:00',12:'14:30',13:'15:00',14:'15:30',15:'16:00',16:'16:30',17:'17:00', 18:'17:30'},inplace =True)
        room_example_html_list.append(room_example.to_html())
    return room_example_html_list
