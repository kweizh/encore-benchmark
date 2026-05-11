When automating Encore builds in headless CI/CD environments, the CLI does not automatically pick up authentication tokens from standard environment variables without explicit commands.

You need to write a shell script (`build.sh`) that explicitly authenticates the Encore CLI using a pre-authentication key and subsequently builds a Docker image tagged `my-app:latest` in a CI/CD pipeline. 

**Constraints:**
- The script must manually pass the `ENCORE_AUTH_KEY` environment variable to the `encore auth login` command using the appropriate flag.
- The script must check for the presence of the `ENCORE_AUTH_KEY` environment variable and exit with an error code if it is not set.