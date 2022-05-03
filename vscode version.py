from operator import itruediv, truediv
import random
import copy
import matplotlib.pyplot as plt

#Module class for holding each type of module with their corresponding attributes
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
#class Session:
#    lecture = "Empty"
#    lab1 = "Empty"
#    lab2 = "Empty"
#    slots = [lecture, lab1, lab2]

#Opens module text file
modules = open("Modules.txt")
allModules = []
lectures = 1

#Extracts raw module information & converts it into Module objects
def LoadAllModules(allModules):
    arrayIndex = 0
    for moduleAttributes in modules:
        moduleAttributesFormatted = moduleAttributes.split('|')

        #Module session information
        moduleCode = moduleAttributesFormatted[0]
        lecturerName = moduleAttributesFormatted[1]
        sessionsUnformatted = moduleAttributesFormatted[2]
        labs = int(sessionsUnformatted)
        
        #Module conflict information
        conflictingModules = moduleAttributesFormatted[3]
        conflictingModulesFormatted = conflictingModules.split(',')
        
        #Information assigned to Module object
        allModules.append(Module(moduleCode, lecturerName, conflictingModulesFormatted, labs))
        arrayIndex = arrayIndex + 1
    return allModules

#Blank timetable for filling later
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

#Array of associatedly timetabled module conflicts
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

#Creates a randomly generated timetable from a blank timetable
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
    
    return randomTimetable, randomTimetableConflicts

#Determines correctness of timetable in terms of its practicality
def TimetableFitness(randomTimetable, randomTimetableConflicts):
    #Concurrence constraints
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
    
    #Precedence constraints
    precedenceConstraintsViolations = 0
    precedingLectures = []

    for session in randomTimetable:
        #Adds the currently indexed sessions to array of historically assigned
        precedingLectures.append(session[0])
        lab1 = session[1]
        lab2 = session[2]

        #Checks if sessions have already been assigned
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

def Hillclimber(timetable, violationsA, randomTimetableAConflicts, mutationSystem, iterations):
    print("Hillclimber():")

    lastBestTimetable = timetable
    lastBestTimetableConflicts = randomTimetableAConflicts
    lastBestViolations = violationsA
    allBestViolations = [None] * iterations

    #0 = SessionReplace
    if mutationSystem == 0:
        for i in range(iterations):
            timetable, randomTimetableAConflicts, violationsA = SessionReplace(lastBestTimetable, lastBestTimetableConflicts, lastBestViolations)
            allBestViolations[i] = violationsA
            lastBestTimetable = timetable
            lastBestTimetableConflicts = randomTimetableAConflicts
            lastBestViolations = violationsA
        print("Hillclimber (Session Replace) Result: ", str(violationsA))
        return lastBestTimetable, lastBestViolations

    #1 = RuinAndRecreate
    if mutationSystem == 1:
        for i in range(iterations):
            timetable, violationsA = RuinAndRecreate(lastBestTimetable, lastBestViolations)
            allBestViolations[i] = violationsA
            lastBestTimetable = timetable
            lastBestViolations = violationsA
        print("Hillclimber (Ruin & Recreate) Result: ", str(violationsA))
        return lastBestTimetable, lastBestViolations

