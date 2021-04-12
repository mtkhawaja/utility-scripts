#!/usr/bin/env bash

echo "⌛ Downloading dotfile repo."
git clone 'https://github.com/mtkhawaja/dotfiles.git' '/var/tmp/dotfiles'

echo "⌛ Running setup script."
# shellcheck disable=SC1091
source '/var/tmp/dotfiles/scripts/setup.sh'
echo "✅ Setup complete."

echo "⌛ Removing dotfile repo."
rm -r --interactive=never '/var/tmp/dotfiles'
echo "✅ Repo removed."
