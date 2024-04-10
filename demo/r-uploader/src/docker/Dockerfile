FROM python:3.11 as builder

ENV BUILD_DIR=/build
RUN mkdir ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

COPY nacc_common-0.0.1-py3-none-any.whl ./wheels

###
FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends r-base r-base-dev \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /wd

ENV SCRIPT_DIR=/script
RUN mkdir ${SCRIPT_DIR}
WORKDIR ${SCRIPT_DIR}

COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

RUN pip install --no-cache /wheels/*

RUN R -e "install.packages(c('reticulate'))"

COPY demo/r-uploader/src/r/uploader/uploader.R .

ENTRYPOINT [ "R", "-e", "source('/script/uploader.R')" ]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/r-uploader
#