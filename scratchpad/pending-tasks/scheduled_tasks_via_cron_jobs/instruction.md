Encore simplifies backend orchestration by natively supporting scheduled tasks mapped directly to API endpoints.

You need to define a `cleanup` Cron Job that executes every hour and triggers an internal `cleanupApi` endpoint to simulate deleting expired data in a background process. 

**Constraints:**
- Use the `CronJob` class from `encore.dev/cron` with the schedule configuration set to `every: "1h"`.
- The `cleanupApi` endpoint mapped to the Cron Job must be kept private and MUST NOT be exposed to the public internet.