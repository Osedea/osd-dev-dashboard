#!/bin/bash

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GREEN='\e[0;30;42m'
YELLOW='\e[0;30;43m'
RED='\e[0;30;41m'
END='\e[0m'
ENDN='\e[0m\n'

USER="$(who am i | awk '{print $1}')"

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    *)          machine="UNKNOWN:${unameOut}"
esac

run_as_user() {
    ME="$(whoami)"
    if [[ "$USER" == "$ME" ]]; then
        bash -c "$1"
    else
        su - "$USER" -c "$1"
    fi;
}

link_configuration() {
    printf "${YELLOW}Removing Old Conky Configuration...${ENDN}"
    run_as_user "rm -rf ~/.conky &> /dev/null"
    printf "${YELLOW}Adding Osedea Conky Configuration...${ENDN}"
    run_as_user "mkdir -p ~/.conky"
    
    run_as_user "cp -r $DIR/* ~/.conky"

    if [[ "$?" == '0' ]]; then
        printf "${GREEN}==> Osedea Conky Configuration Successfully Installed${ENDN}"
    else
        printf "${RED}==> Could not link Osedea Conky Configuration${ENDN}"
        exit 1
    fi;
}

install_conky() {
    if [[ "$(which conky)" != '' ]]; then
        printf "${YELLOW}==> Conky detected, skipping installation...${ENDN}"
    else
        if [[ $EUID -ne 0 ]]; then
            echo "This script must be sudo'd"
            exit 1
        fi
        if [[ "$machine" == "Linux" ]]; then
            printf "${YELLOW}Installing for LINUX...${ENDN}"
            wget https://github.com/brndnmtthws/conky/releases/download/v1.11.5/conky-x86_64.AppImage -P /opt/conky
            apt install jq parallel -y
            chmod +x ./conky-x86_64.AppImage
            ln -s /opt/conkyconky-x86_64.AppImage /usr/local/bin/conky
        elif [[ "$machine" == "Mac" ]]; then
            printf "${YELLOW}Installing for OSX...${ENDN}"
            rm -rf /opt/conky
            rm -rf /tmp/conky_install/ &> /dev/null
            mkdir -p /tmp/conky_install/
            wget https://github.com/brndnmtthws/conky/archive/v1.11.5.zip -P /tmp/conky_install/
            cd /tmp/conky_install
            unzip v1.11.5.zip
            cd conky-1.11.5
            run_as_user "brew install jq parallel cmake freetype gettext lua imlib2 pkg-config librsvg docbook2x lcov"
            run_as_user "brew link gettext --force"
            mkdir build
            cd build
            cmake\
                -DBUILD_TESTS=OFF\
                -DBUILD_LUA_RSVG=ON\
                -DBUILD_LUA_IMLIB2=ON\
                ..
            make
            make install
        fi;
        if [[ "$(which conky)" != '' ]]; then
            printf "${GREEN}==> Conky Successfully Installed${ENDN}"
        else
            printf "${RED}==> Conky Not Installed${ENDN}"
            exit 1
        fi;
    fi;
}

generate_configuration() {
    python3 ./src/generator.py
}
install() {
    install_conky
    generate_configuration
    link_configuration
}

install
