"""Utilities for getting center information from NACC Data Platform."""
import logging
from typing import Optional

from flywheel import Client

log = logging.getLogger('__main__')


def get_center_id(client: Client, adcid: str) -> Optional[str]:
    """Look up the center group ID for a given ADCID.

    Args:
        adcid (str): The ADCID of the center.

    Returns:
        Optional[str]: The group ID of the center, or None if not found.
    """
    metadata = client.lookup("nacc/metadata")
    if not metadata:
        log.error("Failed to find nacc/metadata project")
    metadata = metadata.reload()
    if 'centers' not in metadata.info:
        log.error("No 'centers' key in nacc/metadata")
        return None

    if adcid not in metadata.info['centers']:
        log.error("No center with ADCID %s in nacc/metadata", adcid)
        return None

    return metadata.info['centers'][str(adcid)]['group']
