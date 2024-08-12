"""Utilities for pulling error data attached to files."""
from typing import Any, Dict, List

from flywheel import Project


def build_rows(file_object: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Builds a list of error table rows from the file dictionary object.

    Flattens in gear name, and error locations.

    Args:
      file_object: the file dictionary
    """
    gear_names = {key for key in file_object['info']['qc'].keys()}
    table = []
    for gear_name in gear_names:
        for error in file_object['info']['qc'][gear_name]['validation'][
                'data']:
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
    project = project.reload()
    return [
        item for sl in [
            build_rows(file) for file in project.files
            if file.info.get('qc', None)
        ] for item in sl
    ]
