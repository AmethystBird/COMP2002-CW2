from operator import truediv
import random
import copy

class Module:
    #Object variables
    moduleCode = ""
    lecturerName = ""
    moduleConflicts = []
    
    #Sessions attached
    lectures = 1
    labs = -1
    
    #Constructor
    def __init__(self, moduleCode, lecturerName, conflictingModules, labs):
        self.moduleCode = moduleCode
        self.lecturerName = lecturerName
        self.moduleConflicts = conflictingModules
        self.labs = labs
    
    def AssignLab():
        if (labs > 0):
            labs = labs - 1
        else:
            print("Error: Attempted assignment of lab when there are no labs to assign.")
    
    #Regular getters & setters
    def GetModuleCode():
        return self.moduleCode
    
    def SetModuleCode(name):
        this.moduleCode = moduleCode
    
    def GetLecturerName():
        return self.lecturerName
    
    def SetLecturerName(lecturerName):
        this.lecturerName = lecturerName
    
    def GetConflictingModules():
        return self.conflictingModules
    
    def SetConflictingModules(conflictingModules):
        this.conflictingModules = conflictingModules
    
    def GetLectures():
        return self.lectures
    
    def SetLectures(lectures):
        this.lectures = lectures
    
    def GetLabs():
        return self.lectures
    
    def SetLabs(labs):
        this.labs = labs

#A 3 day session within a day
class Session:
    lecture = "Empty"
    lab1 = "Empty"
    lab2 = "Empty"
    slots = [lecture, lab1, lab2]

modules = open("Modules.txt")
#print(modules.read())

#allModules = {}
allModules = []
#dictionaryIndex = 0

lectures = 1

def LoadAllModules(allModules):
    dictionaryIndex = 0
    for moduleAttributes in modules:
        moduleAttributesFormatted = moduleAttributes.split('|')
        moduleCode = moduleAttributesFormatted[0]
        lecturerName = moduleAttributesFormatted[1]
        sessionsUnformatted = moduleAttributesFormatted[2]
        labs = int(sessionsUnformatted)
        
        #print(moduleCode, lecturerName, lectures, labs)
        conflictingModules = moduleAttributesFormatted[3]
        conflictingModulesFormatted = conflictingModules.split(',')
        
        allModules.append(Module(moduleCode, lecturerName, conflictingModulesFormatted, labs))
        #allModules[dictionaryIndex] = Module(moduleCode, lecturerName, conflictingModules, labs)
        dictionaryIndex = dictionaryIndex + 1
    return allModules

#Create random timetable
blankTimetable = [["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"],
                  ["LectureEmpty", "Lab1Empty", "Lab2Empty"]]

