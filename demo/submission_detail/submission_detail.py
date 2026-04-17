"""Example script for viewing QC details of a specific submission on NACC Data
Platform.

Looks up a submission by participant ID, date, and module, then displays
visit metadata, per-stage QC summary, and optionally the full error list.
"""

import argparse
import json
import logging
import sys
from csv import DictWriter
from pathlib import Path
from typing import Any, Optional

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from nacc_common.error_data import (  # noqa: E402
    get_submission_errors,
    get_submission_qc_summary,
    get_submission_visit_metadata,
    list_submissions,
)
from flywheel import Client  # noqa: E402
from nacc_common.pipeline import get_project  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def resolve_identifier(
    project: Any,
    ptid: str,
    visit_date: str,
    module: str,
) -> Optional[str]:
    """Resolve a submission identifier from ptid, date, and module.

    Args:
        project: the Flywheel project
        ptid: participant ID
        visit_date: visit date (YYYY-MM-DD)
        module: module name

    Returns:
        the opaque submission identifier, or None if not found
    """
    submissions = list_submissions(
        project,
        modules={module.upper()},
        ptids={ptid},
    )

    matches = [s for s in submissions if s.get("date") == visit_date]

    if len(matches) == 0:
        return None

    if len(matches) > 1:
        log.warning(
            "multiple submissions match ptid=%s date=%s module=%s:",
            ptid,
            visit_date,
            module,
        )
        for match in matches:
            log.warning(
                "  %s / %s / %s — %s",
                match["ptid"],
                match["date"],
                match["module"],
                match.get("overall_status", "unknown"),
            )
        log.warning("using the first match")

    return matches[0]["identifier"]


def print_summary(
    visit_metadata: Optional[dict[str, Any]],
    qc_summary: Optional[dict[str, Any]],
) -> None:
    """Print visit metadata and QC summary to stdout."""
    if visit_metadata:
        print("\n--- Visit Metadata ---")
        print(f"  PTID:      {visit_metadata.get('ptid', 'N/A')}")
        print(f"  NACCID:    {visit_metadata.get('naccid', 'N/A')}")
        print(f"  ADCID:     {visit_metadata.get('adcid', 'N/A')}")
        print(f"  Date:      {visit_metadata.get('date', 'N/A')}")
        print(f"  Visit #:   {visit_metadata.get('visitnum', 'N/A')}")
        print(f"  Module:    {visit_metadata.get('module', 'N/A')}")
        print(f"  Packet:    {visit_metadata.get('packet', 'N/A')}")

    if qc_summary:
        print(f"\n--- QC Summary (overall: {qc_summary['overall_status']}) ---")
        print(f"  {'Stage':<30} {'Status':<12} {'Errors':>6}")
        print(f"  {'-' * 30} {'-' * 12} {'-' * 6}")
        for stage_name, stage_info in qc_summary.get("stages", {}).items():
            print(
                f"  {stage_name:<30} {stage_info['status']:<12} "
                f"{stage_info['error_count']:>6}"
            )
    print()


def main():
    """View QC details for a specific submission on the NACC Data Platform."""
    parser = argparse.ArgumentParser(
        description="View QC details for a specific submission"
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
        "-t",
        "--ptid",
        help="participant ID",
        required=True,
    )
    parser.add_argument(
        "--date",
        help="visit date (YYYY-MM-DD)",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--module",
        help="module name (e.g. UDS, LBD, FTLD, NP)",
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
        "-e",
        "--errors",
        help="output file path for errors CSV (omit to skip error export)",
        default=None,
        nargs="?",
        const="auto",
    )
    parser.add_argument(
        "--json",
        help="output summary as JSON instead of formatted text",
        action="store_true",
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

    # 5. Resolve the submission identifier from ptid + date + module
    identifier = resolve_identifier(
        source_project, args.ptid, args.date, args.module
    )
    if identifier is None:
        log.error(
            "no submission found for ptid=%s date=%s module=%s",
            args.ptid,
            args.date,
            args.module,
        )
        sys.exit(1)

    # 6. Fetch visit metadata and QC summary
    visit_metadata = get_submission_visit_metadata(source_project, identifier)
    qc_summary = get_submission_qc_summary(source_project, identifier)

    if args.json:
        output = {
            "visit_metadata": visit_metadata,
            "qc_summary": qc_summary,
        }
        print(json.dumps(output, indent=2))
    else:
        print_summary(visit_metadata, qc_summary)

    # 7. Optionally export errors to CSV
    if args.errors is not None:
        errors = get_submission_errors(source_project, identifier)
        if not errors:
            log.info("no errors for this submission")
            return

        if args.errors == "auto":
            error_path = (
                f"submission-errors-{args.ptid}-{args.date}-"
                f"{args.module.upper()}.csv"
            )
        else:
            error_path = args.errors

        fieldnames = list(errors[0].keys())
        with open(error_path, mode="w", encoding="utf-8") as out_file:
            writer = DictWriter(out_file, fieldnames=fieldnames, dialect="unix")
            writer.writeheader()
            writer.writerows(errors)

        log.info("wrote %d error(s) to %s", len(errors), error_path)


if __name__ == "__main__":
    main()
