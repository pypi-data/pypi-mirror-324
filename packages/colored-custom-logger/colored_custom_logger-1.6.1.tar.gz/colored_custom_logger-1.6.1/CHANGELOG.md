# 🌈 Changelog

All notable changes to this project will be documented in this fabulous file! 🎉

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2024-09-09

### 🎨 Added
- ✨ New `test_logger.py` file for testing the logger functionality.

### 🔄 Changed
- 🔧 Updated `__init__.py` with improved ColoredFormatter and CustomLogger classes:
  - ColoredFormatter now applies color to the entire log line prefix.
  - Simplified and improved code structure and documentation.
- 📊 Updated version numbers in multiple files (README.md, docs/api.md, docs/index.md, pyproject.toml, setup.py, src/colored_custom_logger/__init__.py).
- 🔧 Improved `utils/sync_versions.py`:
  - Renamed from `version_sync.py` to `sync_versions.py`.
  - Now uses CustomLogger for logging.
  - Reads version directly from `colored_custom_logger.__version__`.

### 🐛 Fixed
- 🎨 Changed CRITICAL log level color from Bright Red to Light Magenta.
- 🚀 Resolved issues with color formatting and log level setting.


## [1.5.7] - 2024-09-08 🚀

### 🎨 Added
- ✨ Magical ability to set different log levels for different logger instances
- 🔧 New `set_default_level` class method to change logging level for all existing and future logger instances

### 🔄 Changed
- 🧪 `CustomLogger` now keeps track of all logger instances
- 🔢 `get_logger` method now returns existing instances if available, potentially updating their level

### 🐛 Fixed
- 🚀 Issue with changing log levels for loggers in imported modules

## [1.5.6] - 2024-09-08 🎈

### 🔧 Changed
- 📊 Updated default log level to INFO

## [1.5.5] - 2024-09-08 🌟

### 🎨 Added
- ✨ Magical ability to set a default logging level for all CustomLogger instances
- 🔧 Fancy option to set a specific logging level when instantiating a logger

### 🔄 Changed
- 🧪 Supercharged unit tests to cover new functionality
- 🔢 Improved version synchronization across project files (we're all in sync now!)

### 🐛 Fixed
- 🚀 Minor bug fixes and performance improvements (we squashed those pesky bugs!)

## [1.5.4] - 2024-07-30 🚀

### 🎨 Added
- 🛠️ New utility scripts for version synchronization and package building

### 🔧 Changed
- 📚 Updated documentation setup instructions
- 🔗 Updated documentation links in project configuration files

## [1.5.3] - 2024-07-27 🌈

### 🎨 Added
- 📸 New example scripts and images for documentation

### 🔧 Changed
- 🎨 Updated color scheme for critical log level
- 📊 Changed default log level to DEBUG
- 🖥️ Set console handler to use sys.stdout

### 📚 Documentation
- 📝 Expanded usage guide with more examples
- 🖼️ Added screenshots to showcase logger output

## [1.5.2] - 2024-07-27 🏗️

### 🎨 Added
- 🏗️ Initial project structure and core functionality

### 📚 Documentation
- 📝 Added initial README, documentation setup, and API reference

---

Remember, life's too short for boring changelogs! Keep logging and stay colorful! 🌈🎨🎭
