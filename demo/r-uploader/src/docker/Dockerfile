FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends r-base=4.2 r-base-dev=4.2 \
 && rm -rf /var/lib/apt/lists/*
