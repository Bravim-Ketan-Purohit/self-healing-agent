# Base sandbox image for the self-healing agent.
# Pre-installs pytest so containers can run tests with network_mode=none.
FROM python:3.12-slim

# Install only the minimal test runner
RUN pip install --no-cache-dir pytest==8.4.0 && \
    rm -rf /root/.cache

# Create non-root user
RUN groupadd -g 10001 sandbox && \
    useradd -u 10001 -g 10001 -m -s /bin/sh sandbox

# Create work directory
RUN mkdir -p /work && chown 10001:10001 /work

USER 10001:10001
WORKDIR /work
