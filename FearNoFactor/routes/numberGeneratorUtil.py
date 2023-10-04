import random

nextLevelDict = {
    "2": "4",
    "4": "1",
    "1": "3",
    "3": "5,6,8",
    "5,6,8": "2"
}

problemDict = {
    "2": set(
        [4, 6, 8, 9, 10, 14, 15, 21, 22, 25, 26, 27, 33, 34, 35, 38, 39, 46, 49, 51, 55, 57, 58, 62, 65, 69, 74, 77, 82,
         85, 86, 87, 91, 93, 94, 95, 106, 111, 115, 118, 119, 121, 122, 123, 125, 129, 133, 134, 141, 142, 143]),
    "4": set([24, 30, 40, 42, 54, 56, 64, 66, 70, 78, 88, 102, 104, 105, 110, 114, 128, 130, 135, 136, 138]),
    "1": set(
        [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
         107, 109, 113, 127, 131, 137, 139]),
    "3": set([12, 16, 18, 20, 28, 32, 44, 45, 50, 52, 63, 68, 75, 76, 81, 92, 98, 99, 116, 117, 124]),
    "5,6,8": set([36, 48, 60, 72, 80, 84, 90, 96, 100, 108, 112, 120, 126, 132, 140, 144]),
}


def getLevelFromProblem(problem):
    if problem in problemDict["2"]: return "2"
    if problem in problemDict["4"]: return "4"
    if problem in problemDict["1"]: return "1"
    if problem in problemDict["3"]: return "3"
    if problem in problemDict["5,6,8"]: return "5,6,8"
    return "2"


def getNextEasyProblem(target_num, solved_problems_string):
    current_level = getLevelFromProblem(target_num)
    solved_problems = set() if solved_problems_string == '' else set([int(ea) for ea in solved_problems_string.split(",")])
    solved_problems.add(target_num)
    if problemDict[current_level].issubset(solved_problems):
        # user has solved all problems in current level
        # remove all problems of current level
        solved_problems = solved_problems.difference(problemDict[current_level])

    next_level = nextLevelDict[current_level]
    next_problem = random.choice(list(problemDict[next_level].difference(solved_problems)))
    return next_problem, ','.join([str(ea) for ea in solved_problems])
