FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    curl -L https://encore.dev/install.sh | bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.encore/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore.ts project environment with Node.js v24 installed."

RUN cd /home/user && \
    encore app create app --lang=typescript --example=ts/hello-world

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the Encore.ts task environment
#   - Encore CLI installed in /root/.encore/bin
#   - /home/user/app: initialized Encore.ts project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
