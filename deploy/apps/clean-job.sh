#!/bin/bash

# 从命令行读取循环次数
COUNT=$1

# 为每种类型的 Job 定义基本名称
CPU_JOB_NAME="cpu-"
DISK_JOB_NAME="disk-"
NET_JOB_NAME="network-"
GPU_JOB_NAME="gpu-"

# 循环删除 Jobs
for ((i=1; i<=COUNT; i++))
do
    # 删除每个 CPU Job
    kubectl delete jobs.batch.volcano.sh ${CPU_JOB_NAME}$i
    echo "Deleted ${CPU_JOB_NAME}$i job"

    # 删除每个 Disk Job
    kubectl delete jobs.batch.volcano.sh ${DISK_JOB_NAME}$i
    echo "Deleted ${DISK_JOB_NAME}$i job"

    # 删除每个 Network Job
    kubectl delete jobs.batch.volcano.sh ${NET_JOB_NAME}$i
    echo "Deleted ${NET_JOB_NAME}$i job"

    # 删除每个 GPU Job
    kubectl delete jobs.batch.volcano.sh ${GPU_JOB_NAME}$i
    echo "Deleted ${GPU_JOB_NAME}$i job"
done

echo "All jobs deleted successfully."
