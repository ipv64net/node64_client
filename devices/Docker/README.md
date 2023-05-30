# IPv64 Client on Docker

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

## Hardware Requirements

 - [Docker](https://github.com/docker/docker-install)
 
## Installation

Instructions for Compose V2 (From the end of June 2023 Compose V1 won’t be supported anymore) https://docs.docker.com/compose/


1. Clone repo
```sh
git clone https://github.com/ipv64net/node64_client.git
cd node64_client/devices/Docker/
```
2. Build
```sh
docker compose build
```
3. Edit the Node #Secret in the docker-compose.yml or create .env file in same directory and insert ipv64NodeSecret=<Node #Secret>
4. run
```sh
docker compose up -d
```
## Installation with Prebuild Container CLI

1. Before starting the container you have to replace ${ipv64NodeSecret} with your Node Secret
```sh
docker run -d \
  --name node64_client \
  -e Node64Secret=<Node #Secret> \
  --restart=unless-stopped \
  ghcr.io/ipv64net/ipv64_client:latest
```

## Installation with Prebuild Container Compose (Protainer)

1. Before starting deploy the compose replace ${ipv64NodeSecret} with your Node Secret or use .env file
```yml
version: '3.8'
services:
  node64_client:
    restart: unless-stopped
    container_name: node64_client
    image: ghcr.io/ipv64net/ipv64_client:latest
    environment:
      - Node64Secret=${ipv64NodeSecret}
```
