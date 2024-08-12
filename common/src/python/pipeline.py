"""Implements utilities for data pipelines in NACC Data Platform."""
import logging
from typing import Literal

from flywheel import Client

log = logging.getLogger('__main__')


def get_project(client: Client,
                group_id: str,
                datatype: Literal['form', 'enrollment', 'dicom'] = 'form',
                pipeline_type: Literal['ingest', 'sandbox'] = 'sandbox',
                study_id: str = 'adrc'):
    """Look up the project for a given center, study, and datatype.

    Args:
        group_id (str): The group ID of the center.
        datatype (str): The datatype to look up.
        pipeline_type (str): The type of the pipeline.
        study_id (str): The study ID for the project.
    Returns:
        Project: The project for the given center, study, and datatype.
    """
    suffix = f"-{study_id}" if study_id != 'adrc' else ''
    project_label = f"{pipeline_type}-{datatype}{suffix}"
    project = client.lookup(f"{group_id}/{project_label}")
    if not project:
        log.error("Failed to find project %s", project_label)

    return project


def get_published_view(client: Client, label: str) -> str:
    """Return the view ID for the published dataview.

    Args:
      client: the Flywheel SDK client
      label: the label for the dataview to return
    Returns:
      the ID for the dataview
    """
    metadata_project = client.lookup("nacc/metadata")
    views = client.get_views(metadata_project.id, filter=f"label={label}")
    return views[0].id
