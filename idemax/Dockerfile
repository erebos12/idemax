# Stage 1: Build the Go binary
FROM golang:1.20 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build the Go application (statically linked for Alpine)
RUN CGO_ENABLED=0 GOOS=linux go build -o idemax main.go

# Stage 2: Create a minimal production container
FROM alpine:latest

# Install necessary dependencies
RUN apk --no-cache add ca-certificates bash

# Set working directory
WORKDIR /root/

ENV REDIS_HOST=redis:6379


# Copy the built Go binary from the builder stage
COPY --from=builder /app/idemax /root/idemax

# Ensure correct permissions
RUN chmod +x /root/idemax

# Expose application port
EXPOSE 8080

# Set ENTRYPOINT instead of CMD
ENTRYPOINT ["/root/idemax"]
