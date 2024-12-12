# https://github.com/edgexfoundry/app-functions-sdk-go/blob/main/app-service-template/Dockerfile

#build stage
FROM --platform=linux/arm64 golang:1.23-alpine3.20 AS builder

RUN apk add --update --no-cache make git gcc libc-dev zeromq-dev libsodium-dev
WORKDIR /

COPY go.mod .
RUN go mod download

COPY . .
ARG MAKE="make build"
RUN $MAKE

#final stage
FROM alpine:3.14
# TODO: Change Copyright to your company if open sourcing or remove label
LABEL license='SPDX-License-Identifier: Apache-2.0' copyright='Copyright (c) 2022: Intel'
LABEL Name=gatemate-app-influx-mqtt Version=3.1_arm64

# dumb-init is required as security-bootstrapper uses it in the entrypoint script
RUN apk add --update --no-cache ca-certificates dumb-init zeromq
# Ensure using latest versions of all installed packages to avoid any recent CVEs
RUN apk --no-cache upgrade

COPY ./res/ /res
ENV EDGEX_SECURITY_SECRET_STORE=false

# TODO: set this port appropriatly as it is in the configuation.yaml
EXPOSE 1337

ENTRYPOINT ["/gatemate-app-influx-mqtt"]
CMD ["-cp=keeper.http://edgex-core-keeper:59890", "--registry", "--confdir=/res"]