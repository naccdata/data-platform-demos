FROM python:3.11

# 1. Copy the Pex file for the uploader.
COPY demo.python-uploader.src.python.uploader/bin.pex /bin/run

# 2. Create working directory to be mounted as working directory
RUN mkdir /wd
WORKDIR /wd

# 3. Set the the Pex file to be run by default
ENTRYPOINT [ "python3", "/bin/run" ]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/python-uploader
#