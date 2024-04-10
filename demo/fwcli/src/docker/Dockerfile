FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
         curl \
         ca-certificates \
         unzip

 ENV SCRIPT_DIR=/script
 RUN mkdir ${SCRIPT_DIR}
 WORKDIR ${SCRIPT_DIR}

RUN curl -o fw.zip https://storage.googleapis.com/flywheel-dist/cli/17.8.2/fw-linux_amd64-17.8.2.zip \
 && unzip fw.zip \
 && mv linux_amd64 bin

ENV PATH="${PATH}:${SCRIPT_DIR}/bin"

RUN mkdir /wd
WORKDIR /wd

ENTRYPOINT [ "fw", "ingest", "folder", "--group", "sample-center", "--project", "sandbox-form", "/wd" ]