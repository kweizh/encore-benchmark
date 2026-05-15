FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    curl -L https://encore.dev/install.sh | bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Encore to PATH
ENV PATH="/root/.encore/bin:${PATH}"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore.ts file processing task environment with Node.js v24 and Encore CLI installed."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    npm install encore.dev@latest

# Container contents:
#   - curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24
#   - Encore CLI
#   - /home/user/app: Empty project directory with encore.dev installed

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
