import GPy
import GPyOpt
from numpy.random import seed
import matplotlib
import matlab.engine
import csv

eng = matlab.engine.start_matlab()


def main():
    m1Pos = getPos('./Data/mount1.csv')
    m2Pos = getPos('./Data/mount2.csv')
    m3Pos = getPos('./Data/mount3.csv')

    bounds = [
        {'name': 'm1x', 'type': 'continuous',
            'domain': (m1Pos[0]-0.05, m1Pos[0]+0.05)},
        {'name': 'm1y', 'type': 'continuous',
            'domain': (m1Pos[1]-0.05, m1Pos[1]+0.05)},
        {'name': 'm1z', 'type': 'continuous',
            'domain': (m1Pos[2]-0.05, m1Pos[2]+0.05)},
        {'name': 'm2x', 'type': 'continuous',
            'domain': (m2Pos[0]-0.05, m1Pos[0]+0.05)},
        {'name': 'm2y', 'type': 'continuous',
            'domain': (m2Pos[1]-0.05, m1Pos[1]+0.05)},
        {'name': 'm2z', 'type': 'continuous',
            'domain': (m2Pos[2]-0.05, m1Pos[2]+0.05)},
        {'name': 'm3x', 'type': 'continuous',
            'domain': (m3Pos[0]-0.05, m1Pos[0]+0.05)},
        {'name': 'm3y', 'type': 'continuous',
            'domain': (m3Pos[1]-0.05, m1Pos[1]+0.05)},
        {'name': 'm3z', 'type': 'continuous',
            'domain': (m3Pos[2]-0.05, m1Pos[2]+0.05)},
        {'name': 'm1kx', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm1ky', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm1kz', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm2kx', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm2ky', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm2kz', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm3kx', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm3ky', 'type': 'continuous', 'domain': (5*(10**4), 10**8)},
        {'name': 'm3kz', 'type': 'continuous', 'domain': (5*(10**4), 10**8)}]

    print(eng.Objective())

    solver = GPyOpt.methods.BayesianOptimization(
        blackbox, domain=bounds, model_type='GP', acquisition_type='EI', normalize_Y=False, acquisition_weight=2)
    solver.run_optimization(10)
    print(solver.fx_opt)
    return


def getPos(filename):
    mPos = []
    with open(filename, newline='') as mount_file:
        mount_reader = csv.reader(mount_file, delimiter=',', quotechar='|')
        flag = 0
        for row in mount_reader:
            if flag:
                mPos.append(float(row[6]))
            else:
                flag = 1

    return mPos


def updateMount(filename, mx, my, mz, mkx, mky, mkz):
    rows = []
    pos = [mx, my, mz]
    stiffness = [mkx, mky, mkz]

    with open(filename, newline='') as mount_file:
        mount_reader = csv.reader(mount_file, delimiter=',', quotechar='|')
        for row in mount_reader:
            rows.append(row)

    for i in range(4):
        if i != 0:
            (rows[i])[6] = str(pos[i-1])
            (rows[i])[1] = str(stiffness[i-1])

    with open(filename, 'w', newline='') as mount_file:
        mount_writer = csv.writer(
            mount_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for row in rows:
            mount_writer.writerow(row)
    return


def pseudoBlackBox(evalList):
    for row in evalList:
        blackbox(row)


def blackbox(argumentList):
    updateMount('./Data/mount1.csv', argumentList[1], argumentList[2],
                argumentList[3], argumentList[10], argumentList[11], argumentList[12])
    updateMount('./Data/mount2.csv', argumentList[4], argumentList[5],
                argumentList[6], argumentList[13], argumentList[14], argumentList[15])
    updateMount('./Data/mount3.csv', argumentList[7], argumentList[8],
                argumentList[9], argumentList[16], argumentList[17], argumentList[18])
    return -eng.Objective()


if __name__ == "__main__":
    main()
