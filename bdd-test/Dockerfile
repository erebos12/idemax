# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies (optional)
RUN apt-get update && apt-get install -y curl unzip wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# Copy only the feature files into the container
COPY features/ /app/features/
COPY execute_tests.sh /app/execute_tests.sh

# Install pip and virtual environment tools
RUN python -m pip install --upgrade pip

# Install py-bdd-test from PyPI
RUN pip install py-bdd-test

# Set the default command to run behave tests
CMD ["behave", "--format=pretty"]
