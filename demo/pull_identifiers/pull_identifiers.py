"""Example script for querying identifiers from an enrollment pipeline on NACC
Data Platform."""

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project, get_published_view  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def main():
    """Pull participant identifiers from an enrollment pipeline on the NACC
    Data Platform."""
    parser = argparse.ArgumentParser(
        description="Pull enrollment identifiers for a study"
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
        help="output file path (default: center-identifiers-<date>.csv)",
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

    # 3. Get the dataview ID for participant identifiers.
    view_id = get_published_view(client=client, label="center-participant-identifers")

    # 4. Get the Flywheel group ID for the center by the ADCID.
    try:
        group_id = get_center_id(client=client, adcid=str(args.adcid))
    except CenterError as error:
        log.error(str(error))
        sys.exit(1)
    log.info("Group ID for ADCID %s is %s", args.adcid, group_id)

    # 5. Get the enrollment pipeline project.
    source_project = get_project(
        client=client,
        group_id=group_id,
        datatype="enrollment",
        pipeline_type=args.pipeline,
        study_id=args.studyid,
    )
    if not source_project:
        log.error("No enrollment project found for center: %s", group_id)
        sys.exit(1)

    log.info("Using project %s/%s", source_project.group, source_project.label)

    # 6. Save to a CSV file
    output_path = args.output or f"center-identifiers-{date.today()}.csv"
    client.save_view_data(
        view_id,
        source_project.id,
        output_path,
        format="csv",
    )


if __name__ == "__main__":
    main()
