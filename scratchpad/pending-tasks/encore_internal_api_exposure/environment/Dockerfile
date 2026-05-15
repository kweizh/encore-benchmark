FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Encore
RUN curl -L https://encore.dev/install.sh | bash
ENV PATH="/root/.encore/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore project with an internal API endpoint."

# Setup the project
RUN mkdir -p /home/user/my-app/hello && \
    cd /home/user/my-app && \
    cat > encore.app <<'INNER_EOF'
id: "my-app"
INNER_EOF

RUN cd /home/user/my-app && \
    cat > package.json <<'INNER_EOF'
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "encore.dev": "latest"
  }
}
INNER_EOF

RUN cd /home/user/my-app && \
    cat > tsconfig.json <<'INNER_EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "CommonJS",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
INNER_EOF

RUN cd /home/user/my-app && \
    cat > hello/hello.ts <<'INNER_EOF'
import { api } from "encore.dev/api";

export const myEndpoint = api(
  { method: "GET", path: "/hello/:name" },
  async ({ name }: { name: string }) => ({ message: `Hello ${name}` })
);
INNER_EOF

RUN cd /home/user/my-app && npm install

# Container contents:
#   - Encore CLI installed.
#   - Node.js v24 installed.
#   - /home/user/my-app - Encore project with an internal API.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]