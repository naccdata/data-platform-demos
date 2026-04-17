"""Example script for listing submissions and their QC status from a pipeline
project on NACC Data Platform."""

import argparse
import logging
import sys
from csv import DictWriter
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

import filter_helpers  # noqa: E402
from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from nacc_common.error_data import list_submissions  # noqa: E402
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")

HEADER_NAMES = ["ptid", "date", "module", "overall_status"]


def main():
    """List submissions and their QC status from a pipeline project."""
    parser = argparse.ArgumentParser(
        description="List submissions and QC status for a pipeline project"
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
        help="output file path (default: submissions-<project>-<date>.csv)",
        default=None,
    )
    parser.add_argument(
        "-k", "--api-key", help="Flywheel API key (default: from env or keyring)"
    )
    filter_helpers.add_filter_args(parser)
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

    # 5. Collect filter sets
    module_set = filter_helpers.collect_modules(args.module)
    ptid_set = filter_helpers.collect_ptids(args.ptid)
    filter_helpers.log_active_filters(module_set, ptid_set, log)

    # 6. List submissions from project
    submissions_kwargs: dict[str, object] = {}
    if module_set is not None:
        submissions_kwargs["modules"] = module_set
    if ptid_set is not None:
        submissions_kwargs["ptids"] = ptid_set
    table = list_submissions(source_project, **submissions_kwargs)  # type: ignore[arg-type]

    if not table:
        log.info("no submissions in project %s", source_project.label)
        return

    log.info("found %d submission(s)", len(table))

    # 7. Strip internal identifier and write output
    rows = [{k: row[k] for k in HEADER_NAMES if k in row} for row in table]

    output_path = args.output or filter_helpers.build_output_filename(
        "submissions", source_project.label, module_set, ptid_set
    )
    with open(output_path, mode="w", encoding="utf-8") as out_file:
        writer = DictWriter(out_file, fieldnames=HEADER_NAMES, dialect="unix")
        writer.writeheader()
        writer.writerows(rows)

    log.info("wrote %d row(s) to %s", len(rows), output_path)


if __name__ == "__main__":
    main()
