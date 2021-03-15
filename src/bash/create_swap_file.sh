#!/usr/bin/env bash

# swap memory reference: https://help.ubuntu.com/community/SwapFaq

# Defaults
default_partition_size="3g"
partition_size=${1:-$default_partition_size}
default_swap_file_path="/$partition_size.swap"
swap_file_path=${2:-$default_swap_file_path}

# See Current Swap File/Partition.
sudo swapon --show

# Create Swap File of size: partition_size GB
sudo fallocate -l "$partition_size" "$swap_file_path"

# Configure File Permissions to restrict unauthorized access.
sudo chmod 600 "$swap_file_path"

# Format File as Swap
sudo mkswap "$swap_file_path"

# Enable Swap Space
sudo swapon "$swap_file_path"

# Verify Swap Space
cat /proc/swaps

# Make Swap File Perpmanent.
echo "$swap_file_path swap defaults 0 0" | sudo tee -a /etc/fstab
