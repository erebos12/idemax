# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies & create a virtual environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    && python -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install colorama py-bdd-test==1.0.29 \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Set the environment path for the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy required application files
COPY features /app/venv/lib/python3.11/site-packages/py_bdd_test/features
COPY behave.ini wait_for_service.py execute_tests.sh /app/

# Ensure the test execution script is executable
RUN chmod +x /app/execute_tests.sh
