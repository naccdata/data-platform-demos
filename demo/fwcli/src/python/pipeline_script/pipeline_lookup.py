"""Script to look up pipeline for data submission."""
import argparse
import logging
import os
import sys

from flywheel import Client
from pipeline import get_project

log = logging.getLogger('__main__')


def main():
    """Look up pipeline based on command line argument values."""
    parser = argparse.ArgumentParser(
        description="Lookup pipeline project label")
    parser.add_argument('-c',
                        '--center',
                        help='the center group name',
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

    if 'FW_API_KEY' not in os.environ:
        log.error("environment variable FW_API_KEY not found")
        sys.exit(1)

    client = Client(os.environ['FW_API_KEY'])
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    project = get_project(client=client,
                          group_id=args.center,
                          datatype=args.datatype,
                          pipeline_type=args.pipeline,
                          study_id=args.studyid)
    if project:
        print(project.label)


if __name__ == "__main__":
    main()
