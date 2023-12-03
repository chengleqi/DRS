#!/bin/bash

# 从命令行读取循环次数
COUNT=$1

# 基础文件名
CPU_FILENAME="my-cpu.yaml"
DISK_FILENAME="my-disk.yaml"

# 循环创建并应用 Pod
for ((i=1; i<=COUNT; i++))
do
    # 替换占位符并应用新的 YAML
    sed "s/stress-video/stress-video-$i/" $CPU_FILENAME | kubectl apply -f -
    echo "Created pod stress-video-$i"
    sleep 20
    sed "s/stress-disk/stress-disk-$i/" $DISK_FILENAME | kubectl apply -f -
    sleep 20
done

echo "All pods created successfully."
