"""Property-based tests for demo/common/filter_helpers.py.

Tests Properties 3 and 4 from the filter-errors-status design document.
"""

from __future__ import annotations

import sys
from datetime import date

# Make the shared helper module importable
sys.path.insert(0, "demo/common")

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from filter_helpers import build_output_filename, filter_by_ptids

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Strategy for record dicts with a "ptid" key
_ptid_value = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Pd")),
    min_size=1,
    max_size=12,
)

_record = st.fixed_dictionaries({"ptid": _ptid_value})

_records_list = st.lists(_record, max_size=30)

_optional_ptid_set = st.one_of(
    st.none(),
    st.frozensets(_ptid_value, min_size=1, max_size=10).map(set),
)

# Strategy for filename segments – printable, no hyphens (to avoid ambiguity
# when verifying hyphen-joined segments inside the filename)
_name_char = st.characters(
    whitelist_categories=("L", "N"),
    min_codepoint=65,
    max_codepoint=122,
)

_simple_name = st.text(alphabet=_name_char, min_size=1, max_size=8)

_optional_module_set = st.one_of(
    st.none(),
    st.frozensets(_simple_name.map(str.upper), min_size=1, max_size=5).map(set),
)

_optional_ptid_set_for_filename = st.one_of(
    st.none(),
    st.frozensets(_simple_name, min_size=1, max_size=5).map(set),
)


# ---------------------------------------------------------------------------
# Property 3: PTID post-filter retains exactly the matching records
# ---------------------------------------------------------------------------


@settings(max_examples=100)
@given(records=_records_list, ptids=_optional_ptid_set)
def test_filter_by_ptids_retains_matching_records(
    records: list[dict[str, str]],
    ptids: set[str] | None,
) -> None:
    """**Validates: Requirements 5.1, 5.2, 5.3, 5.4**

    When ptids is None the full list is returned unchanged.
    When ptids is a set, only records whose 'ptid' value is in the set are
    returned, and they appear in the original order.
    """
    result = filter_by_ptids(records, ptids)

    if ptids is None:
        # Requirement 5.3 / 5.4 — all records retained
        assert result == records
    else:
        # Requirement 5.1 / 5.2 — exactly matching records, in order
        expected = [r for r in records if r.get("ptid") in ptids]
        assert result == expected

        # Every returned record has a matching ptid
        for r in result:
            assert r["ptid"] in ptids

        # Order is preserved — indices in original list are monotonically increasing
        if result:
            indices = [records.index(r) for r in result]
            assert indices == sorted(indices)


# ---------------------------------------------------------------------------
# Property 4: Output filename includes sorted filter segments
# ---------------------------------------------------------------------------


@settings(max_examples=100)
@given(
    prefix=_simple_name,
    project_label=_simple_name,
    modules=_optional_module_set,
    ptids=_optional_ptid_set_for_filename,
)
def test_build_output_filename_includes_filter_segments(
    prefix: str,
    project_label: str,
    modules: set[str] | None,
    ptids: set[str] | None,
) -> None:
    """**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

    - Module names appear sorted and hyphen-joined in the filename.
    - PTID values appear sorted, hyphen-joined, prefixed with "ptid-".
    - When both are None the filename is <prefix>-<label>-<date>.csv.
    - The filename always ends with .csv.
    """
    filename = build_output_filename(prefix, project_label, modules, ptids)

    # Always ends with .csv
    assert filename.endswith(".csv")

    # Today's date always appears
    today = str(date.today())
    assert today in filename

    # Prefix is the first segment
    assert filename.startswith(prefix + "-")

    if modules is not None:
        # Sorted module names appear as a hyphen-joined segment
        sorted_modules = sorted(modules)
        module_segment = "-".join(sorted_modules)
        assert module_segment in filename

    if ptids is not None:
        # Sorted PTIDs appear as a "ptid-<sorted-hyphen-joined>" segment
        sorted_ptids = sorted(ptids)
        ptid_segment = "ptid-" + "-".join(sorted_ptids)
        assert ptid_segment in filename

    if modules is None and ptids is None:
        # No filter segments — simple pattern
        expected = f"{prefix}-{project_label}-{today}.csv"
        assert filename == expected
