FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash wget && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://encore.dev/install.sh | bash
ENV PATH="/root/.encore/bin:$PATH"

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore application with a circular dependency between order and user services."

RUN cd /home/user && \
    encore app create myproject --lang=ts && \
    cd myproject && \
    mkdir -p order user && \
    cat >order/order.ts <<'EOF'
import { api } from "encore.dev/api";
import { getUserName } from "../user/user";

export const getOrder = api(
  { method: "GET", path: "/order/:id", expose: true },
  async ({ id }: { id: string }) => {
    const userName = await getUserName(id);
    return { orderId: id, user: userName };
  }
);

export async function getOrderInfo(id: string): Promise<string> {
    return "Order" + id;
}
EOF
RUN cd /home/user/myproject && \
    cat >user/user.ts <<'EOF'
import { api } from "encore.dev/api";
import { getOrderInfo } from "../order/order";

export const getUser = api(
  { method: "GET", path: "/user/:id", expose: true },
  async ({ id }: { id: string }) => {
    const orderInfo = await getOrderInfo(id);
    return { userId: id, order: orderInfo };
  }
);

export async function getUserName(id: string): Promise<string> {
    return "User" + id;
}
EOF

# Container contents:
#   - Encore installed in /root/.encore/bin/encore
#   - Node.js v24 for TypeScript support
#   - /home/user/myproject - Encore project with circular dependency between order and user services.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
