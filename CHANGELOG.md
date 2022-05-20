# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5] - 2022-05-20

### Added

- Bash linter script.
- JSON linter script.
- Latex linter script.
- Markdown linter script.
- Python linter script.
- Pytest unit tests.

## [0.4] - 2022-05-06

### Added

- Changelog file.

## [0.3] - 2022-05-03

### Added

- Docstrings in Python scripts.
- Sphinx documentation of Python code.

### Removed

- Preparation stage is now included in stage 1 and stage 2 separately.
- Unused functions.

## [0.2] - 2022-04-27

### Added

- Separate folder structure for data (stage 1) and analysis data (stage 2).
- Placeholders for financial data is now located in custom JSON files. The
  replaced data can then be parsed in Latex files.
- DCF for different FCF growth rates in order to get a better feeling for
  potential gains for the company.

### Changed

- Rework stock analysis pipeline stages.

## [0.1] - 2022-03-12

### Added

- Initial project outline.
- Initial solution with placeholders in Latex template.
- Python scripts for extracting data from JSON files and calculating composed
  financial data.
- Mapping from ISIN to API parameters for EOD historical data API.
