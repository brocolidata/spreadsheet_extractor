FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get -y install \
        software-properties-common \
        curl \
        unzip \
        bash \
        python3-pip \
        git \
        make \
        libffi-dev \
        jq \
        libpq-dev\
        gcc

# Copy & Install the dependencies file
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH "${PATH}:~/.local/bin"
