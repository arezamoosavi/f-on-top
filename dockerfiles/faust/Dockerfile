FROM ubuntu:latest

# Install OpenJDK 8
RUN \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_FORMAT=legacy

RUN apt-get -y update && apt-get install -y libzbar-dev bash gcc git libc-dev
RUN apt-get install -y build-essential
RUN apt-get install -y netcat && apt-get autoremove -y

RUN apt-get update && \
    apt-get -y install sudo

RUN useradd -m alireza && echo "alireza:alireza" | chpasswd && adduser alireza sudo

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

COPY dockerfiles/faust/requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf requirements.txt

RUN mkdir -p /services
COPY ./services /services

COPY dockerfiles/faust/faust_run.sh /faust_run.sh
RUN chmod 777 /faust_run.sh
RUN chmod 777 ./

WORKDIR /services