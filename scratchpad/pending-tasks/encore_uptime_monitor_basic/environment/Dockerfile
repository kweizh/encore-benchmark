FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash

ENV ENCORE_INSTALL="/root/.encore"
ENV PATH="$ENCORE_INSTALL/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore environment with an initial uptime-monitor app containing a monitor service."

RUN cd /home/user && \
    encore app create uptime-monitor --lang=ts --platform=false && \
    mkdir -p /home/user/uptime-monitor/monitor && \
    cat > /home/user/uptime-monitor/monitor/encore.service.ts <<'EOF'
import { Service } from "encore.dev/service";
export default new Service("monitor");
EOF
RUN cat > /home/user/uptime-monitor/monitor/ping.ts <<'EOF'
import { api } from "encore.dev/api";

export const ping = api(
  { method: "GET", path: "/ping", expose: true },
  async (): Promise<{ message: string }> => {
    return { message: "pong" };
  }
);
EOF

# Container contents:
#   - curl ca-certificates git python3 python3-pip python3-pytest bash nodejs
#   - encore CLI installed
#   - /home/user/uptime-monitor: Encore app with monitor service and ping.ts

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
