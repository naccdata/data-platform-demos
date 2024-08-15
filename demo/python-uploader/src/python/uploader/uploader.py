"""Example uploader script for submitting forms to NACC Data Platform."""
import argparse
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
    """Upload a file to the NACC Data Platform.

    Uses Flywheel instance determined by the API key value set in
    FW_API_KEY.
    """
    # 0. The argument parser is used to allow running the script from the
    #    command line.
    parser = argparse.ArgumentParser(description="Upload file")
    parser.add_argument('-a',
                        '--adcid',
                        help='the center group name',
                        type=int,
                        choices=range(0, 100),
                        required=True)
    parser.add_argument('-d',
                        '--datatype',
                        choices=['dicom', 'enrollment', 'form'],
                        help='the datatype name (default: form)',
                        default='form')
    parser.add_argument('-p',
                        '--pipeline',
                        choices=['ingest', 'sandbox'],
                        help='the pipeline type (default: sandbox)',
                        default='sandbox')
    parser.add_argument('-s',
                        '--studyid',
                        help='the study ID (default: adrc)',
                        default='adrc')
    parser.add_argument('filepath', help='the path to the file to upload')
    args = parser.parse_args()

    # 1. The Flywheel SDK uses a Client object to interact with Flywheel.
    #    First get the API key from the environment variable FW_API_KEY
    if 'FW_API_KEY' not in os.environ:
        log.error("environment variable FW_API_KEY not found")
        sys.exit(1)

    # 2. Create the Client object using the API key.
    #    The key determines which instance you are using.
    client = Client(os.environ['FW_API_KEY'])
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    # 3. Get the Flywheel group ID for the center by the ADCID.
    group_id = get_center_id(client=client, adcid=str(args.adcid))
    log.info("Group ID for ADCID %s is %s", args.adcid, group_id)

    # 4. Get the form sandbox pipeline project
    #    The default behavior is to upload to a testing sandbox for form data.
    #    Set the parameter pipeline_type='ingest' to upload center data.
    upload_project = get_project(client=client,
                                 group_id=group_id,
                                 datatype=args.datatype,
                                 pipeline_type=args.pipeline,
                                 study_id=args.studyid)
    if not upload_project:
        log.error("No form sandbox project found for center: %s", group_id)
        sys.exit(1)

    log.info("Using project %s/%s", upload_project.group, upload_project.label)

    # 5. Upload the file.
    #    This script assumes it is run in an environment with a directory /wd,
    #    which is set within the Dockerfile.
    if not os.path.exists(args.filepath):
        log.error("no file found: %s", args.filepath)
        sys.exit(1)

    if not os.path.getsize(args.filepath) > 0:
        log.error("file %s is empty", args.filepath)
        sys.exit(1)

    response = upload_project.upload_file(args.filepath)
    log.info("uploaded file %s: %s bytes", args.filepath, response[0]['size'])


if __name__ == "__main__":
    main()
