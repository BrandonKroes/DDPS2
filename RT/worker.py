import GPUtil


def getGPUMemory():
    print("test")
    gpus = GPUtil.getGPUs()

    memory = 0

    for gpu in gpus:
        if gpu.memoryTotal > memory:
            memory = gpu.memoryTotal
        print(gpu.id, gpu.name, gpu.memoryTotal)
    return memory


getGPUMemory()
