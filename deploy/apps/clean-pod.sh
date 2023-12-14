#!/bin/bash

# 检查参数数量
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start-index> <end-index>"
    exit 1
fi

# 读取起始和终止索引
START_INDEX=$1
END_INDEX=$2

# 循环删除 Pod
for ((i=START_INDEX; i<=END_INDEX; i++))
do
    CPU_POD_NAME="stress-video-$i"
    echo "Deleting pod $DISK_POD_NAME"
    kubectl delete pod $CPU_POD_NAME
    DISK_POD_NAME="stress-disk-$i"
    echo "Deleting pod $CPU_POD_NAME"
    kubectl delete pod $DISK_POD_NAME
done

echo "Pod deletion completed."
