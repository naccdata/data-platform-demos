# Listing submissions

This example is a Python script that uses the `error_data.list_submissions` function from the `nacc_common` package to list all submissions in a pipeline project along with their overall QC status.

Follow the steps in the [top-level README](../../README.md#setting-up-demo-environment) for getting started.

## Usage

List all submissions for a center:

```bash
uv run demo/list_submissions/list_submissions.py --adcid 0
```

Filter by module:

```bash
uv run demo/list_submissions/list_submissions.py --adcid 0 -m UDS
```

Filter by participant ID:

```bash
uv run demo/list_submissions/list_submissions.py --adcid 0 -t ABC123
```

Combine filters and specify output file:

```bash
uv run demo/list_submissions/list_submissions.py --adcid 0 -m UDS -t ABC123 -o my-submissions.csv
```

## Output

The script writes a CSV file with the following columns:

| Column | Description |
|---|---|
| `ptid` | Participant ID |
| `date` | Visit/submission date |
| `module` | Module name (UDS, LBD, FTLD, NP, etc.) |
| `overall_status` | Overall QC status (PASS, FAIL, or IN REVIEW) |

## Options

| Flag | Description | Default |
|---|---|---|
| `-a`, `--adcid` | ADCID for your center (0-99) | required |
| `-d`, `--datatype` | Datatype (dicom, enrollment, form) | form |
| `-p`, `--pipeline` | Pipeline type (ingest, sandbox) | sandbox |
| `-s`, `--studyid` | Study ID | adrc |
| `-m`, `--module` | Module filter (comma-separated, repeatable) | all |
| `-t`, `--ptid` | PTID filter (comma-separated, repeatable) | all |
| `-o`, `--output` | Output file path | auto-generated |
| `-k`, `--api-key` | Flywheel API key | from env or keyring |