#Create random timetable
randomTimetableConflicts = [[[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []],
                            [[], [], []]]

def TimetableRandomiser(randomTimetable, allModules, randomTimetableConflicts):
    for module in allModules:
        #Overlap checks if slot is empty or not
        overlap = 0
        while (overlap == 0):
            #Randomly selects lecture slot
            randomLectureSlot = random.randint(0, 19)

            #Checks if slot is empty, in which case assign lecture
            if randomTimetable[randomLectureSlot][0] == "LectureEmpty":
                randomTimetable[randomLectureSlot][0] = module.moduleCode
                randomTimetableConflicts[randomLectureSlot][0] = module.moduleConflicts
                overlap = 1
        #print("Lecture: ", randomTimetable[randomLectureSlot][0])
        
        overlap = 0
        while (overlap == 0):
            while (module.labs > 0):
                #Randomly selects 2D lab slot
                randomLabSlotX = random.randint(0, 19)
                randomLabSlotY = random.randint(1, 2)

                #Checks if slot is empty, in which case assign lab
                if randomTimetable[randomLabSlotX][randomLabSlotY] == "Lab1Empty" or "Lab2Empty":
                    randomTimetable[randomLabSlotX][randomLabSlotY] = module.moduleCode
                    randomTimetableConflicts[randomLabSlotX][randomLabSlotY] = module.moduleConflicts
                    module.labs = module.labs - 1
                    overlap = 1
                #print("Lab: ", randomTimetable[randomLabSlotX][randomLabSlotY])
        
    return randomTimetable, randomTimetableConflicts

def TimetableFitness(randomTimetable, randomTimetableConflicts):
    #Precedence Constraints
    concurrenceConstraintsViolations = 0
    conflictsIndex = 0

    for session in randomTimetable:

        #All slots
        slot0 = session[0]
        slot1 = session[1]
        slot2 = session[2]

        #Conflicts associated against each slot
        conflictingModulesS0 = randomTimetableConflicts[conflictsIndex][0]
        conflictingModulesS1 = randomTimetableConflicts[conflictsIndex][1]
        conflictingModulesS2 = randomTimetableConflicts[conflictsIndex][2]
        conflictsIndex = conflictsIndex + 1

        #Lecture 1 against lab 1 conflicts
        for conflictingModulesS0 in conflictingModulesS1:
            if slot0 == conflictingModulesS0:
                concurrenceConstraintsViolations = concurrenceConstraintsViolations + 1
                break
        
        #Lecture 1 against lab 2 conflicts
        for conflictingModulesS0 in conflictingModulesS2:
            if slot0 == conflictingModulesS0:
                concurrenceConstraintsViolations = concurrenceConstraintsViolations + 1
                break
        
        #Lab 1 against lab 2 conflicts
        for conflictingModuleS1 in conflictingModulesS2:
            if slot0 == conflictingModuleS1:
                concurrenceConstraintsViolations = concurrenceConstraintsViolations + 1
                break
    
    #Precedence Constraints
    precedenceConstraintsViolations = 0
    precedingLectures = []
    #lecturesIndex = 0

    for session in randomTimetable:
        precedingLectures.append(session[0]) # = session[0]
        #lecturesIndex = lecturesIndex + 1
        lab1 = session[1]
        lab2 = session[2]

        if lab1 not in precedingLectures:
            precedenceConstraintsViolations = precedenceConstraintsViolations + 1
        if lab2 not in precedingLectures:
            precedenceConstraintsViolations = precedenceConstraintsViolations + 1

    fitnessValue = concurrenceConstraintsViolations * precedenceConstraintsViolations
    return fitnessValue

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
allModules = LoadAllModules(allModules)
allModulesUse = copy.deepcopy(allModules)
randomTimetableConflictsUse = copy.deepcopy(randomTimetableConflicts)

randomTimetable = copy.deepcopy(blankTimetable)
randomTimetable, randomTimetableConflictsUse = TimetableRandomiser(randomTimetable, allModulesUse, randomTimetableConflictsUse)

#Displays random timetable
for session in randomTimetable:
    print("Slot: ", session[0], session[1], session[2])

violations = TimetableFitness(randomTimetable, randomTimetableConflictsUse)
print("VIOLATIONS: ")
print(violations)
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Hillclimber(timetable, violationsA, mutationSystem, iterations):
    print("Hillclimber():")

    lastBestTimetable = timetable
    lastBestViolations = violationsA

    #0 = SessionReplace
    if mutationSystem == 0:
        for i in range(iterations):
            SessionReplace(timetable)
    
    #1 = RuinAndRecreate
    if mutationSystem == 1:
        for i in range(iterations):
            timetable, bestViolations = RuinAndRecreate(timetable, violationsA)
        print("Hillclimber (Ruin & Recreate) Result: ", str(bestViolations))


def SessionReplace(timetableA):
    print("SessionReplace():")
    return timetableA

def RuinAndRecreate(randomTimetableA, violationsA):
    #print("RuinAndRecreate():")

    allModulesUse = copy.deepcopy(allModules)
    randomTimetableBConflictsUse = copy.deepcopy(randomTimetableConflicts)

    randomTimetableB = copy.deepcopy(blankTimetable)
    randomTimetableB, randomTimetableBConflictsUse = TimetableRandomiser(randomTimetableB, allModulesUse, randomTimetableBConflictsUse)

    violationsB = TimetableFitness(randomTimetableB, randomTimetableBConflictsUse)

    #OG VERSION:
    #timetableB = copy.deepcopy(blankTimetable)
    #allModulesUse = copy.deepcopy(allModules)
    #randomTimetableConflictsUse = copy.deepcopy(randomTimetableConflicts)
    
    #timetableB, randomTimetableConflictsUse = TimetableRandomiser(timetableB, allModulesUse, randomTimetableConflictsUse)

    #violationsA = TimetableFitness(timetableA)
    #violationsB = TimetableFitness(timetableB, randomTimetableConflictsUse)

    if violationsA < violationsB:
        return randomTimetableA, violationsA
    if violationsA > violationsB:
        return randomTimetableB, violationsB
    else:
        eitherTimetable = random.randint(0, 1)
        if eitherTimetable == 0:
            return randomTimetableA, violationsA
        if eitherTimetable == 1:
            return randomTimetableB, violationsB

Hillclimber(randomTimetable, violations, 1, 128)