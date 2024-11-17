# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - TBD

### Breaking Changes

- Restructured entire codebase (everything now within ./src/)
- All constants and global variables now import from constants.py
- Renamed many (all?) settings entires in config.yml

### Added

- This CHANGELOG
- README (now contains information)
- New configuration setting: logfile
- New install.py function to create necessary directories and files upon first run

### Changed

- Reorganized example_config.yml to place settings before known_hosts
- Removed unnecessary if __name__=="__main__" statements in client and server
