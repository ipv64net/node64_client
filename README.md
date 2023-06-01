# IPv64 Client

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

[![Syntax Check](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml/badge.svg)](https://github.com/ipv64net/ipv64_client/actions/workflows/main.yml)

[![Docker Build](https://github.com/ipv64net/ipv64_client/actions/workflows/docker-ghcr.yml/badge.svg)](https://github.com/ipv64net/ipv64_client/actions/workflows/docker-ghcr.yml)


## Installation

Install the dependencies and start the server.

```sh
apt install python3 python3-pip git -y
git clone https://github.com/ipv64net/node64_client
cd node64_client
pip3 install -r requirements.txt
```

## Start
### Node Secret as Parameter
```sh
python3 node64.py <Your Node Secret Key>
```
### Node Secret as Environment Variable

#### variant 1

```sh
export Node64Secret=<Your Node Secret Key>
python3 node64.py
```

#### variant 2

```sh
Node64Secret=<Your Node Secret Key> python3 node64.py <Your Node Secret Key>
```

### enable color output

To activate the color output an environment variable Node64Color is needed
```sh
export Node64Color=true
```
### enable verbose

To enable verbose, the verbose checkbox on the website must be activated.


## Installation on hardware devices

[Debian 11](devices/Debian11/README.md)

[Docker](devices/Docker/DOCKER.md)

[Mango (GL-MT300N-V2)](devices/gl-inet/GL-MT300N-V2/README.md)
