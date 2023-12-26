#!/bin/bash
# https://juicefs.com/docs/zh/csi/getting_started

# on Storage Cluster
# install minio
docker run -d --name minio \
    -p 9000:9000 \
    -p 9900:9900 \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    -v $PWD/minio-data:/data \
    --restart unless-stopped \
    minio/minio server /data --console-address ":9900"

# install redis
docker run -d --name redis -p 6379:6379 redis --requirepass "mypassword"

# create filesystem
juicefs format --storage minio \
    --bucket http://127.0.0.1:9000/myjfs \
    --access-key minioadmin \
    --secret-key minioadmin  \
    "redis://:mypassword@127.0.0.1:6379/1" \
    myjfs

# mount on local manchine
juicefs mount -d "redis://:mypassword@127.0.0.1:6379/1" /mnt/jfs


# on Consumer Cluster
# Deploy JuiceFS CSI Driver
kubectl apply -f https://raw.githubusercontent.com/juicedata/juicefs-csi-driver/master/deploy/k8s.yaml

# check csi driver
kubectl -n kube-system get pods -l app.kubernetes.io/name=juicefs-csi-driver

# apply secret and storageclass
kubectl apply -f secret.yaml -f storageclass.yaml
