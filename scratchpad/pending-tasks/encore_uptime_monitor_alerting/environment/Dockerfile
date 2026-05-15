FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash docker.io && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash
ENV PATH="/root/.encore/bin:${PATH}"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore Uptime Monitor task environment."

RUN cd /home/user && \
    encore app create uptime-monitor --lang=ts && \
    cd uptime-monitor && \
    npm install

# Container contents:
#   - Node.js v24 and docker.io installed
#   - Encore CLI installed
#   - /home/user/uptime-monitor - initialized Encore application

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
