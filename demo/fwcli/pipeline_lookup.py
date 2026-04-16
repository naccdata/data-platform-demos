"""Script to look up pipeline for data submission."""

import argparse
import logging
import sys
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def main():
    """Look up pipeline based on command line argument values."""
    parser = argparse.ArgumentParser(description="Lookup pipeline project label")
    parser.add_argument("-c", "--center", help="the center group name", required=True)
    parser.add_argument(
        "-d",
        "--datatype",
        choices=["dicom", "enrollment", "form"],
        help="the datatype name (default: form)",
        default="form",
    )
    parser.add_argument(
        "-p",
        "--pipeline",
        choices=["ingest", "sandbox"],
        help="the pipeline type (default: sandbox)",
        default="sandbox",
    )
    parser.add_argument(
        "-s", "--studyid", help="the study ID (default: adrc)", default="adrc"
    )
    parser.add_argument(
        "-k", "--api-key", help="Flywheel API key (default: from env or keyring)"
    )
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)

    client = Client(api_key)
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    project = get_project(
        client=client,
        group_id=args.center,
        datatype=args.datatype,
        pipeline_type=args.pipeline,
        study_id=args.studyid,
    )
    if project:
        print(project.label)


if __name__ == "__main__":
    main()
