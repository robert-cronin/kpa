# Copyright (c) 2024 Robert Cronin
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# ================ BUILD STAGE ================
FROM golang:1.22 as builder

ARG TARGETARCH

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=$TARGETARCH go build -a -installsuffix cgo -o kpa .

# ================= KUBECTL STAGE =================
FROM alpine:latest as kubectl

ARG TARGETARCH
ARG KUBECTL_VERSION=v1.28.2

RUN apk add --no-cache curl

RUN curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl" && \
    curl -LO "https://dl.k8s.io/${KUBECTL_VERSION}/bin/linux/${TARGETARCH}/kubectl.sha256" && \
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum -c && \
    chmod +x kubectl

# ================ RUN STAGE ================
FROM alpine:latest

ARG TARGETARCH

RUN apk add --no-cache ca-certificates

WORKDIR /root/

COPY --from=builder /app/kpa .
COPY --from=kubectl /kubectl /usr/local/bin/

CMD ["./kpa"]