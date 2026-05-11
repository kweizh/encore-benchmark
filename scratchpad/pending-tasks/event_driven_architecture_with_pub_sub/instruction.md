Encore avoids tight coupling and circular dependencies between microservices by utilizing cloud-agnostic Pub/Sub messaging primitives.

You need to create a `clicks` Topic to handle asynchronous messaging and write a Subscription in a separate analytics service that triggers when a `redirect` API publishes a `ClickEvent`. 

**Constraints:**
- The `clicks` Topic must be strictly configured with an `at-least-once` delivery guarantee.
- You MUST structure the imports so that the analytics service imports the Topic from the redirect service, ensuring no circular dependencies are created between the two services.