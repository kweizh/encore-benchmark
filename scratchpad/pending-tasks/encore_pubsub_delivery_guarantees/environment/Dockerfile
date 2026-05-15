FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    curl -L https://encore.dev/install.sh | bash && \
    ln -s /root/.encore/bin/encore /usr/local/bin/encore && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore framework environment with Node.js v24 for building an Encore Pub/Sub app."

# Container contents:
#   - Node.js v24 installed
#   - Encore CLI installed and linked to /usr/local/bin/encore
#   - /home/user created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
