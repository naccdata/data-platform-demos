"""Example uploader script for submitting forms to NACC Data Platform."""
import logging
import os
import sys

from center_info import get_center_id
from flywheel import Client
from pipeline import get_project

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('__main__')


def main():
    """Upload a file to the NADD Data Platform.

    Uses Flywheel instance determined by the API key value set in
    FW_API_KEY.
    """

    # 1. The Flywheel SDK uses a Client object to interact with Flywheel.
    #    First get the API key from the environment variable FW_API_KEY
    if 'FW_API_KEY' not in os.environ:
        log.error("environment variable FW_API_KEY not found")
        sys.exit(1)

    # 2. Create the Client object using the API key.
    #    The key determines which instance you are using.
    client = Client(os.environ['FW_API_KEY'])

    # 3. Get the Flywheel group ID for the center by the ADCID.
    #    This hardcodes the NACC Sample Center, and will have to be changed
    group_id = get_center_id(client=client, adcid=0)
    log.info("Group ID for ADCID 0 is %s", group_id)

    # 4. Get the form sandbox pipeline project
    #    The default behavior is to upload to a testing sandbox for form data.
    #    Set the parameter pipeline_type='ingest' to upload center data.
    upload_project = get_project(client=client, group_id=group_id)
    if not upload_project:
        log.error("No form sandbox project found for center: %s", group_id)
        sys.exit(1)

    log.info("Using project %s/%s", upload_project.group, upload_project.label)

    # 5. Upload the file.
    #    This script assumes it is run in an environment with a directory /wd,
    #    which is set within the Dockerfile.
    filename = "form-data.csv"
    file_path = f"/wd/{filename}"

    if not os.path.exists(file_path):
        log.error("no file found: %s", filename)
        sys.exit(1)

    if not os.path.getsize(file_path) > 0:
        log.error("file %s is empty", filename)
        sys.exit(1)

    response = upload_project.upload_file(file_path)
    log.info("uploaded file %s: %s bytes", filename, response[0]['size'])


if __name__ == "__main__":
    main()
