FROM ubuntu:latest

RUN apt-get -q update

# Get pyenv but put it in /usr/local/pyenv rather that the user's home directory
# so it can be used in different dev containers which have different users.
ENV PYENV_ROOT="/usr/local/pyenv"
RUN apt-get install -y git sudo \
 && git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} \
 && git clone https://github.com/pyenv/pyenv-virtualenv.git $(PYENV_ROOT)/plugins/pyenv-virtualenv
 && sudo chmod 777 ${PYENV_ROOT}
ENV PATH="${PYENV_ROOT}/bin:${PATH}"

# Install Python build dependencies (tzdata needs some special handling)
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
  vim

# Install micropython-1.18 using pyenv
RUN apt-get -y install locales
ENV PYENV_VERSION=micropython-1.18
RUN /usr/local/pyenv/bin/pyenv install ${PYENV_VERSION}
RUN pyenv global ${PYENV_VERSION}
RUN pyenv rehash

# Update alternatives so that the pyenv Python is the default Python.
# We can't use an alias because the container's entrypoint is a shell script and .bashrc is not sourced.
# RUN update-alternatives --install /usr/bin/python python ${PYENV_ROOT}/versions/${PYENV_VERSION}/bin/python 1

# For convenience add pyenv to the .bashrc file for root.
USER root
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Set the locale to UTF-8, the default with Ubuntu is Posix and this causes problems for Pyenv in CodeSpaces.
RUN apt-get install -y locales \
 && rm -rf /var/lib/apt/lists/* \
 && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Expose the ports for the APIs
EXPOSE 8080
