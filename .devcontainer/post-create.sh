#!/bin/bash
# Activate Starship in the .bashrc
echo 'eval "$(starship init bash)"' >> ~/.bashrc
# Add pyenv to the .bashrc
echo 'export PYENV_ROOT="/usr/local/pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo 'I be done now!'
