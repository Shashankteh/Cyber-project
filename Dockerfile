# Stage 1: Build the Go application
FROM golang:alpine AS builder

RUN apk add build-base
COPY . /src
WORKDIR /src/cmd/WatchYourLAN/
RUN CGO_ENABLED=0 go build -o /app/WatchYourLAN .

# Stage 2: Set up the final container with both the Go and Python applications
FROM python:3.9-slim

# Install dependencies for Python and other tools
WORKDIR /app

# Copy the Go binary from the builder stage
COPY --from=builder /app/WatchYourLAN /app/

# Copy the Python application files
COPY arp-scan /app/arp-scan

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/arp-scan/requriements.txt

# Install arp-scan and other necessary tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends arp-scan && \
    rm -rf /var/lib/apt/lists/*

# Expose necessary ports for the applications
EXPOSE 3000

# Run both applications
CMD ["sh", "-c", "./WatchYourLAN & python /app/arp-scan/app.py"]
