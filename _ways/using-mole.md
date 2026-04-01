---
layout: post
title: How to run mole
seo: Ways - run mole
tag: ways
permalink: /ways/run-mole
link: https://github.com/tw93/Mole/blob/main/README.md
cited: Mole
date: 2026-03-01

---

## Features

- All-in-one toolkit: Combines CleanMyMac, AppCleaner, DaisyDisk, and iStat Menus in a single binary
- Deep cleaning: Removes caches, logs, and browser leftovers to reclaim gigabytes of space
- Smart uninstaller: Removes apps plus launch agents, preferences, and hidden remnants
- Disk insights: Visualizes usage, finds large files, rebuilds caches, and refreshes system services
- Live monitoring: Shows real-time CPU, GPU, memory, disk, and network stats

## Quick Start

Install via Homebrew

`brew install mole`

Or via script

`# Optional args: -s latest for main branch code, -s 1.17.0 for specific version
curl -fsSL <https://raw.githubusercontent.com/tw93/mole/main/install.sh> | bash`

_Note: Mole is built for macOS. An experimental Windows version is available in the windows branch for early adopters._

## Run

    mo                           # Interactive menu
    mo clean                     # Deep cleanup
    mo uninstall                 # Remove apps + leftovers
    mo optimize                  # Refresh caches & services
    mo analyze                   # Visual disk explorer
    mo status                    # Live system health dashboard
    mo purge                     # Clean project build artifacts
    mo installer                 # Find and remove installer files

    mo touchid                   # Configure Touch ID for sudo
    mo completion                # Set up shell tab completion
    mo update                    # Update Mole
    mo update --nightly          # Update to latest unreleased main build, script install only
    mo remove                    # Remove Mole from system
    mo --help                    # Show help
    mo --version                 # Show installed version

## Preview safely

    mo clean --dry-run
    mo uninstall --dry-run
    mo purge --dry-run

    # Also works with: optimize, installer, remove, completion, touchid enable

    mo clean --dry-run --debug   # Preview + detailed logs
    mo optimize --whitelist      # Manage protected optimization rules
    mo clean --whitelist         # Manage protected caches
    mo purge --paths             # Configure project scan directories
    mo analyze /Volumes          # Analyze external drives only
