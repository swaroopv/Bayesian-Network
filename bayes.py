__author__ = 'swvenu'
import logging
import sys
import operator
import itertools


class Disease:
    def __init__(self, inputList):
        self.name = inputList[0]
        self.noOfSymptoms = int(inputList[1])
        self.probability = float(inputList[2])
        self.symptoms = []

    def addSymptom(self, symptom):
        self.symptoms.append(symptom)


class Symptoms:
    def __init__(self, name, pwd, pwod):
        self.name = name
        self.probabilityWithDisease = float(pwd)
        self.probabilityWithoutDisease = float(pwod)


def testsIncreaseOrDecreaseProbabilityOfDisease(findings):
    """
    This function takes patients findings and returns individual tests that would give biggest
    increase and decrease in probability of disease
    :param findings: A string containing patients symptom record
    :return: result (dict) - individual tests with their result which would give biggest increase and decrease in probability of disease

    """
    result = {}
    for idx, finding in enumerate(findings):
        undefinedAsTrue = {}
        disease = diseasesArray[idx]
        result[disease.name] = []
        finding = eval(finding)
        noOfUndefined = finding.count('U')
        if noOfUndefined == 0:
            result[disease.name].append('none')
            result[disease.name].append('N')
            result[disease.name].append('none')
            result[disease.name].append('N')
            continue

        for i in range(0, noOfUndefined):
            tempList = finding[:]
            # replace i'th 'U' by 'T'
            index = replaceItemInList(tempList, i, 'U', 'T')
            symptom = disease.symptoms[index].name
            prob = calculateProbabilityOfDisease(tempList, idx);
            undefinedAsTrue[symptom] = prob.itervalues().next()
        # determine which gives largest increase
        undefinedAsTrueMaxkey = max(undefinedAsTrue.iteritems(), key=operator.itemgetter(1))[0]
        undefinedAsTrueMinkey = min(undefinedAsTrue.iteritems(), key=operator.itemgetter(1))[0]
        undefinedAsFalse = {}
        for j in range(0, noOfUndefined):
            tempList = finding[:]
            # replace j'th 'U' by 'F'
            index = replaceItemInList(tempList, j, 'U', 'F')
            symptom = disease.symptoms[index].name
            prob = calculateProbabilityOfDisease(tempList, idx);
            undefinedAsFalse[symptom] = prob.itervalues().next()
        # determine which gives largest decrease
        undefinedAsFalseMaxkey = max(undefinedAsFalse.iteritems(), key=operator.itemgetter(1))[0]
        undefinedAsFalseMinkey = min(undefinedAsFalse.iteritems(), key=operator.itemgetter(1))[0]
        if undefinedAsTrue[undefinedAsTrueMaxkey] > undefinedAsFalse[undefinedAsFalseMaxkey]:
            maxKey = undefinedAsTrueMaxkey
            maxKeyValue = 'T'
        else:
            maxKey = undefinedAsFalseMaxkey
            maxKeyValue = 'F'
        if undefinedAsTrue[undefinedAsTrueMinkey] < undefinedAsFalse[undefinedAsFalseMinkey]:
            minKey = undefinedAsTrueMinkey
            minKeyValue = 'T'
        else:
            minKey = undefinedAsFalseMinkey
            minKeyValue = 'F'
        result[disease.name].append(maxKey)
        result[disease.name].append(maxKeyValue)
        result[disease.name].append(minKey)
        result[disease.name].append(minKeyValue)
    log.debug(result)
    return result


def replaceItemInList(List, nthOccurence, replaceThis, withThis):
    """
     replace nth occurrence of a item in the list
    :param List:
    :param nthOccurence:
    :param replaceThis:
    :param withThis:
    :return:
    """
    count = 0
    for idx, item in enumerate(List):
        if item == replaceThis:
            if count == nthOccurence:
                List[idx] = withThis
                return idx
            count += 1