def SessionReplace(randomTimetableA, randomTimetableAConflicts, violationsA):
    randomTimetableB = copy.deepcopy(randomTimetableA)
    randomTimetableBConflicts = copy.deepcopy(randomTimetableAConflicts)

    #Type of slot to exchange
    slotType = random.randint(0, 2)

    if slotType == 0: #Slot 0: lecture slot
        slotA = random.randint(0, 19)
        slotB = slotA
        while slotB == slotA:
          slotB = random.randint(0, 19) 
        
        #Gets copies of session slots
        slotToExchangeToA = randomTimetableB[slotB][slotType]
        slotToExchangeToB = randomTimetableB[slotA][slotType]

        #Exchanges session slots with the copies
        randomTimetableB[slotA][slotType] = slotToExchangeToA
        randomTimetableB[slotB][slotType] = slotToExchangeToB
    elif slotType > 0: #Slot 1 or 2: lab1 or lab2 slot
        slotA = random.randint(0, 19)
        slotB = slotA
        while slotB == slotA:
          slotB = random.randint(0, 19)
        
        #Whether lab 1 or lab 2 slots
        slotAType = random.randint(1, 2)
        slotBType = random.randint(1, 2)
        
        #Gets copies of session slots
        slotToExchangeToA = randomTimetableB[slotB][slotBType]
        slotToExchangeToB = randomTimetableB[slotA][slotAType]
        slotConflictsToExchangeToA = randomTimetableBConflicts[slotB][slotBType]
        slotConflictsToExchangeToB = randomTimetableBConflicts[slotA][slotAType]

        #Exchanges session slots with the copies
        randomTimetableB[slotA][slotAType] = slotToExchangeToA
        randomTimetableB[slotB][slotBType] = slotToExchangeToB
        randomTimetableBConflicts[slotA][slotAType] = slotConflictsToExchangeToA
        randomTimetableBConflicts[slotB][slotBType] = slotConflictsToExchangeToB

    violationsB = TimetableFitness(randomTimetableB, randomTimetableBConflicts)

    if violationsA < violationsB:
        return randomTimetableA, randomTimetableAConflicts, violationsA
    if violationsA > violationsB:
        return randomTimetableB, randomTimetableBConflicts, violationsB
    else:
        eitherTimetable = random.randint(0, 1)
        if eitherTimetable == 0:
            return randomTimetableA, randomTimetableAConflicts, violationsA
        if eitherTimetable == 1:
            return randomTimetableB, randomTimetableBConflicts, violationsB

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

#timetableForSessionReplace = copy.deepcopy(randomTimetable)
#timetableConflictsForSessionReplace = copy.deepcopy(randomTimetableConflictsUse)
#timetableForRuinAndRecreate = copy.deepcopy(randomTimetable)
#timetableConflictsForRuinAndRecreate = copy.deepcopy(randomTimetableConflictsUse)

allBestSRViolationLists = [None] * 30
allBestRARViolationLists = [None] * 30

for i in range(30):
    timetableForSessionReplace = copy.deepcopy(randomTimetable)
    timetableConflictsForSessionReplace = copy.deepcopy(randomTimetableConflictsUse)
    
    bestSRTimetable, bestSRViolations = Hillclimber(timetableForSessionReplace, violations, timetableConflictsForSessionReplace, 0, 500)
    allBestSRViolationLists[i] = bestSRViolations
for i in range(30):
    timetableForRuinAndRecreate = copy.deepcopy(randomTimetable)
    timetableConflictsForRuinAndRecreate = copy.deepcopy(randomTimetableConflictsUse)

    bestRARTimetable, bestRARViolations = Hillclimber(timetableForRuinAndRecreate, violations, timetableConflictsForRuinAndRecreate, 1, 500)
    allBestRARViolationLists[i] = bestRARViolations

averageSRFitness = sum(allBestSRViolationLists) / len(allBestSRViolationLists)
averageRARFitness = sum(allBestRARViolationLists) / len(allBestRARViolationLists)
maxSRFitnessAccuracy = min(allBestSRViolationLists)
minSRFitnessAccuracy = max(allBestSRViolationLists)
maxRARFitnessAccuracy = min(allBestRARViolationLists)
minRARFitnessAccuracy = max(allBestRARViolationLists)

print(averageSRFitness, maxSRFitnessAccuracy, minSRFitnessAccuracy, averageRARFitness, maxRARFitnessAccuracy, minSRFitnessAccuracy)

allFitnessScores = [allBestSRViolationLists, allBestRARViolationLists]
allFitnessScoresBoxPlot = plt.boxplot(allFitnessScores)