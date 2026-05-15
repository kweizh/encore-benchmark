FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore CI/CD task environment with Encore CLI installed."

# Install Encore CLI in the environment so the agent can use it to create the app
RUN curl -L https://encore.dev/install.sh | bash

# Add encore to PATH
ENV PATH="/root/.encore/bin:$PATH"
# Wait, the install script puts it in $HOME/.encore/bin which is /root/.encore/bin for root user.
# But the agent might run as root, so /root/.encore/bin is correct.
# Actually, the task description says: "/home/user/.encore/bin/encore auth login"
# But the agent runs as root in the container, so $HOME is /root.
# Let's adjust the task description to use `~/.encore/bin/encore` or just `encore`.
# I'll rewrite the task description in a moment.

# Container contents:
#   - Node.js v24 for TypeScript support
#   - Encore CLI installed in /root/.encore/bin
#   - /home/user: base directory for the project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]