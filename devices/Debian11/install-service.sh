#!/bin/bash
clear
######here all the variables#######################################################################################
apps="git build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev python3 python3-pip" #add here your application
service_file="/etc/systemd/system/node64_client.service"
initD_file="/etc/init.d/node64_client"
####################################################################################################################
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi
#this is the auto-install routine
if ! dpkg -s $apps >/dev/null 2>&1; then
    apt install $apps -y
fi

function get_ipv64_client() {
    mkdir /opt
    cd /opt/
    git clone https://github.com/ipv64net/ipv64_client.git
    cd ipv64_client/
    pip3 install -r requirements.txt
}

function update_ipv64_client() {
    cd /opt/ipv64_client/
    git pull
    pip3 install -r requirements.txt
}

function ask_for_secret() {
    read -p "Please enter IPv64-Node-Secret: " secret
    echo "Your Secret is: ${secret}"
}

function make_service_file() {

    echo "[Unit]" >>"${service_file}"
    echo "Description=Node64 Client Script" >>"${service_file}"
    echo "After=network.target" >>"${service_file}"
    echo "StartLimitIntervalSec=0" >>"${service_file}"
    echo "" >>"${service_file}"
    echo "[Service]" >>"${service_file}"
    echo "Type=simple" >>"${service_file}"
    echo "Restart=always" >>"${service_file}"
    echo "WorkingDirectory=/opt/ipv64_client/" >>"${service_file}"
    echo "ExecStart=python ipv64_client.py ${secret}" >>"${service_file}"
    echo "" >>"${service_file}"
    echo "[Install]" >>"${service_file}"
    echo "WantedBy=network-online.target" >>"${service_file}"
}

function make_initD_file() {
    echo "#!/bin/sh /etc/rc.common" >>"${initD_file}"
    echo "USE_PROCD=1" >>"${initD_file}"
    echo "START=95" >>"${initD_file}"
    echo "STOP=01" >>"${initD_file}"
    echo "start_service() {" >>"${initD_file}"
    echo "    procd_open_instance" >>"${initD_file}"
    echo "    procd_set_param respawn ${threshold:-20} ${timeout:-5} ${retry:-3}" >>"${initD_file}"
    echo "    procd_set_param command /usr/bin/python3 "/opt/ipv64_client/ipv64_client.py" ${secret}" >>"${initD_file}"
    echo "    procd_close_instance" >>"${initD_file}"
    echo "}" >>"${initD_file}"
}

display_help() {
    echo "Usage: install-service.sh [-h | --help] [-i | --install] [-u | --update] -- Here should be a description about the node64_client in the near future." >&2
    echo
    echo "  -h | --help    -> show this help text"
    echo "  -i | --install -> install the node64_client on your system"
    echo "  -u | --update  -> update the node64_client to the latest Version"
    echo
    # echo some stuff here for the -a or --add-options
    exit 1
}

################################
# Check if parameters options  #
# are given on the commandline #
################################
while :; do
    case "$1" in
    -h | --help)
        display_help # Call your function
        exit 0
        ;;
    -i | --install)
        echo "------------------------"
        echo "Install the node64_Client"
        echo "------------------------"
        get_ipv64_client
        ask_for_secret
        make_service_file
        make_initD_file
        echo "------------------------"
        echo "The installation of the node64_client is finished"
        echo "------------------------"
        echo "Enable the service with:"
        echo "systemctl daemon-reload"
        echo "systemctl enable node64_client.service"
        echo "systemctl enable --now node64_client"
        break
        ;;
    -u | --update)
        echo "------------------------"
        echo "Update the node64_Client"
        echo "------------------------"
        update_ipv64_client
        echo "The update of the node64_client is finished"
        echo "------------------------"
        echo "now restart the node64_client Service with:"
        echo "systemctl restart node64_client.service"
        break
        ;;

    --) # End of all options
        shift
        break
        ;;
    -*)
        echo "Error: Unknown option: $1" >&2
        ## or call function display_help
        display_help
        exit 1
        ;;
    *) # No more options
        display_help
        exit 1
        ;;
    esac
done
