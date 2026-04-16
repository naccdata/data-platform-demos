"""Unit tests for demo/common/filter_helpers.py."""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

# Add demo/common to sys.path so we can import filter_helpers directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "demo" / "common"))

import filter_helpers  # noqa: E402


# ---------------------------------------------------------------------------
# add_filter_args: short aliases
# ---------------------------------------------------------------------------


def test_short_alias_m_for_module() -> None:
    """The -m short alias is accepted for --module.

    Validates: Requirements 1.5, 1.6
    """
    parser = argparse.ArgumentParser()
    filter_helpers.add_filter_args(parser)
    args = parser.parse_args(["-m", "UDS"])
    assert args.module == ["UDS"]


def test_short_alias_t_for_ptid() -> None:
    """The -t short alias is accepted for --ptid.

    Validates: Requirements 4.5, 4.6
    """
    parser = argparse.ArgumentParser()
    filter_helpers.add_filter_args(parser)
    args = parser.parse_args(["-t", "PT001"])
    assert args.ptid == ["PT001"]


# ---------------------------------------------------------------------------
# log_active_filters
# ---------------------------------------------------------------------------


def test_log_active_filters_modules(caplog: logging.LogRecord) -> None:
    """Active module filters are logged at INFO level.

    Validates: Requirements 6.1, 6.3
    """
    logger = logging.getLogger("test.modules")
    with caplog.at_level(logging.INFO, logger="test.modules"):
        filter_helpers.log_active_filters({"UDS", "LBD"}, None, logger)
    assert any("Filtering by modules" in r.message for r in caplog.records)
    info_records = [r for r in caplog.records if "Filtering by modules" in r.message]
    assert all(r.levelno == logging.INFO for r in info_records)


def test_log_active_filters_ptids(caplog: logging.LogRecord) -> None:
    """Active PTID filters are logged at INFO level.

    Validates: Requirements 6.2, 6.4
    """
    logger = logging.getLogger("test.ptids")
    with caplog.at_level(logging.INFO, logger="test.ptids"):
        filter_helpers.log_active_filters(None, {"PT001", "PT002"}, logger)
    assert any("Filtering by PTIDs" in r.message for r in caplog.records)
    info_records = [r for r in caplog.records if "Filtering by PTIDs" in r.message]
    assert all(r.levelno == logging.INFO for r in info_records)


def test_log_active_filters_none(caplog: logging.LogRecord) -> None:
    """No log output is produced when no filters are active."""
    logger = logging.getLogger("test.none")
    with caplog.at_level(logging.DEBUG, logger="test.none"):
        filter_helpers.log_active_filters(None, None, logger)
    assert len(caplog.records) == 0


# ---------------------------------------------------------------------------
# build_output_filename — no filters
# ---------------------------------------------------------------------------


def test_build_output_filename_no_filters() -> None:
    """With no filters the filename is <prefix>-<label>-<date>.csv.

    Validates: Requirements 7.5, 7.6
    """
    today = str(date.today())
    result = filter_helpers.build_output_filename("errors", "my-project", None, None)
    assert result == f"errors-my-project-{today}.csv"


# ---------------------------------------------------------------------------
# collect_modules / collect_ptids — empty/whitespace input
# ---------------------------------------------------------------------------


def test_collect_modules_empty_input() -> None:
    """collect_modules returns None for empty or whitespace-only input."""
    assert filter_helpers.collect_modules(None) is None
    assert filter_helpers.collect_modules([]) is None
    assert filter_helpers.collect_modules([""]) is None
    assert filter_helpers.collect_modules(["  ", " , , "]) is None


def test_collect_ptids_empty_input() -> None:
    """collect_ptids returns None for empty or whitespace-only input."""
    assert filter_helpers.collect_ptids(None) is None
    assert filter_helpers.collect_ptids([]) is None
    assert filter_helpers.collect_ptids([""]) is None
    assert filter_helpers.collect_ptids(["  ", " , , "]) is None


# ---------------------------------------------------------------------------
# filter_by_ptids — records missing the ptid key
# ---------------------------------------------------------------------------


def test_filter_by_ptids_excludes_records_missing_ptid_key() -> None:
    """Records without a 'ptid' key are excluded when a PTID filter is active."""
    records = [
        {"ptid": "PT001", "module": "UDS"},
        {"module": "LBD"},  # no ptid key
        {"ptid": "PT002", "module": "NP"},
    ]
    result = filter_helpers.filter_by_ptids(records, {"PT001", "PT002"})
    assert result == [
        {"ptid": "PT001", "module": "UDS"},
        {"ptid": "PT002", "module": "NP"},
    ]
