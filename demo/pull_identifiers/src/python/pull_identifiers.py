"""Example script for querying identifiers from an enrollment pipeline on NACC
Data Platform."""
import argparse
import logging
import os
import sys
from datetime import date

from center_info import get_center_id
from flywheel import Client
from pipeline import get_project, get_published_view

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('__main__')


def main():
    """Queries the enrollment pipeline dataviews available on the NACC Data
    Platform.

    Uses Flywheel instance determined by the API key value set in
    FW_API_KEY.
    """
    parser = argparse.ArgumentParser(
        description="Pull enrollment identifiers for a study")
    parser.add_argument('-a',
                        '--adcid',
                        help='the center group name',
                        type=int,
                        choices=range(0, 100),
                        required=True)
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

    # 3. Get the dataview ID for participant identifiers
    view_id = get_published_view(client=client,
                                 label='center-participant-identifers')

    # 4. Get the Flywheel group ID for the center by the ADCID.
    #    This hardcodes the NACC Sample Center, and will have to be changed
    group_id = get_center_id(client=client, adcid=str(args.adcid))
    log.info("Group ID for ADCID %s is %s", args.adcid, group_id)

    # 4. Get the enrollment form sandbox pipeline project
    #    Set the parameter pipeline_type='ingest' to upload center data.
    source_project = get_project(client=client,
                                 group_id=group_id,
                                 datatype='enrollment',
                                 pipeline_type=args.pipeline,
                                 study_id=args.studyid)
    if not source_project:
        log.error("No enrollment sandbox project found for center: %s",
                  group_id)
        sys.exit(1)

    log.info("Using project %s/%s", source_project.group, source_project.label)

    # 5. Save to a CSV file
    client.save_view_data(view_id,
                          source_project.id,
                          f'center-identifiers-{date.today()}.csv',
                          format='csv')


if __name__ == "__main__":
    main()
