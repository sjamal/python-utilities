# Roadmap

Planned utility functions and helper modules. These are building blocks intended for reuse across other Python projects in this ecosystem.

---

## In Progress

_Nothing currently active._

---

## Planned

### File & I/O Helpers

- [ ] **file_utils.py** — Common file operations: safe read/write with encoding detection, atomic writes (write-then-rename), directory tree walker, and checksum verification (MD5/SHA256).
- [ ] **archive_utils.py** — Compress and decompress tar/gz/zip archives with progress reporting. Supports rotating archives by date suffix.
- [ ] **config_loader.py** — Load and merge configuration from YAML, JSON, or `.env` files with environment variable override support. Validates required keys on load.

### Data Helpers

- [ ] **type_coercer.py** — Attempt safe type coercion for DataFrame columns (strings → int/float/datetime) with configurable fallback behaviour and a coercion report.
- [ ] **outlier_utils.py** — IQR and Z-score based outlier detection functions returning boolean masks. Reusable across data-processing and ML repos.
- [ ] **chunked_reader.py** — Read large CSV/JSON files in configurable chunks with optional progress bar. Yields DataFrames for downstream processing.

### System & Environment

- [ ] **env_validator.py** — Check that required environment variables are set and non-empty. Prints a clear failure message listing missing vars. Useful in CI/CD scripts and pipelines.
- [ ] **retry_decorator.py** — Configurable `@retry` decorator with exponential backoff and jitter. Supports whitelisting specific exceptions.
- [ ] **timer_decorator.py** — `@timed` decorator that logs function name and elapsed time. Configurable log level and output format.
- [ ] **process_runner.py** — Thin wrapper around `subprocess` for running shell commands from Python: captures stdout/stderr, raises on non-zero exit, optional timeout.

### Reporting

- [ ] **report_builder.py** — Build structured plaintext or Markdown reports from a dict of sections. Handles headers, tables (from lists of dicts), and code blocks.
- [ ] **table_formatter.py** — Format a list of dicts as an aligned plaintext table or Markdown table. Configurable column widths and alignment.
- [ ] **logger_setup.py** — Standard logging configuration: console + rotating file handler, configurable level, consistent format across all projects.

### Date & Time

- [ ] **date_utils.py** — Common date helpers: parse ambiguous date strings, compute business days between dates, generate date range lists, convert between timezones.

---

## Ideas / Backlog

- Secrets loader that pulls from Azure Key Vault or environment with a unified interface
- Pagination helper for REST API clients (handles `next` link traversal)
- Diff reporter for comparing two dicts/DataFrames with a human-readable summary

---

## Notes

- All utilities should have no side effects and be importable without configuration.
- Each module should be independently usable — no cross-module dependencies within this repo.
- Include docstrings and at least one usage example per function.
