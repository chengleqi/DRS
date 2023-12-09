#include <iostream>
#include <cuda_runtime.h>
#include <cstring>
#include <chrono>
#include <thread>

// 模仿 https://github.com/wilicc/gpu-burn 的使用方法，但是不使用GPU计算，只占用显存
size_t parseMemoryArgument(const char* arg, size_t freeMem) {
    char* end;
    double memArg = strtod(arg, &end);

    if (*end == '%') {
        return static_cast<size_t>(freeMem * (memArg / 100.0));
    } else {
        return static_cast<size_t>(memArg * 1024 * 1024);
    }
}

int main(int argc, char **argv) {
    size_t totalMem, freeMem;
    cudaMemGetInfo(&freeMem, &totalMem);

    size_t memSize = 0;
    int duration = 0;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-m") == 0 && i + 1 < argc) {
            memSize = parseMemoryArgument(argv[++i], freeMem);
        } else if (strcmp(argv[i], "-t") == 0 && i + 1 < argc) {
            duration = atoi(argv[++i]);
        }
    }

    if (memSize <= 0 || memSize > freeMem) {
        std::cerr << "Invalid memory size." << std::endl;
        return 1;
    }

    char *memPtr;
    cudaMalloc((void**)&memPtr, memSize);
    std::cout << "Allocated " << memSize / (1024 * 1024) << " MB of GPU memory." << std::endl;

    std::cout << "Running for " << duration << " seconds..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(duration));

    cudaFree(memPtr);
    return 0;
}