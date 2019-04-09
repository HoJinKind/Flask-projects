import readwritefromFB
import chromosome
import copy
from random import random, choice, randint
import generate1Test
#These will be the test cases dont for the first algorithms
import pytest

def testOneSession():
    SessionParameters={'location':'lt','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints=dict())
    assert success
    
def testMultipleSessions():
    SessionParameters1={'location':'lt','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    SessionParameters2={'location':'lt','sessionid':'2','duration':'3','subject':'abc','cohorts':['class1']}
    Session1=chromosome.session(SessionParameters1,'Mrhamburger')
    Session2=chromosome.session(SessionParameters2,'Mrhamburger')
    rooms={'8.888':'lt'}
    success=generate1Test.gen([Session1,Session2],rooms,dict_prof_constraints=dict())
    assert success

def testOneSessionOneProfConstraint():
    #more hours than available
    SessionParameters={'location':'lt','sessionid':'1','duration':'2','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    dict_prof_constraints= {'Mrhamburger':{'monday':{'duration':'19','startTime':'0'}}}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints)
    assert success 

def testOneSessionOnePossibility():
    #more hours than available
    # #there is one slot, thursday afternoon 2-3pm, before HASS
    SessionParameters={'location':'lt','sessionid':'1','duration':'2','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    dict_prof_constraints= {
        'Mrhamburger':{
            'monday':{'duration':'19','startTime':'0'},
            'tuesday':{'duration':'19','startTime':'0'},
            'wednesday':{'duration':'19','startTime':'0'},
            'thursday':{'duration':'11','startTime':'0'},
            'friday':{'duration':'19','startTime':'0'}}}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints=dict())
    assert success

def testOneSessionTooLong():
    #more hours than available
    SessionParameters={'location':'lt','sessionid':'1','duration':'20','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints=dict())
    assert success ==False

def testOneSessionNoAvailRoomType():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints=dict())
    assert success == False
    


def testOneSessionTooManyConstraints():
    #more hours than available
    SessionParameters={'location':'lt','sessionid':'1','duration':'2','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'8.888':'lt'}
    dict_prof_constraints= {
        'Mrhamburger':{
            'monday':{'duration':'19','startTime':'0'},
            'tuesday':{'duration':'19','startTime':'0'},
            'wednesday':{'duration':'19','startTime':'0'},
            'thursday':{'duration':'19','startTime':'0'},
            'friday':{'duration':'19','startTime':'0'}}}
    success=generate1Test.gen([oneClass],rooms,dict_prof_constraints)
    readwritefromFB.copyProfconst()
    assert success ==False