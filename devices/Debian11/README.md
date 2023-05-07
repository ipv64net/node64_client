# IPv64 Client on Debian11

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

## Requirements

### Hardware

- Debian 11
- 2 GB or more Storage free

### Software

- wget

```sh
sudo apt install wget
```

## Installation

1. Execute install script

- install the service

```sh
wget https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/Debian11/install-service.sh
sudo bash install-service.sh -i
```

- update the service

```sh
wget https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/Debian11/install-service.sh
sudo bash install-service.sh -u
```

- print the help message

```sh
wget https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/Debian11/install-service.sh
sudo bash install-service.sh -h
```

## OR Step by Step

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

5. Copy the [Service-File](https://github.com/ipv64net/ipv64_client/blob/main/devices/Debian11/systemd/node64_client.service) to the folder /etc/systemd/system/

```sh
wget -O /etc/systemd/system/node64_client.service https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/Debian11/systemd/node64_client.service
```

6. Edit the Node #Secret in the Servicefile
7. Enable the Service

```sh
systemctl enable --now node64_client
```
