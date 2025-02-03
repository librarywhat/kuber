import os.path
import subprocess
import time

while True:
    try:
        ip = subprocess.check_output("kubectl get svc -A | awk '/ingress-nginx-controller/ {print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'", shell=True, text=True)
    except subprocess.CalledProcessError as e:
        time.sleep(5)
        continue
    break
with open("/opt/containerd/lib/manifests/metallb-config.yaml",'w',encoding='utf-8') as f:
    f.write(f"""apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: public-ip-pool
  namespace: default
spec:
  addresses:
  - {ip}/32
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: public-ip-advertisement
  namespace: default
spec:
  ipAddressPools:
  - public-ip-pool""")

while True:
    try:
        ip = subprocess.check_output("kubectl get svc -A | awk '/ingress-nginx-controller/ {print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'", shell=True, text=True)
        time.sleep(5)
        continue
    except subprocess.CalledProcessError as e:
        os.system("kubectl apply -f /opt/containerd/lib/manifests/metallb-config.yaml")
        break