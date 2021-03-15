#!/usr/bin/env bash

# unattended-upgrades Reference: https://wiki.debian.org/UnattendedUpgrades

##################################################
# Enable Unattended Updates and:
#  * Security Updates (default)
#  * Upgradeable Packages
# Globals:
#   None
# Arguments:
#  $1: Path to apt configuration stub for
#      unattended-upgrades.
##################################################

function enable_unattended_updates() {
  cat <<EOF >"$1"
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::Unattended-Upgrade "1";
EOF
}

##################################################
# Configure Unattended Updates to:
#  * Remove Unused Dependencies
#  * Remove Unused Kernel Packages
#  * Automatically Reboot if necessary.
# Globals:
#   None
# Arguments:
#  $1: Path to default configuration file for
#      unattended-upgrades.
##################################################

function configure_unattended_updates() {
  settings=("Unattended-Upgrade::Remove-Unused-Dependencies")
  settings+=("Unattended-Upgrade::Remove-Unused-Kernel-Packages")
  settings+=("Unattended-Upgrade::Automatic-Reboot")
  for option in "${settings[@]}"; do
    sed -i "s|^//$option\s.*|$option \"true\";|" "$1"
  done
}

# Download, Install and Configure Automatic Updates
sudo apt install unattended-upgrades
enable_path="/etc/apt/apt.conf.d/20auto-upgrades"
config_path="/etc/apt/apt.conf.d/50unattended-upgrades"
if [ ! -a "/etc/apt/apt.conf.d/20auto-upgrades" ]; then
  enable_unattended_updates $enable_path
fi
setup_unattended_updates $config_path
