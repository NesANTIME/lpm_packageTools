#!/bin/bash

clear
echo "[!] PROGRAMA DE INSTALACION DE LPM PACKET"
echo " By NesAnTime - v1.2.0"
echo " "

if command -v pipx &> /dev/null 
then
    echo "pipx esta Instalado"
    echo " "
else
    echo "pipx no esta instalado, iniciando instalacion..."

    python3 -m pip install --user pipx
    python3 -m pip ensurepath

    echo "Instalado Correctamente!"
fi

if pipx list | grep -q "lpm" 
then
    pipx uninstall lpm
fi

pipx install .
pipx inject lpm requests

echo