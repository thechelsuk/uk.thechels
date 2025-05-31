#!/usr/bin/env python3
"""
Generate Software Bill of Materials (SBOM) for TheChels.uk website
This script extracts package information from Gemfile.lock and requirements.txt
and generates a markdown SBOM file.
"""

import os
import re
import datetime
from pathlib import Path


def parse_gemfile_lock(gemfile_lock_path):
    """Parse Gemfile.lock to extract gem names and versions."""
    gems = {}

    with open(gemfile_lock_path, 'r') as f:
        content = f.read()

    # Extract gem specifications from the specs section
    specs_section = re.search(r'specs:\s*\n(.*?)\nPLATFORMS', content,
                              re.DOTALL)
    if specs_section:
        specs_content = specs_section.group(1)

        # Split into lines and look for gem entries
        lines = specs_content.split('\n')
        for line in lines:
            # Look for lines that start with 4 spaces and contain (version)
            # These are the main gem entries, not dependencies
            match = re.match(r'^    ([a-zA-Z0-9_-]+)\s+\(([^)]+)\)$', line)
            if match:
                gem_name, version = match.groups()
                gems[gem_name] = version

    return gems


def parse_requirements_txt(requirements_path):
    """Parse requirements.txt to extract package names."""
    packages = []

    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before any version specifiers)
                    package_name = re.split(r'[>=<!=]', line)[0].strip()
                    if package_name:
                        packages.append(package_name)

    return sorted(packages)


def get_python_package_info():
    """Get Python package information from requirements files."""
    base_path = Path(__file__).parent.parent

    # Main requirements.txt
    main_requirements = base_path / "requirements.txt"
    main_packages = parse_requirements_txt(main_requirements)

    # Python-specific requirements.txt
    python_requirements = base_path / "_python" / "requirements.txt"
    python_packages = parse_requirements_txt(python_requirements)

    # Combine and deduplicate
    all_packages = sorted(set(main_packages + python_packages))

    return all_packages


def generate_sbom_markdown():
    """Generate the SBOM markdown file."""
    base_path = Path(__file__).parent.parent
    gemfile_lock_path = base_path / "Gemfile.lock"

    # Parse dependencies
    gems = parse_gemfile_lock(gemfile_lock_path)
    python_packages = get_python_package_info()

    # Generate markdown content
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    markdown_content = f"""# Software Bill of Materials (SBOM)

**Project:** TheChels.uk
**Generated:** {current_date}
**Description:** Personal website built with Jekyll and Python utilities

## Overview

This document lists all software dependencies used in the TheChels.uk website project, including both Ruby gems for Jekyll and Python packages for utility scripts.

## Ruby Gems (Jekyll Dependencies)

The following Ruby gems are used for the Jekyll static site generator:

| Gem Name | Version | Description |
|----------|---------|-------------|
"""

    # Add Ruby gems
    for gem_name, version in sorted(gems.items()):
        markdown_content += f"| {gem_name} | {version} | Ruby gem |\n"

    markdown_content += f"""
**Total Ruby Gems:** {len(gems)}

## Python Packages

The following Python packages are used for utility scripts and data processing:

| Package Name | Type | Usage |
|--------------|------|-------|
"""

    # Add Python packages with descriptions
    package_descriptions = {
        'feedparser': 'RSS/Atom feed parsing',
        'requests': 'HTTP library for API calls',
        'pathlib': 'Object-oriented filesystem paths',
        'datefinder': 'Date extraction from text',
        'yahoo_fin': 'Yahoo Finance data retrieval',
        'pandas': 'Data manipulation and analysis',
        'requests_html': 'HTML parsing with JavaScript support',
        'argparse': 'Command-line argument parsing',
        'pyyaml': 'YAML file processing',
        'pytest': 'Testing framework',
        'pytest-cov': 'Test coverage reporting',
        'pytest-md': 'Markdown output for pytest',
        'pytest-emoji': 'Emoji support for pytest',
        'yapf': 'Python code formatter',
        'lxml_html_clean': 'HTML cleaning utilities',
        'yfinance': 'Yahoo Finance data access',
        'pillow': 'Image processing library',
        'ruamel.yaml': 'Advanced YAML processing'
    }

    for package in python_packages:
        description = package_descriptions.get(package, 'Python package')
        markdown_content += f"| {package} | Python package | {description} |\n"

    markdown_content += f"""
**Total Python Packages:** {len(python_packages)}

## Summary

- **Ruby Gems:** {len(gems)} packages
- **Python Packages:** {len(python_packages)} packages
- **Total Dependencies:** {len(gems) + len(python_packages)} packages

## Package Managers

- **Ruby:** Bundler (via Gemfile)
- **Python:** pip (via requirements.txt)

## Security Notes

All dependencies are managed through their respective package managers and should be regularly updated to address security vulnerabilities. The project uses:

- `bundle audit` for Ruby gem security checking
- `pip-audit` for Python package security checking (recommended)

## License Information

This SBOM is provided for transparency. Individual packages maintain their own licenses. Please refer to each package's documentation for specific license terms.

---

*This SBOM was automatically generated on {current_date} using the project's dependency files.*
"""

    return markdown_content


def main():
    """Main function to generate and save the SBOM."""
    try:
        # Generate the SBOM content
        sbom_content = generate_sbom_markdown()

        # Save to file
        base_path = Path(__file__).parent.parent
        output_path = base_path / "_pages/SBOM.md"

        with open(output_path, 'w') as f:
            f.write(sbom_content)

        print(f"✅ SBOM generated successfully: {output_path}")
        print(f"📄 File size: {len(sbom_content)} characters")

        # Count totals
        gems = parse_gemfile_lock(base_path / "Gemfile.lock")
        python_packages = get_python_package_info()

        print(f"📦 Ruby gems: {len(gems)}")
        print(f"🐍 Python packages: {len(python_packages)}")
        print(f"🔢 Total dependencies: {len(gems) + len(python_packages)}")

    except Exception as e:
        print(f"❌ Error generating SBOM: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
