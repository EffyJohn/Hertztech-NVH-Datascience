from bayes_opt import BayesianOptimization
import matlab.engine
import csv

eng = matlab.engine.start_matlab()


def main():
    m1Pos = getPos('./Data/mount1.csv')
    m2Pos = getPos('./Data/mount2.csv')
    m3Pos = getPos('./Data/mount3.csv')

    pbounds = {
        'm1x': (m1Pos[0]-0.05, m1Pos[0]+0.05),
        'm1y': (m1Pos[1]-0.05, m1Pos[1]+0.05),
        'm1z': (m1Pos[2]-0.05, m1Pos[2]+0.05),
        'm2x': (m2Pos[0]-0.05, m2Pos[0]+0.05),
        'm2y': (m2Pos[1]-0.05, m2Pos[1]+0.05),
        'm2z': (m2Pos[2]-0.05, m2Pos[2]+0.05),
        'm3x': (m3Pos[0]-0.05, m3Pos[0]+0.05),
        'm3y': (m3Pos[1]-0.05, m3Pos[1]+0.05),
        'm3z': (m3Pos[2]-0.05, m3Pos[2]+0.05),
        'm1kx': (5*(10**4), 10**5),
        'm1ky': (5*(10**4), 10**5),
        'm1kz': (5*(10**4), 10**5),
        'm2kx': (5*(10**4), 10**5),
        'm2ky': (5*(10**4), 10**5),
        'm2kz': (5*(10**4), 10**5),
        'm3kx': (5*(10**4), 10**5),
        'm3ky': (5*(10**4), 10**5),
        'm3kz': (5*(10**4), 10**5),
    }

    print(eng.Objective())

    optimizer = BayesianOptimization(
        f=blackbox, pbounds=pbounds, random_state=1, verbose=1)

    optimizer.maximize(init_points=5, n_iter=100)
    print(optimizer.max)
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


def blackbox(m1x, m1y, m1z, m2x, m2y, m2z, m3x, m3y, m3z, m1kx, m1ky, m1kz, m2kx, m2ky, m2kz, m3kx, m3ky, m3kz):
    updateMount('./Data/mount1.csv', m1x, m1y, m1z, m1kx, m1ky, m1kz)
    updateMount('./Data/mount2.csv', m2x, m2y, m2z, m2kx, m2ky, m2kz)
    updateMount('./Data/mount3.csv', m3x, m3y, m3z, m3kx, m3ky, m3kz)
    return -eng.Objective()


if __name__ == "__main__":
    main()
