# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y wget

# Create a virtual environment inside /app/venv
RUN python -m venv /app/venv

# Ensure Python and Pip use the virtual environment (NO NEED TO SOURCE)
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip inside the virtual environment
RUN pip install --upgrade pip

# Install py-bdd-test from PyPI inside the virtual environment
RUN pip install colorama py-bdd-test==1.0.29

# Debugging: List package contents
RUN ls -rtl /app/venv/lib/python3.11/site-packages/py_bdd_test/features/steps/*.py

# Copy feature files
COPY features /app/venv/lib/python3.11/site-packages/py_bdd_test/features
COPY behave.ini /app/behave.ini
COPY wait_for_service.py /app/wait_for_service.py

# This script should be executed from outside the container to run the tests
COPY execute_tests.sh /app/execute_tests.sh

