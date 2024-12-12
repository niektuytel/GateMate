# Build stage: Compile the application service
FROM --platform=linux/arm64 golang:1.17-alpine3.14 AS builder

WORKDIR /temp

LABEL license="SPDX-License-Identifier: Apache-2.0"

# Install dependencies
RUN apk add --update --no-cache make git gcc libc-dev zeromq-dev libsodium-dev

# Copy Go module files and download dependencies
COPY go.mod .
COPY go.sum .
RUN go mod download

# Copy the application code and build the service
COPY . .
RUN go build -o ./app-influx-mqtt

# Final stage: Runtime container
FROM --platform=linux/arm64 alpine:3.14 AS final

# Install runtime dependencies
RUN apk add --update --no-cache zeromq

# Set up working directory
WORKDIR /

# Copy the built application binary and configuration resources
COPY --from=builder /temp/app-influx-mqtt /app-influx-mqtt
COPY ./res/ /res

# Expose the port used by the service
EXPOSE 59798

# Set environment variables required by the application
ENV EDGEX_SECURITY_SECRET_STORE=false

# Entry point for the container
ENTRYPOINT ["/app-influx-mqtt", "-cp=consul.http://edgex-core-consul:8500", "--registry", "--confdir=/res"]