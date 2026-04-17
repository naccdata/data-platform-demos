# Submission detail

This example is a Python script that looks up a specific submission by participant ID, date, and module, then displays visit metadata, a per-stage QC summary, and optionally exports the full error list to CSV.

It uses the `list_submissions`, `get_submission_qc_summary`, `get_submission_errors`, and `get_submission_visit_metadata` functions from the `nacc_common` package.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

## Usage

View the QC summary for a specific submission:

```bash
uv run demo/submission_detail/submission_detail.py --adcid 0 --ptid ABC123 --date 2025-03-15 -m UDS
```

Export errors to CSV (auto-generated filename):

```bash
uv run demo/submission_detail/submission_detail.py --adcid 0 --ptid ABC123 --date 2025-03-15 -m UDS -e
```

Export errors to a specific file:

```bash
uv run demo/submission_detail/submission_detail.py --adcid 0 --ptid ABC123 --date 2025-03-15 -m UDS -e my-errors.csv
```

Output as JSON (useful for scripting):

```bash
uv run demo/submission_detail/submission_detail.py --adcid 0 --ptid ABC123 --date 2025-03-15 -m UDS --json
```

## Output

By default the script prints a formatted summary to stdout:

```
--- Visit Metadata ---
  PTID:      ABC123
  NACCID:    NACC000001
  ADCID:     0
  Date:      2025-03-15
  Visit #:   1
  Module:    UDS
  Packet:    I

--- QC Summary (overall: FAIL) ---
  Stage                          Status       Errors
  ------------------------------ ------------ ------
  form-validator                 FAIL              3
  datastore-upload               PASS              0
```

With `--json`, the same data is printed as a JSON object.

With `-e`, errors are exported to CSV with columns for each error field plus a `stage` column indicating which pipeline stage produced the error.

## Options

| Flag | Description | Default |
|---|---|---|
| `-a`, `--adcid` | ADCID for your center (0-99) | required |
| `-t`, `--ptid` | Participant ID | required |
| `--date` | Visit date (YYYY-MM-DD) | required |
| `-m`, `--module` | Module name (UDS, LBD, FTLD, NP, etc.) | required |
| `-d`, `--datatype` | Datatype (dicom, enrollment, form) | form |
| `-p`, `--pipeline` | Pipeline type (ingest, sandbox) | sandbox |
| `-s`, `--studyid` | Study ID | adrc |
| `-e`, `--errors` | Export errors to CSV (optional path) | off |
| `--json` | Output summary as JSON | off |
| `-k`, `--api-key` | Flywheel API key | from env or keyring |

## Workflow

This script pairs well with `list_submissions.py`. A typical workflow:

1. Run `list_submissions.py` to see all submissions and their overall status
2. Pick a submission of interest (by ptid, date, module)
3. Run `submission_detail.py` to see the per-stage breakdown
4. Add `-e` to export the full error list for that submission
