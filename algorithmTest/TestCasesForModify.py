#this test the modify algorithm, which takes in prof constraints, and shld there be new constraints, reschedule these classes.

import readwritefromFB
import chromosome
import copy
from random import random, choice, randint
import ModifyTest
#These will be the test cases dont for the first algorithms
import pytest


def testModifyAddOneBlockConstraints():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['gemma']={'monday':{'duration':'1','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success


def testModifyAddUnSatisfiableConstraints():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['gemma']={
            'monday':{'duration':'19','startTime':'0'},
            'tuesday':{'duration':'19','startTime':'0'},
            'wednesday':{'duration':'19','startTime':'0'},
            'thursday':{'duration':'19','startTime':'0'},
            'friday':{'duration':'19','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success ==False

def testModifyAddTwoNewProfsConstraints():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['gemma']={'monday':{'duration':'1','startTime':'0'}}
    dict_prof_constraints['ernest']={'monday':{'duration':'5','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success

#adding prof constraint of prof not inside, should not cause problem
def testModifyProfNotInTimetable():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['Mrhamburger']={'monday':{'duration':'10','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success

def testModifyAddProfFullDayConstraint():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['gemma']={'monday':{'duration':'19','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success

def testModifyAddNoMorningsConstraint():
    SessionParameters={'location':'ballroom','sessionid':'1','duration':'3','subject':'abc','cohorts':['class1']}
    oneClass=chromosome.session(SessionParameters,'Mrhamburger')
    rooms={'2.505':'lt','2.506':'cc','2.507':'cc'}
    raw_roomsTimetable = readwritefromFB.readTestingTimeTable()
    dict_prof_constraints=readwritefromFB.readprofConstraintsTest()
    dict_prof_constraints['gemma']=    dict_prof_constraints['gemma']={
            'monday':{'duration':'4','startTime':'0'},
            'tuesday':{'duration':'4','startTime':'0'},
            'wednesday':{'duration':'4','startTime':'0'},
            'thursday':{'duration':'4','startTime':'0'},
            'friday':{'duration':'4','startTime':'0'}}
    success= ModifyTest.gen(rooms,dict_prof_constraints,raw_roomsTimetable)
    assert success

    