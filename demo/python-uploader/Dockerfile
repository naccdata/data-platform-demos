FROM python:3.12-slim

# 1. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# 2. Copy the uploader script and shared helper
COPY demo/common/fw_auth.py /app/demo/common/fw_auth.py
COPY demo/python-uploader/uploader.py /app/demo/python-uploader/uploader.py

# 3. Create working directory to be mounted
RUN mkdir /wd
WORKDIR /wd

# 4. Set the script as the entrypoint; defaults can be overridden at runtime
ENTRYPOINT ["python", "/app/demo/python-uploader/uploader.py"]
CMD ["--adcid", "0", "--datatype", "form", "--pipeline", "sandbox", "form-data-dummyv1.csv"]

# NOTE: to run a shell in the container, you have to override the entrypoint
# at the command line:
#
# docker run -it --entrypoint /bin/bash naccdata/python-uploader
#
