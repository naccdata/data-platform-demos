"""Utilities for pulling error data attached to files."""
from typing import Any, Dict, List

from flywheel import Project


def qc_data(file_object: Dict[str, Any]) -> Dict[str, Any]:
    """Returns the QC object in the metadata for the file.

    Args:
      file_object: the file metadata
    Returns:
      the dictionary for info.qc if non-empty. Otherwise, the empty dictionary.
    """
    return file_object.get('info', {}).get('qc', {})


def error_data(qc_object: Dict[str, Any], gear_name: str) -> Dict[str, Any]:
    """Returns the error object in the QC metadata.

    Args:
      qc_object: the QC metadata (file.qc)
      gear_name: the name of the gear
    Returns:
      the dictionary for gear_name.validation.data if exists.
      Otherwise, the empty dictionary.
    """
    return qc_object.get(gear_name, {}).get('validation', {}).get('data', {})


def build_rows(file_object: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Builds a list of error table rows from the file dictionary object.

    Flattens in gear name, and error locations.

    Args:
      file_object: the file dictionary
    """
    qc_object = qc_data(file_object)
    gear_names = set(qc_object.keys())
    table = []
    for gear_name in gear_names:
        for error in error_data(qc_object, gear_name):
            loc = error.pop('location', {})
            if loc:
                error.update(loc)
            table.append({
                'name': file_object.name,
                'id': file_object.id,
                'gear': gear_name,
                **error
            })
    return table


def get_error_data(project: Project) -> List[Dict[str, Any]]:
    """Creates a list of dictionaries, each corresponding to an error in a file
    in the project.

    Args:
      project: the flywheel project object
    """
    project: Project = project.reload()
    return [
        item for sl in [
            build_rows(file) for file in project.files
            if file.info.get('qc', None)
        ] for item in sl
    ]
