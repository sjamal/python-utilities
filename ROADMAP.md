# Roadmap

Planned utility functions and helper modules. These are building blocks intended for reuse across other Python projects in this ecosystem.

---

## In Progress

_Nothing currently active._

---

## Completed

### File & I/O Helpers

- [x] **file_utils.py** — Common file operations: safe read/write with encoding detection, atomic writes (write-then-rename), directory tree walker, and checksum verification (MD5/SHA256).
- [x] **config_loader.py** — Load and merge configuration from YAML, JSON, or `.env` files with environment variable override support. Validates required keys on load.

### System & Environment

- [x] **env_validator.py** — Check that required environment variables are set and non-empty. Prints a clear failure message listing missing vars. Useful in CI/CD scripts and pipelines.
- [x] **retry_decorator.py** — Configurable `@retry` decorator with exponential backoff and jitter. Supports whitelisting specific exceptions.
- [x] **logger_setup.py** — Standard logging configuration: console + rotating file handler, configurable level, consistent format across all projects.

---

## Planned

### File & I/O Helpers

- [ ] **archive_utils.py** — Compress and decompress tar/gz/zip archives with progress reporting. Supports rotating archives by date suffix.

### Data Helpers

- [ ] **type_coercer.py** — Attempt safe type coercion for DataFrame columns (strings → int/float/datetime) with configurable fallback behaviour and a coercion report.
- [ ] **outlier_utils.py** — IQR and Z-score based outlier detection functions returning boolean masks. Reusable across data-processing and ML repos.
- [ ] **chunked_reader.py** — Read large CSV/JSON files in configurable chunks with optional progress bar. Yields DataFrames for downstream processing.

### System & Environment

- [ ] **timer_decorator.py** — `@timed` decorator that logs function name and elapsed time. Configurable log level and output format.
- [ ] **process_runner.py** — Thin wrapper around `subprocess` for running shell commands from Python: captures stdout/stderr, raises on non-zero exit, optional timeout.

### Reporting

- [ ] **report_builder.py** — Build structured plaintext or Markdown reports from a dict of sections. Handles headers, tables (from lists of dicts), and code blocks.
- [ ] **table_formatter.py** — Format a list of dicts as an aligned plaintext table or Markdown table. Configurable column widths and alignment.

### Date & Time

- [ ] **date_utils.py** — Common date helpers: parse ambiguous date strings, compute business days between dates, generate date range lists, convert between timezones.

---

## Ideas / Backlog

### Secrets & Configuration

- [ ] **secrets_loader.py** — Unified interface for loading secrets from Azure Key Vault, AWS Secrets Manager, or environment variables. Supports caching and auto-refresh.
- [ ] **encryption_utils.py** — Encrypt/decrypt sensitive strings using Fernet (symmetric encryption). Useful for storing encrypted config values.

### API & HTTP Helpers

- [ ] **pagination_helper.py** — REST API pagination utility: handles `next` links, cursor-based pagination, and offset/limit patterns. Yields items from all pages.
- [ ] **http_client_wrapper.py** — Thin wrapper around requests with built-in retries, timeout handling, and automatic JSON encoding/decoding.

### Data Analysis & Reporting

- [ ] **diff_reporter.py** — Compare two dicts or DataFrames and generate human-readable difference reports (what changed, added, removed).
- [ ] **stats_summarizer.py** — Quick stats on numeric data: count, min, max, mean, median, std deviation, quartiles. Returns formatted report.

### Utilities & Helpers

- [ ] **performance_profiler.py** — Simple decorator to measure and log function execution time with memory usage.
- [ ] **batch_processor.py** — Batch processing utility for large datasets: chunks data into configurable batch sizes, tracks progress, handles errors gracefully.
- [ ] **data_validator.py** — Schema validation for dicts: check required fields, types, value ranges. Returns detailed error report.

---

## Notes

- All utilities should have no side effects and be importable without configuration.
- Each module should be independently usable — no cross-module dependencies within this repo.
- Include docstrings and at least one usage example per function.
