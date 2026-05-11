# Encore.dev Benchmark Research
Encore is a backend development platform designed to simplify building distributed systems by treating infrastructure as a logical part of the application code. It uses static analysis to automatically provision infrastructure (databases, Pub/Sub, etc.) on AWS, GCP, or Encore Cloud.
### 1. Library Overview
*   **Description**: Encore is an "Infrastructure-from-Code" framework for TypeScript and Go. It allows developers to define backend primitives (APIs, Databases, Cron Jobs, Pub/Sub) as regular code, while the platform handles the underlying cloud infrastructure, observability (tracing, logging), and CI/CD.
*   **Ecosystem Role**: It sits between a traditional framework (like Express or Gin) and a PaaS/IaC tool (like Heroku or Terraform), automating the "plumbing" of microservices.
*   **Project Setup**:
    1.  Install CLI: `curl -L https://encore.dev/install.sh | bash`
    2.  Create App: `encore app create <app-name> --lang=typescript` (or `--lang=go`)
    3.  Run Locally: `encore run` (Requires Docker for local databases).
    4.  Deploy: `git push encore` or `encore build docker <image-tag>`.
### 2. Core Primitives & APIs
*   **Services**: Defined by a directory containing an `encore.service.ts` file.    ```typescript
    import { Service } from "encore.dev/service";
    export default new Service("my-service");
    ```
*   **APIs**: Type-safe endpoints with automatic routing and validation.
    ```typescript
    import { api } from "encore.dev/api";
    export const myEndpoint = api(
      { method: "GET", path: "/hello/:name", expose: true },
      async ({ name }: { name: string }) => ({ message: `Hello ${name}` })
    );
    ```
*   **Databases**: PostgreSQL databases defined as logical resources.
    ```typescript
    import { SQLDatabase } from "encore.dev/storage/sqldb";
    const db = new SQLDatabase("todo", { migrations: "./migrations" });
    // Usage: await db.query`SELECT * FROM items`;
    ```
*   **Pub/Sub**: Cloud-agnostic asynchronous messaging.
    ```typescript
    import { Topic, Subscription } from "encore.dev/pubsub";
    export const myTopic = new Topic<{id: string}>("my-topic", { deliveryGuarantee: "at-least-once" });
    const _ = new Subscription(myTopic, "my-sub", { handler: async (event) => { ... } });
    ```
*   **Cron Jobs**: Scheduled tasks.
    ```typescript
    import { CronJob } from "encore.dev/cron";
    const _ = new CronJob("cleanup", { every: "1h", endpoint: cleanupApi });
    ```
### 3. Real-World Use Cases & Templates
*   **SaaS Starter**: [Next.js + Encore + Clerk + Stripe](https://encore.dev/templates/saas-starter).
*   **Uptime Monitor**: [Event-driven system using Cron and Pub/Sub](https://encore.dev/templates/eda).
*   **URL Shortener**: [REST API with PostgreSQL](https://encore.dev/templates/url-shortener).
*   **AI Integration**: [MCP Server for AI agents](https://encore.dev/docs/ts/cli/mcp).
### 4. Developer Friction Points
*   **Docker Dependency**: Local development requires Docker for databases. If Docker is not running, `encore run` will fail.
*   **Migration Naming**: Database migrations must follow strict naming: `1_name.up.sql`, `2_name.up.sql`. Skipping numbers or incorrect suffixes causes failures.
*   **Circular Dependencies**: Because Encore uses static analysis to map the architecture, circular dependencies between services (Service A calling Service B which calls Service A) are generally disallowed or tricky to manage.
*   **Auth Key Management**: In CI/CD, the CLI does not automatically pick up an environment variable for authentication. It requires an explicit `encore auth login --auth-key=$ENCORE_AUTH_KEY`.
### 5. Evaluation Ideas
*   **Simple**: Create a "Hello World" service with a single GET endpoint and a corresponding test case.
*   **Intermediate**: Build a URL shortener where the "shorten" API saves to a database and the "redirect" API increments a click counter via a Pub/Sub event to a separate "analytics" service.
*   **Intermediate**: Implement a custom `authHandler` that validates a JWT and restricts access to a "profile" endpoint.
*   **Complex**: Build an Uptime Monitor that uses a Cron Job to ping URLs, saves results to a database, and publishes a "Down" event to a Topic if a site is unreachable, which is then handled by an "Alerting" service.
*   **Complex**: Implement a file processing pipeline where a "Raw" endpoint receives an image, saves it to Object Storage, and triggers a background job (via Pub/Sub) to generate a thumbnail.
### 6. Cloud Platform Auth & Env Vars
To automate interactions with the Encore Cloud Platform (e.g., in a benchmark or CI/CD), use the following environment variables:
*   **`ENCORE_AUTH_KEY`**: The Pre-authentication key generated in **App Settings > Auth Keys**.
    *   *Usage*: `encore auth login --auth-key=$ENCORE_AUTH_KEY`
*   **`ENCORE_APP_ID`**: The unique ID of your Encore application.
    *   *Usage*: Required for API calls to `https://api.encore.cloud/api/apps/$ENCORE_APP_ID/...`
*   **`ENCORE_CLIENT_ID` & `ENCORE_CLIENT_SECRET`**: For programmatic access via OAuth.
    *   *Usage*: Used to obtain a Bearer token from `POST https://api.encore.cloud/api/oauth/token`.
### 7. Sources
1.  [Encore llms.txt](https://encore.dev/llms.txt) - Structured overview of all documentation.
2.  [Encore Quick Start](https://encore.dev/docs/ts/quick-start) - Basic setup and workflow.
3.  [SQL Databases Guide](https://encore.dev/docs/ts/primitives/databases) - Database definition and migration rules.
4.  [Auth Keys Documentation](https://encore.dev/docs/platform/integrations/auth-keys) - CLI authentication for non-interactive environments.
5.  [CI/CD Integration Guide](https://encore.dev/docs/go/self-host/ci-cd) - Standard patterns for automating Encore builds.
6.  [CLI Reference](https://encore.dev/docs/ts/cli/cli-reference) - Full list of commands and flags.
7.  [API Reference](https://encore.dev/docs/platform/integrations/api-reference) - Details on platform API and OAuth authentication.