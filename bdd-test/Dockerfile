# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y wget

# Install Dockerize (useful for waiting on services)
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Create a virtual environment inside /app/venv
RUN python -m venv /app/venv

# Ensure Python and Pip use the virtual environment (NO NEED TO SOURCE)
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip inside the virtual environment
RUN pip install --upgrade pip

# Install py-bdd-test from PyPI inside the virtual environment
RUN pip install --no-cache-dir py-bdd-test==1.0.14

# Debugging: List package contents
RUN ls -rtl /app/venv/lib/python3.11/site-packages/py_bdd_test/features/steps/*.py

# Copy feature files
COPY features /app/venv/lib/python3.11/site-packages/py_bdd_test/features
COPY behave.ini /app/behave.ini

# This script should be executed from outside the container to run the tests
COPY execute_tests.sh /app/execute_tests.sh

