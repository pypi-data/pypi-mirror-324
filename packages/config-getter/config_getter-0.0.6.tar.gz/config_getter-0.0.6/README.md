# config-getter

Holds common configuration files for different types of projects.
Also provides a CLI to easily copy config into projects, available via PyPI.

## Usage

```sh
config-getter python .github/workflows/checks.yml  # Add GitHub Action templates for checking Python projects
config-getter python Makefile  # Add Makefile with helpful Python commands
config-getter python .gitignore  # Add Python items into .gitignore

config-getter docker .dockerignore  # Add .dockerignore file
config-getter docker .gitignore  # Add Docker items into .gitignore

config-getter --help                # Show help text
```

In general, the format is `config-getter <TECH> <CONFIG>`.

A `--force` mode will override existing configuration.

Essentially the CLI just downloads the file from GitHub and places it correctly into the project.

## Install

```sh
# Run in a temporary environment with uvx
uvx config-getter <TECH> <CONFIG>

# Install from source
git clone https://github.com/cooperellidge/get-config.git
make .venv
source .venv/bin/activate
config-getter <TECH> <CONFIG>
```

## Future work

- Appending configuration to existing files, including JSON
- Custom configuration, e.g. point to other GitHub sources
- Templating, so that you can pre-fill templates with things like project names
- Documentation website, MkDocs hosted on GitHub Pages
