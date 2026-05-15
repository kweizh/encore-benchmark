FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash

ENV ENCORE_INSTALL="/root/.encore"
ENV PATH="$ENCORE_INSTALL/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore environment with Node.js v24 for multi-service communication task."

# Container contents:
#   - Node.js v24 installed.
#   - Encore CLI installed.
#   - /home/user base directory.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
