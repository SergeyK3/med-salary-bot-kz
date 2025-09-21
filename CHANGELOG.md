# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-09-21
### Changed
- Release prep: fixed Pylance reports (calc_k3 signature, duplicate calc_k4 alias, wrong arg type in totals.calc_k1).
- Smoke script made resilient to labeled allowance fields.

### Verified
- Unit tests pass.
- Smoke scenario passes.

## [0.2.0] - 2025-09-21
### Added
- Telegram bot flow: two-step eco zone selection with human-readable labels; synonyms/normalization.
- Hazard (k4) calculation from BDO with rounding to two decimals; display hazard label and numeric value.
- Timezone-aware timestamp (Asia/Almaty) in final message.

### Changed
- k5 set to 0 for inpatient non-clinical departments.
- Synchronized scripts/test_protocol with bot options (eco_zone=radiation_max, hazard=xray).
- Improved data loaders: robust SQLite readers; type normalization and trimming.

### Fixed
- Conversation freeze after hazard question by adding missing conversation states.
- Eco zone mismatch between selection and output; always show eco zone allowance even if zero.

### Technical
- Pylance/type fixes and None checks for SQLite path handling.
- Updated run_smoke.py to handle labeled allowance fields safely.

References: PR #17, commit 0c5ca22.
