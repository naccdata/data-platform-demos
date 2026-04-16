FROM python:3.12-slim

# 1. Copy the Pex file for the uploader.
COPY demo.python-uploader.src.python.uploader/bin.pex /bin/run

# 2. Create working directory to be mounted as working directory
RUN mkdir /wd
WORKDIR /wd

# 3. Set the Pex file as the entrypoint; defaults can be overridden at runtime
ENTRYPOINT ["/bin/run"]
CMD ["--adcid", "0", "--datatype", "form", "--pipeline", "sandbox", "form-data-dummyv1.csv"]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/python-uploader
#