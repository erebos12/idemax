# Use the official Golang image as a builder
FROM golang:1.20 as builder

# Set the working directory
WORKDIR /app

# Copy go modules files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application
RUN go build -o idemax main.go

# Use a minimal base image for deployment
FROM alpine:latest

# Install ca-certificates
RUN apk --no-cache add ca-certificates

# Set working directory
WORKDIR /root/

# Copy the built binary
COPY --from=builder /app/idemax .

# Expose application port
EXPOSE 8080

# Ensure correct permissions
RUN chmod +x idemax

# Run the application
CMD ["./idemax"]
