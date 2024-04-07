FROM python:3.11 as demo-base

# create directories within container
# /script is where the package lives
ENV SCRIPT_DIR=/script
WORKDIR ${SCRIPT_DIR}

# install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy script into container
COPY ./uploader .

# create working directory to be mounted as working directory
RUN mkdir /wd
WORKDIR /wd

# run script by default
ENTRYPOINT [ "python3", "/script/uploader.py" ]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/upload-demo
#