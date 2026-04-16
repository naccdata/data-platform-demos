"""Example uploader script for submitting forms to NACC Data Platform."""

import argparse
import logging
import os
import sys
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def main():
    """Upload a file to the NACC Data Platform."""
    parser = argparse.ArgumentParser(description="Upload file")
    parser.add_argument(
        "-a",
        "--adcid",
        help="the ADCID for your center (0-99)",
        type=int,
        choices=range(0, 100),
        required=True,
    )
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
    parser.add_argument("filepath", help="the path to the file to upload")
    parser.add_argument(
        "-k", "--api-key", help="Flywheel API key (default: from env or keyring)"
    )
    args = parser.parse_args()

    # 1. Get the API key (CLI flag > env var > keyring > prompt)
    api_key = get_api_key(args.api_key)

    # 2. Create the Client object using the API key.
    client = Client(api_key)
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    # 3. Get the Flywheel group ID for the center by the ADCID.
    try:
        group_id = get_center_id(client=client, adcid=str(args.adcid))
    except CenterError as error:
        log.error(str(error))
        sys.exit(1)
    log.info("Group ID for ADCID %s is %s", args.adcid, group_id)

    # 4. Get the pipeline project.
    upload_project = get_project(
        client=client,
        group_id=group_id,
        datatype=args.datatype,
        pipeline_type=args.pipeline,
        study_id=args.studyid,
    )
    if not upload_project:
        log.error("No project found for center: %s", group_id)
        sys.exit(1)

    log.info("Using project %s/%s", upload_project.group, upload_project.label)

    # 5. Upload the file.
    if not os.path.exists(args.filepath):
        log.error("no file found: %s", args.filepath)
        sys.exit(1)

    if not os.path.getsize(args.filepath) > 0:
        log.error("file %s is empty", args.filepath)
        sys.exit(1)

    response = upload_project.upload_file(args.filepath)
    log.info("uploaded file %s: %s bytes", args.filepath, response[0]["size"])


if __name__ == "__main__":
    main()
