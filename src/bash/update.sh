#!/usr/bin/env bash

# Install Updates
sudo apt update
sudo apt upgrade -y
# Remove: Unused Packages and Old Package Versions
sudo apt autoremove
sudo apt autoclean
