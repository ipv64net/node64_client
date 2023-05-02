# IPv64 Client on Debian11

![alt text](https://ipv64.net/img/ipv64_logo.svg "Logo")

## Hardware Requirements

 - Debian 11
 - 2 GB or more Storage free
 
## Installation


1. Install the required packages
```sh
apt update
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
apt install python3 -y
apt install python3-pip -y
```
4. Download the Node64 files and install the required python-packages
```sh
mkdir /opt
cd /opt/
git clone https://github.com/ipv64net/ipv64_client.git
cd ipv64_client/
pip3 install -r requirements.txt
```
5. Copy the [Service-File](https://github.com/ipv64net/ipv64_client/blob/main/devices/gl-inet/GL-MT300N-V2/init.d/node64_client) to the folder /etc/init.d/
```sh
wget -O /etc/systemd/system/node64_client.service https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/Debian11/systemd/node64_client.service
```
6. Edit the Node #Secret in the Servicefile
7. Enable the Service
```sh
systemctl enable --now node64_client
```
