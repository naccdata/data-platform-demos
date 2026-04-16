"""Example script for pulling QC status from a pipeline project on NACC Data
Platform."""

import argparse
import logging
import sys
from csv import DictWriter
from datetime import date
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from nacc_common.error_data import STATUS_HEADER_NAMES, get_status_data  # noqa: E402
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def main():
    """Pull QC status from a pipeline project on the NACC Data Platform."""
    parser = argparse.ArgumentParser(
        description="Pull QC status for pipeline project"
    )
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
    parser.add_argument(
        "-o",
        "--output",
        help="output file path (default: qc-status-<project>-<date>.csv)",
        default=None,
    )
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

    # 4. Get the pipeline project
    source_project = get_project(
        client=client,
        group_id=group_id,
        datatype=args.datatype,
        pipeline_type=args.pipeline,
        study_id=args.studyid,
    )
    if not source_project:
        log.error("No project found for center: %s", group_id)
        sys.exit(1)

    log.info("Using project %s/%s", source_project.group, source_project.label)

    # 5. Get QC status from project
    table = get_status_data(source_project)
    if not table:
        log.info("no status data in project %s", source_project.label)
        return

    # 6. Format data
    output_path = (
        args.output or f"qc-status-{source_project.label}-{date.today()}.csv"
    )
    with open(output_path, mode="w", encoding="utf-8") as out_file:
        writer = DictWriter(out_file, fieldnames=STATUS_HEADER_NAMES, dialect="unix")
        writer.writeheader()
        writer.writerows(table)


if __name__ == "__main__":
    main()
