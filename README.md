# IPv64 Client

![alt text](https://ipv64.net/img/ipv64_logo.svg "Logo")

[![Syntax Check](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml/badge.svg)](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml)

## Installation

Install the dependencies and start the server.

```sh
apt install python3 python3-pip git -y
git clone https://github.com/ipv64net/ipv64_client
cd ipv64_client
pip3 install -r requirements.txt
python3 ipv64_client.py <Dein Node Secret Key>
```


## Docker
```sh
git clone https://github.com/ipv64net/ipv64_client
cd ipv64_client
docker-compose build
```
Edit docker-compose.yml
```sh
docker-compose up -d
```


## Installation on hardware devices

[Debian 11](devices/Debian11/README.md)

[Mango (GL-MT300N-V2)](devices/gli-net/GL-MT300N-V2/README.md)
