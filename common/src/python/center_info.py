from typing import Optional


def get_center_id(fw: Client, adcid: int) -> Optional[str]:
    """
    Looks up the center group ID for a given ADCID.
    
    Args:
        adcid (int): The ADCID of the center.
    
    Returns:
        Optional[str]: The group ID of the center, or None if not found.
    """
    metadata = fw.lookup("nacc/metadata")
    if not metadata:
        log.error("Failed to find nacc/metadata project")
    metadata = metadata.reload()
    if 'centers' not in metadata.info:
        log.error("No 'centers' key in nacc/metadata")
        return None
    
    if str(adcid) not in metadata.info['centers']:
        log.error("No center with ADCID %s in nacc/metadata", adcid)
        return None

    return metadata.info['centers'][str(adcid)]['group']