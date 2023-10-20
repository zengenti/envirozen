FROM ubuntu:latest

RUN apt-get -q update

# Get pyenv but put it in /usr/local/pyenv rather that the user's home directory
# so it can be used in different dev containers which have different users.
ENV PYENV_ROOT="/usr/local/pyenv"
ENV PATH="${PYENV_ROOT}/bin:${PATH}"
RUN apt-get install -y git sudo \
 && git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} \
 && sudo chmod 777 ${PYENV_ROOT}

# Install Python build dependencies (tzdata needs some special handling)
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
