FROM python:3.12-slim

# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends r-base r-base-dev \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /wd

ENV SCRIPT_DIR=/script
RUN mkdir ${SCRIPT_DIR}
WORKDIR ${SCRIPT_DIR}

# Install Python dependencies and R reticulate package
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && R -e "install.packages(c('reticulate'))"

COPY demo/r-uploader/uploader.R .

ENTRYPOINT [ "R", "-e", "source('/script/uploader.R')" ]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/r-uploader
#
