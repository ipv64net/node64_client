# IPv64 Client

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

[![Syntax Check](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml/badge.svg)](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml)
[![Docker Container](https://github.com/ipv64net/ipv64_client/actions/workflows/docker-build.yml/badge.svg)](https://github.com/ipv64net/ipv64_client/actions/workflows/docker-build.yml)

## Installation

Install the dependencies and start the server.

```sh
apt install python3 python3-pip git -y
git clone https://github.com/ipv64net/ipv64_client
cd ipv64_client
pip3 install -r requirements.txt
python3 ipv64_client.py <Dein Node Secret Key>
```

## Installation on hardware devices

[Debian 11](devices/Debian11/README.md)

[Docker](devices/Docker/README.md)

[Mango (GL-MT300N-V2)](devices/gl-inet/GL-MT300N-V2/README.md)
