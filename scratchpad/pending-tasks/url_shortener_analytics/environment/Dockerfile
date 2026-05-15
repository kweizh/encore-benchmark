FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash docker.io && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Encore
ENV ENCORE_INSTALL=/root/.encore
RUN curl -L https://encore.dev/install.sh | bash
ENV PATH="$ENCORE_INSTALL/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore environment with Node.js and Docker installed for URL shortener task."

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - docker.io for running local databases
#   - Node.js v24 for TypeScript support
#   - Encore CLI installed in /root/.encore/bin

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]