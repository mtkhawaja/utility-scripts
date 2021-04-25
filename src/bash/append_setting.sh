#!/usr/bin/env bash

#######################################
# Append supplied setting to file if
# the setting does not already exist.
# CLI Arguments:
#   $1 = file to append setting to.
#   $2 = setting.
#######################################

function main() {
    if [ "$#" -lt 2 ]; then
        echo 'Invalid number of arguments supplied !'
        return 1
    fi
    file=$1
    setting=$2
    if [ ! -e "$file" ]; then
        return 1
    fi
    if setting_exists "$file" "$setting" = 0; then
        echo 'Supplied setting already exists!'
        return 0
    fi
    append_header "$file"
    append_setting "$file" "$setting"
    return 0
}

#######################################
# Check if a setting (line) exists.
# Arguments:
#   $1 = file to be searched.
#   $2 = fixed search pattern.
# GREP Flags:
# q = Quiet Mode | x = Ignore Case | F = Fixed (exact) match
# Outputs:
# 0: Match Found | 1: Match Not Found
#######################################
function setting_exists() {
    file=$1
    pattern=$2
    grep -qxF "$pattern" "$file"
    return $?
}

#######################################
# Append header to file.
# Arguments:
#   $1 = File to append setting(s) to.
#######################################
function append_header() {
    header="# Programatically added on $(date)"
    file=$1
    echo "$header" >>"$file"
}

#######################################
# Append setting to specified file
# Arguments:
#   $1 = File to append setting(s) to.
#   $2 = setting(s).
#######################################
function append_setting() {
    file=$1
    setting=$2
    echo "$setting" >>"$file"
}

main "$@"
