# 第一阶段：构建阶段
FROM nvidia/cuda:12.0.1-cudnn8-devel-ubuntu22.04 AS builder

# 设置工作目录
WORKDIR /app

# 复制源代码到容器中
COPY mem_alloc.cu /app/

# 编译 CUDA 程序
RUN nvcc -o mem_alloc mem_alloc.cu

# 第二阶段：运行阶段
FROM nvidia/cuda:12.0.1-runtime-ubuntu22.04

# 复制编译好的程序到新的容器
COPY --from=builder /app/mem_alloc /usr/local/bin/mem_alloc

# 设置容器启动时运行的命令
ENTRYPOINT ["mem_alloc"]