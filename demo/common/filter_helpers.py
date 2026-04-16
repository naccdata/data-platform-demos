"""Shared helpers for --module and --ptid CLI filtering."""

from __future__ import annotations

import argparse
import logging
from datetime import date
from typing import Any

log = logging.getLogger(__name__)


def add_filter_args(parser: argparse.ArgumentParser) -> None:
    """Add --module/-m and --ptid/-t arguments to an argparse parser.

    Both flags accept comma-separated values and can be repeated.
    """
    parser.add_argument(
        "-m",
        "--module",
        action="append",
        default=None,
        help="module name(s) to filter by (comma-separated, repeatable)",
    )
    parser.add_argument(
        "-t",
        "--ptid",
        action="append",
        default=None,
        help="participant ID(s) to filter by (comma-separated, repeatable)",
    )


def collect_modules(raw: list[str] | None) -> set[str] | None:
    """Parse and normalize module names to uppercase.

    Returns None when no modules were requested (meaning 'all modules').
    """
    if not raw:
        return None
    modules: set[str] = set()
    for entry in raw:
        for name in entry.split(","):
            stripped = name.strip()
            if stripped:
                modules.add(stripped.upper())
    return modules or None


def collect_ptids(raw: list[str] | None) -> set[str] | None:
    """Parse PTID values (case-sensitive).

    Returns None when no PTIDs were requested (meaning 'all PTIDs').
    """
    if not raw:
        return None
    ptids: set[str] = set()
    for entry in raw:
        for ptid in entry.split(","):
            stripped = ptid.strip()
            if stripped:
                ptids.add(stripped)
    return ptids or None


def log_active_filters(
    modules: set[str] | None,
    ptids: set[str] | None,
    logger: logging.Logger,
) -> None:
    """Log active filter values at INFO level."""
    if modules:
        logger.info("Filtering by modules: %s", ", ".join(sorted(modules)))
    if ptids:
        logger.info("Filtering by PTIDs: %s", ", ".join(sorted(ptids)))


def filter_by_ptids(
    records: list[dict[str, Any]],
    ptids: set[str] | None,
) -> list[dict[str, Any]]:
    """Post-filter records by PTID.

    Returns all records when ptids is None.
    """
    if ptids is None:
        return records
    return [r for r in records if r.get("ptid") in ptids]


def build_output_filename(
    prefix: str,
    project_label: str,
    modules: set[str] | None,
    ptids: set[str] | None,
) -> str:
    """Build a default output filename reflecting active filters.

    Pattern: <prefix>[-<modules>][-ptid-<ptids>]-<project_label>-<date>.csv
    Module and PTID segments are sorted and hyphen-joined.
    """
    parts: list[str] = [prefix]
    if modules:
        parts.append("-".join(sorted(modules)))
    if ptids:
        parts.append("ptid-" + "-".join(sorted(ptids)))
    parts.append(project_label)
    parts.append(str(date.today()))
    return "-".join(parts) + ".csv"
