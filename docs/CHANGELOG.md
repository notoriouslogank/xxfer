# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 27-11-2024

### Breaking Changes

- Renamed xxfer.py to main.py to (hopefully) allow for direct execution with ``python3 -m xxfer``.

## [0.3.1] - 27-11-2024

### Hotfix

- Merged 0.3.0 changes into main branch; updated version

## [0.3.0] - 27-11-2024

### Breaking Changes

- Entire project has been restructured; there are now separate 'configs' and 'install' modules within 'src/'
- Updated requirements.txt to accurately reflect current requirements
- Almost all local imports have changed due to restructuring

### Added

- Docstrings for every function in codebase
- Useful logging messages for (nearly) every function

### Known Bugs

- Compressing and sending files seems to take longer than previous versions

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
