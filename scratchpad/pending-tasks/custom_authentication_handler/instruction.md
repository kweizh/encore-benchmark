Securing endpoints in Encore requires utilizing a centralized authentication handler to intercept and validate requests before they reach the API logic.

You need to implement a custom `authHandler` that reads a Bearer token from the `Authorization` header and use it to restrict access to a private `GET /profile` endpoint in the application. 

**Constraints:**
- The `GET /profile` endpoint must not use `expose: true` in a way that bypasses authentication.
- If the token is missing or invalid, the handler must reject the request rather than passing undefined user data to the endpoint.