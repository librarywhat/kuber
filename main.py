import os.path
import subprocess
import time

def log(*message):
    with open('/opt/logs.csv','a',encoding='utf-8') as f:
        f.write(f'{message}\n')

counter=0

file_text="""apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: public-ip-pool
  namespace: default
spec:
  addresses:
    - {}/32
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: public-ip-advertisement
  namespace: default
spec:
  ipAddressPools:
    - public-ip-pool



"""

while True:
    try:
        ip = subprocess.check_output("kubectl get svc -A | awk '/ingress-nginx-controller/ {print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'", shell=True, text=True)
        log(f"line:13 ip: {ip}")
        print(f"ip:{ip}ip")
        ip = ip.replace('\n',"").strip()

        with open("/opt/containerd/lib/manifests/metallb-config.yaml", 'w', encoding='utf-8') as f:
            f.write(file_text.format(ip))

        log(f"line:34 file done: {ip}")


        break
    except Exception as e:
        log(f"line:39, retry:{counter} error: {e}")
        counter+=1
        time.sleep(5)
        continue

subprocess.check_output("curl -o helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3",shell=True,text=True)
subprocess.check_output("chmod +x helm.sh",shell=True,text=True)
subprocess.check_output("./helm.sh",shell=True,text=True)

while True:
    try:
        code = subprocess.check_output("helm repo add metallb https://metallb.github.io/metallb", shell=True, text=True)
        code = subprocess.check_output("helm install my-metallb metallb/metallb --version 0.14.8", shell=True, text=True)
        log(f"line:48 external_ip exist")
        break
    except:
        time.sleep(5)



time.sleep(5)
while True:
    try:
        subprocess.check_output("kubectl apply -f /opt/containerd/lib/manifests/metallb-config.yaml", shell=True, text=True)
    except Exception as e:
        print(e)
        time.sleep(5)