def calculateMinMaxProbailityOfDisease(findings):
    """
    This function takes patients findings and returns max and min probability of him getting the disease for some combination
    of result for his undefined symptoms
    :param findings: A string containing patients symptom record
    :return: result (dict)

    """
    result = {}
    for idx, finding in enumerate(findings):
        temp = []
        finding = eval(finding)
        noOfUndefined = finding.count('U')
        truthTable = list(itertools.product(['F', 'T'], repeat=noOfUndefined))
        for row in truthTable:
            tempList = finding[:]
            for value in row:
                replaceItemInList(tempList, 0, 'U', value)
            temp.append(calculateProbabilityOfDisease(tempList, idx).itervalues().next())
        result[diseasesArray[idx].name] = ["%.4f" % min(temp), "%.4f" % max(temp)]

    log.debug(result)
    return result


def calculateProbabilityOfAllDisease(findings):
    """
    This function takes all patients findings and returns probability of him getting each disease
    :param findings: A string containing patients symptom record
    :return: result (dict)

    """
    result = {}
    for idx, finding in enumerate(findings):
        finding = eval(finding)
        result.update(calculateProbabilityOfDisease(finding, idx))
    # format result
    for key, value in result.iteritems():
        result[key] = "%.4f" % value
    log.debug(result)
    return result


def calculateProbabilityOfDisease(finding, diseaseNo):
    '''
    Calculates probability of getting a disease given patient's finding
    :param finding: A list containing patients symptom record
    :param diseaseNo: The disease no in diseaseArray  for which we are finding probability
    :return:
    '''
    result = {}
    expression = [diseasesArray[diseaseNo], '|']
    for idy, item in enumerate(finding):
        if item == 'T':
            expression.append(diseasesArray[diseaseNo].symptoms[idy])
        elif item == 'F':
            expression.append(['not', diseasesArray[diseaseNo].symptoms[idy]])
    result[diseasesArray[diseaseNo].name] = resolveProbabilityExpression(expression)
    return result


def resolveProbabilityExpression(expression):
    '''
    Given a probability expression, resolves  it
    :param expression:
    :return: probability - float
    '''
    firstExp = 1
    secondExp = 1
    for idx, item in enumerate(expression):
        negation = False
        if type(item) is list:
            negation = True
            item = item[1]
        if item.__class__.__name__ == "Disease":
            firstExp *= item.probability
            secondExp *= 1 - item.probability
        elif item.__class__.__name__ == "Symptoms":
            firstExp *= (1 - item.probabilityWithDisease) if negation else item.probabilityWithDisease
            secondExp *= (1 - item.probabilityWithoutDisease) if negation else item.probabilityWithoutDisease
    return firstExp / (firstExp + secondExp)


logging.basicConfig(level=logging.DEBUG)
log = logging
diseasesArray = []
if len(sys.argv) > 2 and sys.argv[1] == "-i":
    log.debug(sys.argv)
    try:
        # read file
        inputFile = open(sys.argv[2], 'r')
        outputFile = open(inputFile.name[0:-4] + "_inference.txt", 'w')
        lines = inputFile.read().split('\n')
        line = lines[0].split()
        numberOfDisease = int(line[0])
        numberOfPatients = int(line[1])

        nextLineNumber = 0
        for i in range(0, numberOfDisease):
            nextLineNumber = i * 4 + 1
            disease = Disease(lines[nextLineNumber].split())
            symptomsArray = eval(lines[nextLineNumber + 1])
            pwdArray = eval(lines[nextLineNumber + 2])
            pwodArray = eval(lines[nextLineNumber + 3])
            for j in range(0, len(symptomsArray)):
                symptom = Symptoms(symptomsArray[j], pwdArray[j], pwodArray[j])
                disease.addSymptom(symptom)
            diseasesArray.append(disease)

        nextLineNumber = 4 * numberOfDisease + 1
        for i in range(0, numberOfPatients):
            recordBegin = nextLineNumber
            recordEnd = nextLineNumber + numberOfDisease
            patientFindings = lines[recordBegin:recordEnd]
            log.debug("Patient-" + str(i + 1) + ":")
            outputFile.write("Patient-" + str(i + 1) + ":\n")
            outputFile.write("%s\n" % calculateProbabilityOfAllDisease(patientFindings))
            outputFile.write("%s\n" % calculateMinMaxProbailityOfDisease(patientFindings))
            outputFile.write("%s\n" % testsIncreaseOrDecreaseProbabilityOfDisease(patientFindings))
            nextLineNumber += numberOfDisease
        inputFile.close()
    except IOError as ex:
        log.error(ex.strerror)
else:
    log.error("Please enter input in the following format: python bayes.py -i inputfilename")
