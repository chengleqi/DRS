# useful nvidia links
# https://docs.nvidia.com/cuda/vGPU/index.html
# https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
# https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html
# https://docs.nvidia.com/datacenter/cloud-native/gpu-telemetry/latest/dcgm-exporter.html

# on gpu node
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=containerd --set-as-default
sudo systemctl restart containerd


# on master node
kubectl label node test-vgpu nvidia.com/device-plugin.config=4q
kubectl create ns gpu-operator
kubectl apply -f time-slicing-config.yaml -n gpu-operator

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia \
   && helm repo update
helm install --wait --generate-name \
     -n gpu-operator --create-namespace \
      nvidia/gpu-operator \
      --set driver.enabled=false \
      --set toolkit.enabled=false \
      --set devicePlugin.config.name=time-slicing-config