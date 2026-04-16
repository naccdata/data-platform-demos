FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

USER root
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && rm -f /usr/share/keyrings/yarn.gpg \
    && apt-get update
