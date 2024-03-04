# You can change these variables to use a different base image, but
# you must ensure that your base image inherits from one of ours.
# You can also override these at build time with --build-arg flags
ARG BASE_REPO=gradescope/autograder-base
ARG TAG=ubuntu-20.04
#ARG TAG=latest

FROM ${BASE_REPO}:${TAG}


# ======================= installing dependencies ===========================
# Do whatever setup was needed in setup.sh, including installing apt packages
# Cleans up the apt cache afterwards in the same step to keep the image small
RUN apt-get update #&& apt-get upgrade -y

# The base image defines the CMD and ENTRYPOINT, so don't redefine those
RUN apt-get install -y build-essential gdb-multiarch qemu-system-misc gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu # for xv6 labs
RUN apt-get install -y cowsay expect # for simpleshell labs

RUN apt-get install -y python3 python3-pip python3-dev jq
RUN pip install gradescope-utils art asyncio

# Cleans up the apt cache afterwards in the same step to keep the image small
# NOTE: this means we can't install any pkg(i.e. run apt install ...) after this
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



RUN mkdir /autograder/source
ADD autograder/run_autograder /autograder/source/run_autograder
RUN cp /autograder/source/run_autograder /autograder/run_autograder

ADD autograder/clone_dir /usr/bin
RUN chmod +x /usr/bin/clone_dir

# Ensure that scripts are Unix-friendly and executable
RUN dos2unix /autograder/run_autograder
RUN chmod +x /autograder/run_autograder

# -- debugging --
#RUN git clone https://github.com/agmui/gradescope_semgrep
ADD hw gradescope_semgrep/hw
ADD grading_utils gradescope_semgrep/grading_utils
ADD .git gradescope_semgrep/.git
# --


# to build:
# docker build -t autograder_test .

# to run localy:
# docker run --rm -it -v /path/to/submission:/autograder/submission -v /path/to/results:/autograder/results username/image_name:tag bash
# docker run --rm -it -v ./autograder/temp_sub:/autograder/submission -v ./autograder/temp_rez:/autograder/results -v ./autograder/sample_output.json:/autograder/submission_metadata.json autograder_test:latest bash
# docker run --rm -it -v ./autograder/temp_sub:/autograder/submission -v ./autograder/temp_rez:/autograder/results -v ./autograder/sample_output.json:/autograder/submission_metadata.json autograder_test:latest /autograder/run_autograder && cat /autograder/results/results.json