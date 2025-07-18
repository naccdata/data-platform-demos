"""Script to lookup a center group by ADCID."""

import argparse
import logging
import os
import sys

from nacc_common.center_info import get_center_id, CenterError
from flywheel import Client

log = logging.getLogger("__main__")


def main():
    """Lookup the FW group ID using the center ADCID."""
    parser = argparse.ArgumentParser(description="Lookup center group")
    parser.add_argument(
        "adcid", help="the center group name", type=int, choices=range(0, 100)
    )
    args = parser.parse_args()

    if "FW_API_KEY" not in os.environ:
        log.error("environment variable FW_API_KEY not found")
        sys.exit(1)

    client = Client(os.environ["FW_API_KEY"])
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    try:
        center_id = get_center_id(client=client, adcid=str(args.adcid))
    except CenterError as error:
        log.error(str(error))
        sys.exit(1)

    if center_id:
        print(center_id)


if __name__ == "__main__":
    main()
