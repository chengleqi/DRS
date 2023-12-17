#!/bin/bash

# 从命令行读取循环次数
COUNT=$1

# 基础文件名
CPU_FILENAME="cpu-job.yaml"
DISK_FILENAME="disk-job.yaml"
NET_FILENAME="network-job.yaml"
GPU_FILENAME="gpu-job.yaml"

# 循环创建并应用 Pod
for ((i=1; i<=COUNT; i++))
do
    # 替换占位符并应用新的 YAML
    sed "s/name: cpu/name: cpu-$i/; s/name: job/name: job-$i/" $CPU_FILENAME | kubectl apply -f -
    echo "Created cpu job $i"
    sleep 10

    sed "s/name: disk/name: disk-$i/; s/name: job/name: job-$i/" $DISK_FILENAME | kubectl apply -f -
    echo "Created disk job $i"
    sleep 10

    sed "s/name: network/name: network-$i/; s/name: job/name: job-$i/" $NET_FILENAME | kubectl apply -f -
    echo "Created network job $i"
    sleep 10

    sed "s/name: gpu/name: gpu-$i/; s/name: job/name: job-$i/" $GPU_FILENAME | kubectl apply -f -
    echo "Created gpu job $i"
    sleep 10
done

echo "All jobs created successfully."
