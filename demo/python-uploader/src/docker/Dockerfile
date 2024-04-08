FROM python:3.11 as demo-base

# 1. Create a directories within container for the script
# /script is where the package lives
ENV SCRIPT_DIR=/script
WORKDIR ${SCRIPT_DIR}

# 2. Copy the Pex file for the uploader.
COPY demo.python-uploader.src.python.uploader/bin.pex /bin/run

# 3. Create working directory to be mounted as working directory
RUN mkdir /wd
WORKDIR /wd

# 4. Set the the Pex file to be run by default
ENTRYPOINT [ "python3", "/bin/run" ]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/upload-demo
#