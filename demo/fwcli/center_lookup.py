"""Script to lookup a center group by ADCID."""

import argparse
import logging
import sys
from pathlib import Path

# Allow importing the shared helper from demo/common/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))

from fw_auth import get_api_key  # noqa: E402
from nacc_common.center_info import get_center_id, CenterError  # noqa: E402
from flywheel import Client  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("__main__")


def main():
    """Lookup the FW group ID using the center ADCID."""
    parser = argparse.ArgumentParser(description="Lookup center group")
    parser.add_argument(
        "adcid",
        help="the ADCID for your center (0-99)",
        type=int,
        choices=range(0, 100),
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

    try:
        center_id = get_center_id(client=client, adcid=str(args.adcid))
    except CenterError as error:
        log.error(str(error))
        sys.exit(1)

    if center_id:
        print(center_id)


if __name__ == "__main__":
    main()
