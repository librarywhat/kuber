import os.path
import subprocess
import time

def log(*message):
    with open('/opt/logs.csv','a',encoding='utf-8') as f:
        f.write(f'{message}\n')

counter=0
while True:
    try:
        ip = subprocess.check_output("kubectl get svc -A | awk '/ingress-nginx-controller/ {print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'", shell=True, text=True)
        log(f"line:13 ip: {ip}")

        with open("/opt/containerd/lib/manifests/metallb-config.yaml", 'w', encoding='utf-8') as f:
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
            
        log(f"line:34 file done: {ip}")

        
        break
    except subprocess.CalledProcessError as e:
        log(f"line:39, retry:{counter} error: {e}")
        counter+=1
        time.sleep(5)
        continue
    


while True:
    try:
        ip = subprocess.check_output("kubectl get svc -A | awk '/ingress-nginx-controller/ {print $5}' | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'", shell=True, text=True)
        log(f"line:49 external_ip exist")
        time.sleep(5)
        continue
    except subprocess.CalledProcessError as e:
        os.system("kubectl apply -f /opt/containerd/lib/manifests/metallb-config.yaml")
        log(f"line:54 all done")
        break
