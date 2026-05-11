Encore automatically provisions PostgreSQL databases defined as logical resources, but it relies heavily on static analysis and strict file naming conventions for database migrations.

You need to define a `todo` database using `SQLDatabase` and write the initial SQL migration file to create an `items` table in your Encore project. 

**Constraints:**
- The migration file MUST strictly follow Encore's sequential naming convention (e.g., `1_init.up.sql`) to prevent static analysis failures.
- The database instance must be instantiated correctly, pointing to the specific migrations directory (e.g., `{ migrations: "./migrations" }`).