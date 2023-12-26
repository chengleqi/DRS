# 五个节点，master节点去掉污点，所有节点都有一个除了系统盘以外的数据盘用来部署osd

# https://rook.io/docs/rook/latest-release/Getting-Started/quickstart/
git clone --single-branch --branch v1.13.1 https://github.com/rook/rook.git
cd rook/deploy/examples
kubectl create -f crds.yaml -f common.yaml -f operator.yaml

kubectl create -f cluster.yaml

# CephFilesystem 是RWX的，所以部署CephFilesystem

# apply cephfs
kubectl create -f filesystem.yaml
# apply storageclass
kubectl create -f deploy/examples/csi/cephfs/storageclass.yaml
