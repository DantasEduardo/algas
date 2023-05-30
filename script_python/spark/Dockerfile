FROM debian:stable-slim

COPY raw_staged.py /opt/raw_staged.py
COPY staged_consumed.py /opt/staged_consumed.py
COPY send_data.py /opt/send_data.py

COPY data-raw /opt/data-raw
COPY requirements.txt /opt/requirements.txt

COPY execute.sh /opt/execute.sh

RUN apt-get update && apt-get install openjdk-11-jdk -y 

RUN if which python; then echo Python already installed; else \
    echo Installing Python; \
    apt update && \
    apt install -y python3 python3-pip && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*; fi

RUN pip3 install -r /opt/requirements.txt
ENV PATH="/opt/program:${PATH}"

WORKDIR /opt/
ENTRYPOINT [ "bash","execute.sh" ]