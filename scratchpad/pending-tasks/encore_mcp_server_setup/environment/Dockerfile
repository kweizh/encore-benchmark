FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash
ENV PATH="/root/.encore/bin:${PATH}"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore environment with a basic app initialized."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    encore app create my-test-app --lang=ts --example=hello-world && \
    mv my-test-app/* . && \
    rm -rf my-test-app

ENV PATH="/home/user/.encore/bin:${PATH}"

# Container contents:
#   - encore CLI installed.
#   - /home/user/app - an existing Encore app.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]