# IPv64 Client

![alt text](https://ipv64.net/img/ipv64_logo.svg "Logo")

## Installation

Install the dependencies and start the server.

```sh
apt install python3 python3-pip git -y
git clone https://github.com/ipv64net/ipv64_client
cd ipv64_client
pip install dnspython icmplib multiping requests
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
