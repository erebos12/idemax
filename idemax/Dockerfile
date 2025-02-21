# Stage 1: Build the Go binary
FROM golang:1.20 AS builder

# Set working directory inside the container
WORKDIR /app

# Ensure Go modules are enabled and correctly set
ENV GO111MODULE=on

# Copy go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod tidy

# Copy the entire source code
COPY . . 

# Build the Go application (rename the binary to avoid module conflict)
RUN CGO_ENABLED=0 GOOS=linux go build -o app main.go

# Stage 2: Create a minimal production container
FROM alpine:latest

# Install necessary dependencies
RUN apk --no-cache add ca-certificates bash

# Set working directory
WORKDIR /root/

# Set environment variables
ENV REDIS_HOST=redis:6379

# Copy the built Go binary from the builder stage (renamed to `app`)
COPY --from=builder /app/app /root/app

# Ensure correct permissions
RUN chmod +x /root/app

# Expose application port
EXPOSE 8080

# Set ENTRYPOINT instead of CMD
ENTRYPOINT ["/root/app"]
