# Library for simple Bayesian optimization
from bayes_opt import BayesianOptimization

# Core library object that runs the MATLAB engine !REQUIRES PYTHON 3.7
try:
    import matlab.engine
except:
    print("Please use python 3.7")
    print("MATLAB engine is unsupported for other versions.")
    exit()

import csv

# To clear screen
from os import system, name

# Initialize MATLAB engine object.
eng = matlab.engine.start_matlab()


def main():
    # Retrieve position data of each mount to set initial bounds for optimizer.
    try:
        m1Pos = getPos('./Data/mount1.csv')
        m2Pos = getPos('./Data/mount2.csv')
        m3Pos = getPos('./Data/mount3.csv')
        clear()
        print("Position Data Retreived.")
    except:
        print("Error while accessing mount position data! Please ensure all three mount files exist.")
        return

    # Set bounds for both the positions and stiffnesses for each mount.
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

    print("Bounds have been set.")
    print()

    # Print the starting value of phi, based on the initial set up of position and stifffness, to compare with final results.
    try:
        print("Objective function value at start state is",
              round(float(eng.Objective()), 2))
        print()
    except:
        print("Error while trying to run Objective.m")
        print("Ensure that python version being used is 3.7")
        print("MATLAB engine does not support other versions.")
        return

    input("Press enter to proceed with optimization")
    clear()

    # Gets the user requirement for verbosity of the optimizer.
    while True:
        try:
            verbosity = int(
                input("Enter 0 to suppress output, 1 for all minimas, 2 for all output: "))
            clear()
            if verbosity == 0 or verbosity == 1 or verbosity == 2:
                break
            else:
                print(
                    "Invalid input, please enter a value from the set {0, 1, 2}")
        except:
            print("Invalid input, please enter a value from the set {0, 1, 2}")

    # Gets the user required depth of optimization iterations
    while True:
        try:
            depth = int(input("Enter required iteration depth: "))
            clear()

            if depth <= 0:
                print("Please enter an integer greater than 0")
            else:
                break
        except:
            print("Please enter an integer greater than 0")

    # Create optimizer, passing in "blackbox"
    optimizer = BayesianOptimization(
        f=blackbox, pbounds=pbounds, random_state=1, verbose=verbosity)

    # Start maximizing. The library only has a maximize function, so we simply maximize the negative of the function we want to minimize.
    optimizer.maximize(init_points=5, n_iter=depth)

    input("Press enter to output minimized value produced by optimizer")
    clear()

    outputMin(optimizer.max)
    return


def clear():
    # UDF for clearing screen, to make printed output easier to read.

    if name == 'nt':        # For Windows
        _ = system('cls')
    else:                   # For all others (posix)
        _ = system('clear')


def getPos(filename):
    # Function opens the file provided, and retrieves the mount positions.
    # Input validation has not been implemented, hence the csv files must follow the given standard pattern.

    mPos = []

    with open(filename, newline='') as mount_file:
        mount_reader = csv.reader(mount_file, delimiter=',', quotechar='|')
        flag = 0
        for row in mount_reader:
            if flag:
                # Column 6 contains the x, y, z coordinates of mount, in that order.
                mPos.append(float(row[6]))
            else:
                flag = 1  # Skips the first row which contains table header

    return mPos


def updateMount(filename, mx, my, mz, mkx, mky, mkz):
    #   After each iteration of the optimizer, the optimizer picks a new value for the 18 input variables, to sample the function.
    #   Since the MATLAB function is being called by the optimizer indirectly, it is much easier to simply directly update the csv files.
    #   The only way therefore, that this python code can control the inputs of the Objective.m function, is through csv edits.
    #   This function's purpose is to edit each mount file one at a time.

    # Helper Variables
    rows = []
    pos = [mx, my, mz]
    stiffness = [mkx, mky, mkz]

    # Opens mount file, reads data, stores it into rows. Opened in read mode.
    with open(filename, newline='') as mount_file:
        mount_reader = csv.reader(mount_file, delimiter=',', quotechar='|')
        for row in mount_reader:
            rows.append(row)

    # Updates the data in the rows list, based on inputs recevied from optimizer.
    for i in range(4):
        if i != 0:
            (rows[i])[6] = str(pos[i-1])
            (rows[i])[1] = str(stiffness[i-1])

    # Opens mount file in write mode, and writes in the new data stored in rows.
    with open(filename, 'w', newline='') as mount_file:
        mount_writer = csv.writer(
            mount_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for row in rows:
            mount_writer.writerow(row)
    return


def blackbox(m1x, m1y, m1z, m2x, m2y, m2z, m3x, m3y, m3z, m1kx, m1ky, m1kz, m2kx, m2ky, m2kz, m3kx, m3ky, m3kz):
    # This is a wrapper function. This function exists to prepare the CSV files for the next iteration of calling the MATLAB function.
    # First, the mount files are all three updated based on the instruction from the optimizer.
    # Then, the MATLAB function is called, and the NEGATIVE of its response is returned.
    # This is because the optimizer maximizes, and we want minimization.

    updateMount('./Data/mount1.csv', m1x, m1y, m1z, m1kx, m1ky, m1kz)
    updateMount('./Data/mount2.csv', m2x, m2y, m2z, m2kx, m2ky, m2kz)
    updateMount('./Data/mount3.csv', m3x, m3y, m3z, m3kx, m3ky, m3kz)
    return -eng.Objective()


def outputMin(output):
    # Cleans up output and spits it.

    print("Final value of Objective function:",
          round(-float(output['target']), 2))

    mountData = output['params']
    print()

    print("Mount 1:")
    print("Axis\t Position\t Stiffness")
    print("x\t ", round(float(mountData['m1x']), 4), "\t ", round(
        float(mountData['m1kx']), 2))
    print("y\t ", round(float(mountData['m1y']), 4), "\t ", round(
        float(mountData['m1ky']), 2))
    print("z\t ", round(float(mountData['m1z']), 4), "\t ", round(
        float(mountData['m1kz']), 2))
    print()

    print("Mount 2:")
    print("Axis\t Position\t Stiffness")
    print("x\t ", round(float(mountData['m2x']), 4), "\t ", round(
        float(mountData['m2kx']), 2))
    print("y\t ", round(float(mountData['m2y']), 4), "\t ", round(
        float(mountData['m2ky']), 2))
    print("z\t ", round(float(mountData['m2z']), 4), "\t ", round(
        float(mountData['m2kz']), 2))
    print()

    print("Mount 3:")
    print("Axis\t Position\t Stiffness")
    print("x\t ", round(float(mountData['m3x']), 4), "\t ", round(
        float(mountData['m3kx']), 2))
    print("y\t ", round(float(mountData['m3y']), 4), "\t ", round(
        float(mountData['m3ky']), 2))
    print("z\t ", round(float(mountData['m3z']), 4), "\t ", round(
        float(mountData['m3kz']), 2))
    print()
    print()


if __name__ == "__main__":
    clear()
    main()
