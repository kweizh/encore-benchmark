FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.encore/bin:$PATH"

RUN curl -L https://encore.dev/install.sh | bash

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Encore TypeScript project with invalid database migration names."

RUN cd /home/user && \
    encore app create myproject --example=ts/url-shortener && \
    cd myproject && \
    mkdir -p todo/migrations && \
    echo "CREATE TABLE items (id BIGSERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT false);" > todo/migrations/1_init.sql && \
    echo "INSERT INTO items (title) VALUES ('Learn Encore');" > todo/migrations/3_seed.up.sql && \
    echo "import { api } from 'encore.dev/api';\nimport { SQLDatabase } from 'encore.dev/storage/sqldb';\n\nconst db = new SQLDatabase('todo', { migrations: './migrations' });\n\nexport const getItems = api(\n  { method: 'GET', path: '/items', expose: true },\n  async () => {\n    const rows = await db.query\`SELECT * FROM items\`;\n    return { items: rows };\n  }\n);" > todo/todo.ts

# Container contents:
#   - curl wget ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24
#   - Encore CLI
#   - /home/user/myproject: Encore TS project with an incorrectly named migration file (1_init.sql and 3_seed.up.sql)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
