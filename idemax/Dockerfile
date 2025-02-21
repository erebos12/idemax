# Use official Golang image as the build stage
FROM golang:1.20 as builder

# Set working directory inside the container
WORKDIR /app

# Copy go module files and download dependencies
COPY go.mod ./
RUN go mod tidy  # Ensures go.sum is generated

# Copy the rest of the source code
COPY . .

# Build the Go binary
RUN go build -o idempotency-service main.go

# Use a minimal image for production
FROM alpine:latest

# Install necessary certificates
RUN apk --no-cache add ca-certificates

# Set working directory
WORKDIR /root/

# Copy the built binary from the builder stage
COPY --from=builder /app/idempotency-service .

# Expose application port
EXPOSE 8080

# Start the application
CMD ["./idempotency-service"]
