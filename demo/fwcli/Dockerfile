FROM python:3.12

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
         curl \
         ca-certificates \
         sqlite3 \
         tzdata \
         unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV SCRIPT_DIR=/script
RUN mkdir ${SCRIPT_DIR} \
 && mkdir /wd
WORKDIR ${SCRIPT_DIR}

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy helper scripts as CLI tools
COPY demo/fwcli/center_lookup.py ./bin/center_lookup.py
COPY demo/fwcli/pipeline_lookup.py ./bin/pipeline_lookup.py
COPY demo/fwcli/entrypoint.sh .

# Install Flywheel CLI
RUN curl -o fw.zip https://storage.googleapis.com/flywheel-dist/cli/18.1.2/fw-linux_amd64-18.1.2.zip \
 && unzip fw.zip \
 && mv linux_amd64 bin/fw-cli \
 && chmod +x entrypoint.sh

# Create wrapper scripts so center_lookup and pipeline_lookup work as commands
RUN printf '#!/bin/bash\npython %s/bin/center_lookup.py "$@"\n' "${SCRIPT_DIR}" > ./bin/center_lookup \
 && printf '#!/bin/bash\npython %s/bin/pipeline_lookup.py "$@"\n' "${SCRIPT_DIR}" > ./bin/pipeline_lookup \
 && chmod +x ./bin/center_lookup ./bin/pipeline_lookup

ENV PATH="${PATH}:${SCRIPT_DIR}/bin:${SCRIPT_DIR}/bin/fw-cli"

ENTRYPOINT [ "./entrypoint.sh" ]
