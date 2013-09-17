import csv
import os
import logging
from subprocess import call

from os.path import expanduser
home_dir = expanduser("~")

model_path = os.path.join(home_dir, 'gaussian_process_tmp/')

def LoadFromCSV(fileName):
    reader = csv.reader(open(fileName))
    _buffer = []
    for t, mu, sigma in reader:
        _buffer.append([t, mu, sigma])
    return _buffer


def SaveToCSV(fileName, data):
    writer = csv.writer(file(fileName, 'w'))
    for item in data:
        writer.writerow(item)


def Predict(arg1, arg2, arg3):
    logging("start gp predicting (before call matlab)")
    trainingDataFile = model_path + 'trainingData' + str(arg3) + '.in'
    SaveToCSV(trainingDataFile, arg1)

    testDataFile = model_path + 'testData' + str(arg3) + '.in'
    fout = open(testDataFile, 'w')
    for t in arg2:
        fout.write(str(t) + '\n')
    fout.close()

    outputFile = model_path + 'prediction' + str(arg3) + '.out'
    matlab_path = os.path.join(os.path.curdir(), 'matlab')
    #matlab_path = "/grad/users/kx19/citybeat_online/distributed_gp/matlab"
    os.chdir(matlab_path)

    shellComm = "matlab -r \'my_gp2 %s %s %s %s\'" % (trainingDataFile, testDataFile, outputFile, str(arg3))
    call([shellComm], shell=True)
    buffer = LoadFromCSV(outputFile)
    logging.warning(buffer)
    return buffer


def TestPredict():
    fileName = os.path.join(os.path.curdir, 'tmp/trainingData56.in')
    # fileName = '/grad/users/kx19/CityBeat/distributed_gp/tmp/trainingData56.in'
    reader = csv.reader(open(fileName), delimiter=',')
    buffer = []
    for t, pop in reader:
        buffer.append([t, pop])

    testFileName = os.path.join(os.path.curdir, 'tmp/trainingData56.in')
    #testFileName = '/grad/users/kx19/CityBeat/distributed_gp/tmp/testData56.in'
    reader = csv.reader(open(testFileName), delimiter=',')
    testData = []
    for t in reader:
        testData.append(t)

    print testData
    return


def main():
    TestPredict()


if __name__ == "__main__":
    main()
