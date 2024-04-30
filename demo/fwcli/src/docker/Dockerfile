FROM python:3.11

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
         curl \
         ca-certificates \
         sqlite3 \
         tzdata \
         unzip

ENV SCRIPT_DIR=/script
RUN mkdir ${SCRIPT_DIR} \
 && mkdir /wd
WORKDIR ${SCRIPT_DIR}

COPY demo/fwcli/src/docker/entrypoint.sh .

RUN curl -o fw.zip https://storage.googleapis.com/flywheel-dist/cli/18.1.2/fw-linux_amd64-18.1.2.zip \
 && unzip fw.zip \
 && mv linux_amd64 bin \
 && chmod +x entrypoint.sh

COPY demo.fwcli.src.python.center_script/bin.pex ./bin/center_lookup
COPY demo.fwcli.src.python.pipeline_script/bin.pex ./bin/pipeline_lookup

ENV PATH="${PATH}:${SCRIPT_DIR}/bin"

ENTRYPOINT [ "./entrypoint.sh" ]