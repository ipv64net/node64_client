#!/bin/bash
clear
######here all the variables#######################################################################################
apps="git build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev python3 python3-pip" #add here your application
service_name="node64_io.service"
service_file="/etc/systemd/system/""${service_name}"
####################################################################################################################
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi
#this is the auto-install routine
if ! dpkg -s $apps >/dev/null 2>&1; then
    echo "Currently the source are updated"
    apt update -y >/dev/null 2>&1
    echo "The programs to be required will now be installed."
    apt install $apps -y >/dev/null 2>&1
fi

function print_text() {
    echo "______________________________________________________"
    echo "                   _         ____    ___     _        "
    echo "                  | |       / ___|  /   |   (_)       "
    echo " _ __    ___    __| |  ___ / /___  / /| |    _   ___  "
    echo "| '_ \  / _ \  / _\` | / _ \| ___ \/ /_| |   | | / _ \ "
    echo "| | | || (_) || (_| ||  __/| \_/ |\___  | _ | || (_) |"
    echo "|_| |_| \___/  \__,_| \___|\_____/    |_/(_)|_| \___/ "
    echo "______________________________________________________"
    # @uelle: https://patorjk.com/software/taag/#p=display&h=1&v=2&f=Doom&t=node64.io%0A
}

function get_ipv64_client() {
    if [ ! -d "/opt" ]; then
        mkdir /opt
    fi
    cd /opt/
    git clone https://github.com/ipv64net/ipv64_client.git
    cd ipv64_client/
    pip3 install -r requirements.txt
}

function update_ipv64_client() {
    cd /opt/ipv64_client/
    git fetch --all
    pip3 install -r requirements.txt
}

function ask_for_secret() {
    echo "################################################################"
    read -p "Please enter IPv64-Node-Secret: " secret
    echo "Your Secret is: ${secret}"
    echo "################################################################"
}

function make_service_file() {

    echo "[Unit]" >"${service_file}"
    echo "Description=node64.io client that is receiving tasks for dns, icmp and tracroute task." >>"${service_file}"
    echo "After=network.target" >>"${service_file}"
    echo "StartLimitIntervalSec=0" >>"${service_file}"
    echo "" >>"${service_file}"
    echo "[Service]" >>"${service_file}"
    echo "Type=simple" >>"${service_file}"
    echo "Restart=always" >>"${service_file}"
    echo "WorkingDirectory=/opt/ipv64_client/" >>"${service_file}"
    echo "ExecStart=python3 ipv64_client.py ${secret}" >>"${service_file}"
    echo "" >>"${service_file}"
    echo "[Install]" >>"${service_file}"
    echo "WantedBy=network-online.target" >>"${service_file}"
}

function show_current_config_key() {
    old_config=$(cat "${service_file}" | head -n10 | tail -n1 | awk '{print $3}')
    echo "------------------------------------------------------------------"
    echo "Your current node64.io Secret is: ""${old_config}"
    echo "------------------------------------------------------------------"
}

function show_current_status() {
    node64_status=$(systemctl status node64_io.service | head -n3 | tail -n1 | awk '{print $2}')
    echo "------------------------------------------------------------------"
    echo "Your current status of your node64.io client is: ""${node64_status}"
    echo "------------------------------------------------------------------"
}

function edit_config() {
    show_current_config_key
    while true; do
        read -p "Do you wish to your node64.io Secret? [y|n] " yn
        case $yn in
        [Yy]*)
            ask_for_secret
            make_service_file
            break
            ;;
        [Nn]*)
            echo "No changes have been made."
            exit 0
            ;;
        *) echo "Please answer yes or no." ;;
        esac
    done

}

function delete_ipv64_client() {

    systemctl stop "${service_name}"
    sleep 2
    systemctl disable "${service_name}"
    sleep 2
    rm "${service_file}"
    sleep 2
    rm -r /opt/ipv64_client/
}

display_help() {
    echo "Usage: install-service.sh [-h | --help] [-i | --install] [-u | --update] [-e | --edit] [-c | --config] [-r | --restart] [-d | --delete] [-s | --status]"
    echo "The Node64.io client is receiving tasks for dns, icmp and tracroute task."
    echo
    echo "  -h | --help       -> show this help text"
    echo "  -s | --status     -> show the current node64.io Service status"
    echo "  -i | --install    -> install the node64.io client on your system"
    echo "  -u | --update     -> update the node64.io client to the latest Version"
    echo "  -e | --edit       -> edit your current node64.io config"
    echo "  -c | --config     -> show your current node64.io config"
    echo "  -r | --restart    -> restart the node64.io Service"
    echo "  -d | --delete     -> delete the node64.io Service"
    echo
    exit 1
}

