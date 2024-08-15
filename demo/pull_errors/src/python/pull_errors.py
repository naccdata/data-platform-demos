"""Example script for querying identifiers from an enrollment pipeline on NACC
Data Platform."""
import argparse
import logging
import os
import sys
from csv import DictWriter
from datetime import date

from center_info import get_center_id
from error_data import get_error_data
from flywheel import Client
from pipeline import get_project

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('__main__')


def main():
    """Queries the enrollment pipeline dataviews available on the NACC Data
    Platform.

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

    # 4. Get the pipeline project
    source_project = get_project(client=client,
                                 group_id=group_id,
                                 datatype=args.datatype,
                                 pipeline_type=args.pipeline,
                                 study_id=args.studyid)
    if not source_project:
        log.error("No enrollment sandbox project found for center: %s",
                  group_id)
        sys.exit(1)

    log.info("Using project %s/%s", source_project.group, source_project.label)

    # 5. Collect error data from project
    table = get_error_data(source_project)

    if not table:
        log.info("no errors in project %s", source_project)
        return

    # 6. Format data
    header_names = list(table[0].keys())
    with open(f'errors-{source_project.label}-{date.today()}.csv',
              mode='w',
              encoding='utf-8') as out_file:
        writer = DictWriter(out_file, fieldnames=header_names)
        writer.writeheader()
        writer.writerows(table)


if __name__ == "__main__":
    main()
