# OceanBase Desktop

A Homebrew cask for installing and managing OceanBase Desktop - a powerful GUI tool for OceanBase database management.

## Description

OceanBase Desktop is a comprehensive graphical user interface tool designed to simplify the installation, configuration, and management of OceanBase databases. This Homebrew cask provides an easy way to install OceanBase Desktop on macOS systems.

## Features

- **Easy Installation**: One-command installation via Homebrew
- **Database Management**: Intuitive GUI for OceanBase database operations
- **Cross-Platform**: Optimized for macOS with ARM64 support
- **Integration**: Seamless integration with OrbStack for virtual machine management

## Requirements

- macOS (ARM64 architecture)
- [Homebrew](https://brew.sh/) package manager
- [OrbStack](https://orbstack.dev/) (automatically installed as dependency)

## Installation

### Prerequisites

1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
   ```

2. Add this tap to your Homebrew installation:
   ```bash
   brew tap oceanbase/oceanbase-desktop https://gitee.com/oceanbase/homebrew-oceanbase-desktop.git
   ```

### Install OceanBase Desktop

```bash
brew install --cask oceanbase-desktop
```

The installation will automatically:
- Download the latest version of OceanBase Desktop
- Install OrbStack as a dependency (if not already installed)
- Place the application in your Applications folder

## Usage

After installation, you can:

1. **Launch the Application**: Find "OceanBase Desktop" in your Applications folder or use Spotlight search
2. **First Run**: The application will guide you through initial setup
3. **Database Operations**: Use the GUI to manage your OceanBase databases

## Application Information

- **Current Version**: 1.1.0
- **Architecture**: ARM64 (Apple Silicon)
- **Installation Guide**: [how to install OceanBase Desktop](https://www.oceanbase.com/docs/common-oceanbase-database-cn-1000000002866370)
- **Open Source**: [open source website](https://open.oceanbase.com/)

## Uninstallation

To remove OceanBase Desktop:

```bash
brew uninstall --cask oceanbase-desktop
```

This will also clean up:
- Application files
- Application Support data
- Saved application state
- Application Virtual Machine

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.