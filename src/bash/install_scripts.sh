#!/usr/bin/env bash

function main() {
    # Config
    default_installation_path="$HOME/bin/utility-scripts"
    repo_url='https://github.com/mtkhawaja/utility-scripts.git'
    bash_profile="$HOME/.bash_profile"

    if installation_exists "$default_installation_path"; then
        remove_existing_installation "$default_installation_path"
    fi

    clone_repo "$default_installation_path" "$repo_url"
    configure_PATH "$default_installation_path" "$bash_profile"
    configure_cron_job "$default_installation_path"
    reload_bash_profile "$bash_profile"
}

#######################################
# Check for existing installation.
# Arguments:
#   $1 = Path to installation directory.
# Output:
#   0 = Existing installation found.
#   1 = No existing installation found.
#######################################
function installation_exists() {
    installation_path=$1
    echo "⌛ Checking for existing installation."
    if [ -d "$installation_path" ]; then
        echo "⌛ Existing installation found."
        return 0
    fi
    echo "✅ No existing installation found."
    return 1
}

#######################################
# Check for existing installation.
# Arguments:
#   $1 = Path to installation directory.
#######################################
function remove_existing_installation() {
    installation_path=$1
    echo "⌛ Removing existing installation."
    rm -rf "$installation_path"
    ret_val="$?"
    echo "✅ Existing installation removed."
    return $ret_val
}

#######################################
# Check for existing installation.
# Arguments:
#   $1 = Path to installation directory.
#   $2 = URL to GitHub repo
#######################################
function clone_repo() {
    installation_path=$1
    url_repo=$2
    echo "⌛ Cloning $url_repo. to $url_repo"
    git clone "$url_repo" "$installation_path"
    ret_val="$?"
    echo "✅ Existing installation removed."
    return $ret_val
}

#######################################
# Check for existing installation.
# Arguments:
#   $1 = Path to installation directory.
#   $2 = Path to bash_profile.
#######################################
function configure_PATH() {
    installation_path=$1
    bash_profile=$2
    paths_to_add=("$installation_path/src/python" "$installation_path/src/bash")
    echo "⌛ Configuring PATH."
    for script_dir in "${paths_to_add[@]}"; do
        if ! grep -qxF "$script_dir" "$bash_profile"; then
            echo 'PATH=$PATH:'"$script_dir" >>"$bash_profile"
            echo "✅ Added $script_dir"
        else
            echo "✅ $script_dir already exists. Skipping."
        fi
    done
    echo "✅ PATH Configured."
    return 0
}

#######################################
# Check for existing installation.
# Arguments:
#   $1 = Path to installation directory.
#######################################
function configure_cron_job() {
    installation_path=$1
    cron_schedule='0 6 * * *'
    cron_script="$installation_path/src/bash/sync_git_repo.sh"
    cron_script_args="$installation_path"
    helper_script="$installation_path/src/bash/install_cron_job.sh"
    echo "⌛ Configuring cronjob to check for updates at 06:00"
    bash "$helper_script" "$cron_schedule" "$cron_script" "$cron_script_args"
    ret_val="$?"
    echo "✅ Completed CRON job configuration."
    return "$ret_val"
}

function reload_bash_profile() {
    echo "⌛ Reloading .bash_profile."
    bash_profile=$1
    source "$bash_profile"
    echo "✅ .bash_profile reloaded."
    return "$?"
}

main "$@"
