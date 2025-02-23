# You can change these variables to use a different base image, but
# you must ensure that your base image inherits from one of ours.
# You can also override these at build time with --build-arg flags
ARG BASE_REPO=gradescope/autograder-base
#ARG TAG=ubuntu-20.04
ARG TAG=latest

FROM ${BASE_REPO}:${TAG}


# ======================= installing dependencies ===========================
# Do whatever setup was needed in setup.sh, including installing apt packages
# Cleans up the apt cache afterwards in the same step to keep the image small


RUN apt-get --fix-missing update #&& apt-get upgrade -y

# The base image defines the CMD and ENTRYPOINT, so don't redefine those
RUN apt-get install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu # for xv6 labs
RUN apt-get install -y cowsay expect psmisc ffmpeg valgrind # for simpleshell labs
# adds cowsay to path
ENV PATH="${PATH}:/usr/games"
# install ttyd for vhs
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.x86_64 -O ttyd && \
    mv ttyd /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd
# gets vhs to work on server
ENV VHS_NO_SANDBOX="true"

RUN apt-get install -y python3 python3-pip python3-dev jq
RUN pip3 install gradescope-utils art asyncio

# Cleans up the apt cache afterwards in the same step to keep the image small
# NOTE: this means we can't install any pkg(i.e. run apt install ...) after this
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ADD autograder/clone_dir /usr/bin
RUN chmod +x /usr/bin/clone_dir


RUN mkdir /autograder/hw
ADD autograder/run_autograder /autograder/run_autograder
#RUN cp /autograder/source/run_autograder /autograder/run_autograder


# Ensure that scripts are Unix-friendly and executable
RUN dos2unix /autograder/run_autograder
RUN chmod +x /autograder/run_autograder

# forces to not use cache for the git clone when devleoping
ADD https://github.com/agmui/Gradescope_Setup git_front_page.html
RUN git clone --depth=1 https://github.com/agmui/Gradescope_Setup


# whenever run_autograder changes you need to rebuild and push again
# to build:
# docker build -t os-gradescope-autograders .

# to run localy:
#./docker_run
#   or
#./docker_bash

# to push
#docker tag os-gradescope-autograders agmui/os-gradescope-autograders
#docker push agmui/os-gradescope-autograders:latest

#image name to input into gradescope: agmui/os-gradescope-autograders:latest