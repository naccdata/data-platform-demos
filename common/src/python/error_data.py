"""Utilities for pulling error data attached to files."""

from typing import Any, Callable, Dict, List, Literal, Optional

from flywheel import FileOutput, Project

ERROR_HEADER_NAMES = [
    "type",
    "ptid",
    "visitnum",
    "code",
    "line",
    "column_name",
    "key_path",
    "id",
    "name",
    "gear",
    "container_id",
    "flywheel_path",
    "value",
    "expected",
    "message",
    "timestamp",
]

STATUS_HEADER_NAMES = ["name", "id", "gear", "status"]


def qc_data(file_object: FileOutput) -> Dict[str, Any]:
    """Returns the QC object in the metadata for the file.

    Args:
      file_object: the file metadata
    Returns:
      the dictionary for info.qc if non-empty. Otherwise, the empty dictionary.
    """
    return file_object.get("info", {}).get("qc", {})


def validation_data(qc_object: Dict[str, Any], gear_name: str) -> Dict[str, Any]:
    """Returns the validation object in the QC metadata for the named gear.

    Args:
      qc_object: the QC metadata (file.info.qc)
      gear_name: the name of the gear
    """
    return qc_object.get(gear_name, {}).get("validation", {})


def error_data(qc_object: Dict[str, Any], gear_name: str) -> Dict[str, Any]:
    """Returns the error object in the QC metadata.

    Args:
      qc_object: the QC metadata (file.info.qc)
      gear_name: the name of the gear
    Returns:
      the dictionary for gear_name.validation.data if exists.
      Otherwise, the empty dictionary.
    """
    return validation_data(qc_object=qc_object, gear_name=gear_name).get("data", {})


def status_data(
    qc_object: Dict[str, Any], gear_name: str
) -> Optional[Literal["pass", "fail"]]:
    """Returns the QC status in the QC metadata.

    Args:
      qc_object: the QC metadata (file.info.qc)
      gear_name: the name of the gear
    Returns:
      the QC status for the gear if set. None, otherwise.
    """
    status = validation_data(qc_object=qc_object, gear_name=gear_name).get("state")
    if status is None:
        return None
    if status.lower() == "pass":
        return "pass"
    if status.lower() == "fail":
        return "fail"

    return None


def build_qc_rows(
    file_object: FileOutput,
    insert_row: Callable[[Dict[str, Any], str, List[Dict[str, Any]]], None],
) -> List[Dict[str, Any]]:
    qc_object = qc_data(file_object)
    gear_names = set(qc_object.keys())
    table: List[Dict[str, Any]] = []
    for gear_name in gear_names:
        insert_row(qc_object, gear_name, table)
    return table


def build_error_rows(file_object: FileOutput) -> List[Dict[str, Any]]:
    """Builds a list of error table rows from the file dictionary object.

    Flattens in gear name, and error locations.

    Args:
      file_object: the file dictionary
    """

    def insert_error_row(
        qc_object: Dict[str, Any], gear_name: str, table: List[Dict[str, Any]]
    ) -> None:
        for error in error_data(qc_object, gear_name):
            loc: Dict[str, Any] = error.pop("location", {})  # type: ignore
            if loc:
                error.update(loc)  # type: ignore
            table.append(
                {
                    "name": file_object.name,
                    "id": file_object.id,
                    "gear": gear_name,
                    **error,
                }
            )

    return build_qc_rows(file_object, insert_error_row)


def build_status_rows(file_object: FileOutput) -> List[Dict[str, Any]]:
    def insert_status_row(
        qc_object: Dict[str, Any], gear_name: str, table: List[Dict[str, Any]]
    ) -> None:
        table.append(
            {
                "name": file_object.name,
                "id": file_object.id,
                "gear": gear_name,
                "status": status_data(qc_object, gear_name),
            }
        )

    return build_qc_rows(file_object, insert_status_row)


def get_qc_data(
    project: Project, row_builder: Callable[[FileOutput], List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    project_object: Project = project.reload()
    return [
        item
        for sl in [
            row_builder(file)
            for file in project_object.files
            if file.info.get("qc", None)
        ]
        for item in sl
    ]


def get_error_data(project: Project) -> List[Dict[str, Any]]:
    """Creates a list of dictionaries, each corresponding to an error in a file
    in the project.

    Args:
      project: the flywheel project object
    """
    return get_qc_data(project, build_error_rows)


def get_status_data(project: Project) -> List[Dict[str, Any]]:
    return get_qc_data(project, build_status_rows)