while :; do
    case "$1" in
    -h | --help)
        print_text
        display_help
        exit 0
        ;;
    -i | --install)
        if [ ! -d "/opt/ipv64_client/.git" ]; then
            print_text
            echo "****************************"
            echo "Install the node64.io Client"
            echo "****************************"
            get_ipv64_client
            ask_for_secret
            make_service_file
            echo "----------------------------------------------------"
            echo "The installation of the node64.io Client is finished"
            echo "----------------------------------------------------"
            echo "Enable the node64.io service"
            systemctl daemon-reload
            sleep 2
            systemctl enable "${service_name}"
            sleep 2
            systemctl start "${service_name}"
            break
        else
            print_text
            echo "*********************************************************"
            echo "The node64.io Client is already installed on your System."
            echo "Please update node64.io Client via -u."
            echo "*********************************************************"
            display_help
            exit 1
        fi
        ;;
    -u | --update)
        if [ -d "/opt/ipv64_client/.git" ]; then
            print_text
            echo "***************************"
            echo "Update the node64.io Client"
            echo "***************************"
            update_ipv64_client
            echo "----------------------------------------------"
            echo "The update of the node64.io Client is finished"
            echo "----------------------------------------------"

            break
        else
            print_text
            echo "*********************************************************************************************"
            echo "The directory has not been cloned from Github or node64.io Client has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "*********************************************************************************************"
            display_help
            exit 1
        fi
        ;;
    -e | --edit)
        print_text
        if [ -f "${service_file}" ]; then
            echo "***************************"
            echo "Edit the node64.io Client"
            echo "***************************"
            edit_config
            echo "--------------------------------------------"
            echo "The edit of the node64.io Client is finished"
            echo "--------------------------------------------"
            echo "Reload and restart the node64.io service"
            systemctl daemon-reload
            sleep 2
            systemctl stop "${service_name}"
            sleep 2
            systemctl start "${service_name}"
            break
        else
            echo "***************************************************"
            echo "The service node64.io has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "***************************************************"
            display_help
            exit 1
        fi
        ;;
    -c | --config)
        print_text
        if [ -f "${service_file}" ]; then
            echo "*****************************"
            echo "Show current node64.io Config"
            echo "*****************************"
            show_current_config_key
            break
        else
            echo "***************************************************"
            echo "The service node64.io has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "***************************************************"
            display_help
            exit 1
        fi
        ;;
    -r | --restart)
        print_text
        if [ -f "${service_file}" ]; then
            echo "*********************************"
            echo "Hardrestart the node64.io Service"
            echo "*********************************"
            systemctl daemon-reload
            sleep 2
            systemctl disable "${service_name}"
            sleep 2
            systemctl enable "${service_name}"
            sleep 2
            systemctl start "${service_name}"
            show_current_status
            break
        else
            echo "***************************************************"
            echo "The service node64.io has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "***************************************************"
            display_help
            exit 1
        fi
        ;;

    -d | --delete)
        if ([ -d "/opt/ipv64_client/.git" ] && [ -f "${service_file}" ]); then
            print_text
            echo "***************************"
            echo "Delete the node64.io Client"
            echo "***************************"
            delete_ipv64_client
            echo "---------------------------------------------------"
            echo "The node64.io Client is now removed from the system"
            echo "---------------------------------------------------"
            break
        else
            print_text
            echo "*********************************************************************************************"
            echo "The directory has not been cloned from Github or node64.io Client has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "*********************************************************************************************"
            display_help
            exit 1
        fi
        ;;
    -s | --status)
        print_text
        if [ -f "${service_file}" ]; then
            echo "*****************************"
            echo "Show current node64.io Status"
            echo "*****************************"
            show_current_status
            break
        else
            echo "***************************************************"
            echo "The service node64.io has not been installed yet."
            echo "Please install node64.io Client via github with -i."
            echo "***************************************************"
            display_help
            exit 1
        fi
        ;;

    --)
        shift
        break
        ;;
    -*)
        print_text
        echo "Error: Unknown option: $1" >&2
        display_help
        exit 1
        ;;
    *)
        print_text
        echo "Error: There was no option" >&2
        display_help
        exit 1
        ;;
    esac
done

# created by Mr.Phil
