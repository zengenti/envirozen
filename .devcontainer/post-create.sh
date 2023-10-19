#!/bin/bash
# Activate Starship in the .bashrc
echo 'eval "$(starship init bash)"' >> ~/.bashrc
# Then add pyenv
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo 'I be done now!'
