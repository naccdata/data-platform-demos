"""Helper for resolving the Flywheel API key.

Priority order:
  1. Explicit value passed via --api-key flag
  2. FW_API_KEY environment variable (including .env via python-dotenv)
  3. OS keyring (macOS Keychain, Windows Credential Locker, etc.)
  4. Interactive prompt (stores the key in the keyring for next time)
"""

import getpass
import logging
import os
import sys

from dotenv import load_dotenv

log = logging.getLogger(__name__)

KEYRING_SERVICE = "nacc-data-platform"
KEYRING_USERNAME = "fw-api-key"


def get_api_key(cli_value: str | None = None) -> str:
    """Return the Flywheel API key, or exit if none can be found.

    Args:
        cli_value: Value passed via a CLI flag (highest priority).
    """
    # 1. Explicit CLI flag
    if cli_value:
        return cli_value

    # 2. Environment variable (load .env first)
    load_dotenv()
    env_key = os.environ.get("FW_API_KEY")
    if env_key:
        return env_key

    # 3. OS keyring
    try:
        import keyring

        stored = keyring.get_password(KEYRING_SERVICE, KEYRING_USERNAME)
        if stored:
            log.info("Using API key from system keyring")
            return stored
    except Exception:  # noqa: BLE001
        # keyring may not be available (e.g. headless Docker)
        pass

    # 4. Interactive prompt → store in keyring for next time
    if not sys.stdin.isatty():
        log.error(
            "FW_API_KEY not found. Set it via --api-key, environment variable, "
            "or run interactively to be prompted."
        )
        sys.exit(1)

    key = getpass.getpass("Enter your Flywheel API key: ")
    if not key:
        log.error("No API key provided")
        sys.exit(1)

    try:
        import keyring

        keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, key)
        log.info("API key stored in system keyring for future use")
    except Exception:  # noqa: BLE001
        log.warning("Could not store key in keyring; you will be prompted again")

    return key
