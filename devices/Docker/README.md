# node64 Client on Docker

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

## Requirements

 - [Docker](https://github.com/docker/docker-install)
 - [ipv6 Support (optional)](#ipv6)
 
## Installation

Instructions for Compose V2 (From the end of June 2023 Compose V1 won’t be supported anymore) https://docs.docker.com/compose/


<a name="ipv6"></a>

### enable IPV6 Support (optional only experienced user)

The `/etc/docker/daemon.json` does not exist by default.

1. Container will use host ip
    ```sh
    sudo cat <<EOF >/etc/docker/daemon.json
    {
      "ipv6": true,
      "fixed-cidr-v6": "fd00:dead:beef:c0::/80",
      "ip6tables":true,
      "experimental":true
    }
    EOF
    ```  
    Restart docker.  
    ```sh
    sudo systemctl restart docker
   ```
2. own ip **#TODO**

### Prebuild Container

Before starting the container you have to create `.env` file in same directory and insert `Node64Secret=<Node #Secret>` or edit the `Node64Secret` in the `docker-compose.yml`  
The `.env` is the preferred option (will not overwrite by update).

If you want use the dev branch you can use the `ghcr.io/ipv64net/inode64_client_dev:latest` image.

### docker cli

```sh
docker run -d \
  --name node64client \
  -e Node64Secret=<Node #Secret> \
  --restart=unless-stopped \
  --network="bridge" \
  ghcr.io/ipv64net/node64_client:latest
```

### docker compose

```yml
version: '3.8'
services:
  node64client:
    restart: unless-stopped
    container_name: node64client
    image: ghcr.io/ipv64net/node64_client:latest
    network_mode: bridge
    environment:
      - Node64Secret=${ipv64NodeSecret}
      - Node64Color=true #optional
```

### build yourself

1. Clone repo
    ```sh
    git clone https://github.com/ipv64net/node64_client.git
    cd node64_client/devices/Docker/
    ```
2. Build (if you update the repo then rerun)
    ```sh
    docker compose build
    ```
3.  Create .env file in same directory and insert `Node64Secret=<Node #Secret>` or edit the Node #Secret in the `docker-compose.yml`  
The `.env` is the preferred option (will not overwrite by update)
4. run
    ```sh
    docker compose up -d
    ```

