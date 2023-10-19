#!/bin/bash
# Activate Starship in the .bashrc
curl https://pyenv.run | bash
echo 'eval "$(starship init bash)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
