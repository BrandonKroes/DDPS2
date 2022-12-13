import random


def divideWork():
    workers = [1, 2, 3, 4, 5]  # Workers/Nodes ....
    gpuWorkers = []
    gpuValues = []
    Frames = 100  # Frames....

    for i in range(0, len(workers)):
        # memory = workers[i].getGPUMemory()
        memory = random.randint(0, 9)
        gpuWorkers.append(memory)
        if memory not in gpuValues:
            gpuValues.append(memory)

    print(gpuWorkers)
    print(gpuValues)

    gpuValues.sort()

    print(gpuValues)

    totalValue = 0

    for i in range(0, len(workers)):
        value = gpuValues.index(gpuWorkers[i]) + 1
        totalValue += value
        gpuWorkers[i] = value

    print(gpuWorkers)

    N = int(Frames / totalValue)
    rest = Frames - (N * totalValue)

    print('TotalValue =', totalValue)
    print("N =", N)
    print("rest=", rest)

    result = []

    for i in range(0, len(workers)):
        if (gpuWorkers[i] == len(gpuValues)) and (rest != 0):
            gpuWorkers[i] = gpuWorkers[i] * N + rest
            rest = 0
            print('!')
        else:
            gpuWorkers[i] = gpuWorkers[i] * N

    print(gpuWorkers)
    return gpuWorkers


divideWork()
