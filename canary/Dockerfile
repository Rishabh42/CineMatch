FROM alpine:latest

# Install any necessary dependencies
RUN apk update && \
    apk add --no-cache curl jq

# Copy the application folder inside the container
COPY ../app /app

# Copy the script into the container
COPY deploy.sh /usr/local/bin/deploy.sh

# Set execute permissions on the script
RUN chmod +x /usr/local/bin/deploy.sh

# Set the entry point to execute the script after 12 hours
CMD ["/usr/local/bin/deploy.sh"]
