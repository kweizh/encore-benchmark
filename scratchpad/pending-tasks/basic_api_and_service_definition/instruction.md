Encore uses logical service definitions and type-safe endpoints to automate routing and application architecture mapping.

You need to create a `greeter` service containing an `encore.service.ts` file and a GET endpoint at the path `/hello/:name` that returns `{ message: "Hello <name>" }` in an Encore TypeScript application. 

**Constraints:**
- You must explicitly define and export the service using `new Service("greeter")`.
- The endpoint must be configured to be publicly accessible using the `expose: true` property.