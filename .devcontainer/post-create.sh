#!/bin/bash
# Activate Starship in the .bashrc
echo 'eval "$(starship init bash)"' >> ~/.bashrc
# Then add pyenv
curl https://pyenv.run | bash
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo 'I be done now!'
