# config-getter

Holds common configuration files for different types of projects.
Also provides a CLI to easily copy config into projects.

## Usage

```sh
config-getter python github         # Add GitHub Action templates for Python projects
config-getter python ruff           # Insert ruff config into the current pyproject.toml
config-getter python git            # Append python items into .gitignore

config-getter docker dockerignore   # Add .dockerignore file
config-getter docker python         # Get a Dockerfile for build Python applications
config-getter docker git            # Append Docker items into .gitignore

config-getter --help                # Show help text
```

In general, the format is `config-getter <TECH> <CONFIG>`.

A `--force` mode will override existing configuration.

Essentially the CLI just downloads the file from GitHub and places it correctly into the project.

## Install

```sh
# Install into dedicated environment with pipx or uvx
pipx install config-getter
uvx install config-getter

# Install from source
git clone https://github.com/cooperellidge/get-config.git
make .venv
source .venv/bin/activate
```
