#!/usr/bin/env bash

# Download, Install and Configure Uncomplicated Firewall (UWF)
sudo apt install ufw

# Allow SSH Connections
ufw allow OpenSSH

# Allow Outbound Traffic
sudo ufw default allow outgoing
sudo ufw allow https

# Deny Inbound Traffic
sudo ufw default deny incoming

ufw enable -y

# View Status
sudo ufw status verbose
echo "Ports in Use:"
sudo lsof -i -P -n | grep LISTEN
