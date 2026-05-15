FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash unzip && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash

ENV ENCORE_INSTALL="/root/.encore"
ENV PATH="$ENCORE_INSTALL/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore environment with Node.js v24."

# Container contents:
#   - curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Encore typescript task
#   - Encore CLI installed to /root/.encore/bin

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
