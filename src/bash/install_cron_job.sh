#!/usr/bin/env bash

function main() {
    # CLI
    cron_schedule=$1
    cron_script=$2
    cron_script_args=$3
    cron_job="$cron_schedule $cron_script $cron_script_args"
    # Config
    time_stamp=$(date +%Y-%m-%d-%m%s)
    base_path="${BASH_SOURCE%/*}"
    backup_file="$base_path/../data/backups/$time_stamp-cron.bak"
    temp_file="/var/tmp/$time_stamp-cron_file_dump"

    # Core
    dump_existing_cron_config "$backup_file" "$temp_file"
    if append_job "$temp_file" "$cron_job" = 0; then
        install_cronjob "$temp_file"
        cleanup "$temp_file"
    fi
    return 0
}

function dump_existing_cron_config() {
    backup_file=$1
    temp_file=$2
    crontab -l >"$backup_file"
    crontab -l >"$temp_file"
    return 0
}

#######################################
# Append job if it does not exist.
# Arguments:
#   $1 = path to cron file.
#   $2 = cron job.
#        Example: 0 13 * * * pwd
# Outputs:
# 0: Added New Job
# 1: Job exists; Job Addition skipped.
#######################################
function append_job() {
    cron_file=$1
    cron_job=$2
    if grep -qxF "$cron_job" "$cron_file"; then
        echo "cron job already exists !"
        return 1
    fi
    echo "$cron_job" >>"$cron_file"
    return 0
}

function install_cronjob() {
    cron_file=$1
    crontab "$cron_file"
    return 0
}

function cleanup() {
    cron_file=$1
    rm "$cron_file"
    return 0
}

main "$@"
