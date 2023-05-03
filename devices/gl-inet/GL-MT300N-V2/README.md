# IPv64 Client on Mango (GL-MT300N-V2)

![alt text](/files/images/ipv64_darkmode.svg#gh-dark-mode-only "Logo")
![alt text](/files/images/ipv64_lightmode.svg#gh-light-mode-only "Logo")

## Hardware Requirements

 - GL.iNet Mango (GL-MT300N-V2)
 - USB Stick with 2 GB or more
 
## Installation

1. Reinstall the Mango following the [guide](https://openwrt.org/toh/gl.inet/gl-mt300n_v2)
2. Mount the USB Stick as mount device following the [guide](https://openwrt.org/docs/guide-user/additional-software/extroot_configuration)
3. Install the required packages
```sh
opkg update
opkg --force-removal-of-dependent-packages install python3
opkg --force-removal-of-dependent-packages install python3-pip
opkg --force-removal-of-dependent-packages install git-http
opkg --force-removal-of-dependent-packages install ca-bundle
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
wget -O /etc/init.d/node64_client https://raw.githubusercontent.com/ipv64net/ipv64_client/main/devices/gl-inet/GL-MT300N-V2/init.d/node64_client
```
6. Edit the Node #Secret in the Servicefile
7. Allow to execute the Servicefile
```sh
chmod +x /etc/init.d/node64_client
```
8. Enable the Service and Reboot the Mango
```sh
/etc/init.d/node64_client enable
reboot
```
