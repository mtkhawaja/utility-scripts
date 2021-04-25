#!/usr/bin/env bash

function main() {
    if [[ "$#" -lt 1 ]]; then
        echo 'Please provide absolute path to git repo !'
    else
        path_to_repo=$1
        git -C "$path_to_repo" pull origin
    fi
}

main "$@"
