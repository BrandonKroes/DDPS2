import random


def divideWork():
    workers = [1, 2, 3, 4, 5]  # Workers/Nodes ....
    gpuWorkers = []
    gpuValues = []
    Frames = 100  # Frames....

    for i in range(0, len(workers) + 1):
        memory = workers[i].getGPUMemory()
        gpuWorkers.append(memory)
        if memory not in gpuValues:
            gpuValues.append(memory)

    gpuValues.sort()

    totalValue = 0

    for i in range(0, len(workers)):
        value = gpuValues.index(gpuWorkers[i])
        totalValue += value
        gpuWorkers[i] = value

    N = int(Frames / totalValue)
    rest = Frames - (N * totalValue)

    result = []

    for i in range(0, len(workers)):
        if gpuWorkers[i] == len(gpuValues) and rest != 0:
            gpuWorkers[i] = gpuWorkers[i] * N + rest
            rest = 0
        else:
            gpuWorkers[i] = gpuWorkers[i] * N

    return result
