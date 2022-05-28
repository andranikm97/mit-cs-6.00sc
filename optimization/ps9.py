# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#


def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects = {}
    inputFile = open(filename)
    for line in inputFile:
        line = line.strip('\n')
        name, value, work = line.split(',')
        subjects[name] = (int(value), int(work))

    return subjects


def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0, 0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = list(subjects.keys())
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) + '\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print(res)


#
# Problem 2: Subject Selection By Greedy Optimization
#


def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[0] > subInfo2[0]


def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]


def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return (subInfo1[0]/subInfo1[1]) > (subInfo2[0]/subInfo2[1])


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj[1]

        def __lt__(self, other):
            return mycmp(self.obj, other.obj)

        def __gt__(self, other):
            return mycmp(self.obj, other.obj)

        def __eq__(self, other):
            return mycmp(self.obj, other.obj)

        def __le__(self, other):
            return mycmp(self.obj, other.obj)

        def __ge__(self, other):
            return mycmp(self.obj, other.obj)

        def __ne__(self, other):
            return mycmp(self.obj, other.obj)
    return K


def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    subjectsCopySorted = sorted(subjects.items(),
                                key=cmp_to_key(comparator))

    totalWork = 0
    chosen = {}
    for code, (value, work) in subjectsCopySorted:
        if totalWork + work <= maxWork:
            chosen[code] = subjects[code]
            totalWork += work

    return chosen

#
# Problem 3: Subject Selection By Brute Force
#


def dToB(n, numDigits):
    """requires: n is a natural number less than 2**numDigits
      returns a binary string of length numDigits representing the
              the decimal number n."""
    assert type(n) == int and type(numDigits) == int and\
        n >= 0 and n < 2**numDigits
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr


def genPset(subjects):
    """Generate a list of lists representing the power set of Items"""
    numSubsets = 2**len(subjects)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(subjects)))
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(subjects[j])
        pset.append(elem)
    return pset


def dict2TupleList(d):
    t = []
    for key in d:
        t.append((key, d[key]))
    return t


def tupleList2dict(t):
    d = {}
    for code, data in t:
        d[code] = data

    return d


def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    tupledSubjects = dict2TupleList(subjects)
    pSet = genPset(tupledSubjects)
    bestVal = 0.0
    bestSet = None
    for subjectSet in pSet:
        totalVal = 0
        totalWork = 0
        for code, (val, work) in subjectSet:
            totalVal += val
            totalWork += work

        if totalWork <= maxWork and totalVal > bestVal:
            bestVal = totalVal
            bestSet = tupleList2dict(subjectSet)

    return bestSet
