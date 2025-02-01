from pathlib import Path

import requests
import typer

app = typer.Typer()

GITHUB_BASE_URL = (
    "https://raw.githubusercontent.com/cooperellidge/config-getter/main/config"
)
GITHUB_API_URL = (
    "https://api.github.com/repos/cooperellidge/config-getter/contents/config"
)

ALIASES = {
    "github": ".github",
}


def download_file(tech: str, file_path: str, *, force: bool) -> None:
    """Download a single file and save it to the local directory."""
    url = f"{GITHUB_BASE_URL}/{tech}/{file_path}"
    response = requests.get(url, stream=True, timeout=15)

    if not response.ok:
        typer.echo(f"Error: Could not download {file_path} for {tech}")
        raise typer.Exit(code=1)

    dest_path = Path.cwd() / file_path
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists() and not force:
        typer.echo(f"Warning: {file_path} already exists. Use --force to overwrite.")
        raise typer.Exit(code=1)

    with dest_path.open("w", encoding="utf-8") as f:
        f.write(response.text)

    typer.echo(f"Downloaded: {file_path}")


def fetch_directory_contents(tech: str, directory: str) -> list[dict]:
    """Fetch the contents of a directory from the GitHub API."""
    url = f"{GITHUB_API_URL}/{tech}/{directory}"
    response = requests.get(url, timeout=15)

    if not response.ok:
        typer.echo(
            f"Error: Could not fetch directory listing for {directory} in {tech}"
        )
        return []
    resp = response.json()

    if isinstance(resp, dict):
        return [resp]

    return resp


def download_directory(
    tech: str, directory: str, *, force: bool, depth: int = 3, current_depth: int = 0
) -> None:
    """Recursively download a directory up to the specified depth limit."""
    if depth != -1 and current_depth >= depth:
        typer.echo(
            f"Skipping deeper levels (reached max depth {depth}) for: {directory}"
        )
        return

    typer.echo(f"Exploring: {directory} (Depth: {current_depth})")

    contents = fetch_directory_contents(tech, directory)

    for item in contents:
        relative_path = item["path"].replace(f"config/{tech}/", "", 1)

        if item["type"] == "file":
            download_file(tech, relative_path, force=force)
        elif item["type"] == "dir":
            download_directory(
                tech,
                relative_path,
                force=force,
                depth=depth,
                current_depth=current_depth + 1,
            )


def resolve_alias(path: str) -> str:
    """Resolve alias to its actual directory path if defined."""
    resolved = ALIASES.get(path, path)
    typer.echo(f"Alias: {path} -> {resolved}")
    return resolved


@app.command()
def main(
    tech: str = typer.Argument(..., help="Technology category (e.g., python, docker)"),
    config: str = typer.Argument(..., help="Configuration file or directory"),
    *,
    force: bool = typer.Option(
        default=False, is_flag=True, help="Overwrite existing files"
    ),
    depth: int = typer.Option(
        default=3,
        help="Max recursion depth (-1 for no limit)",
    ),
) -> None:
    """Fetch and place a configuration file or directory into the current project."""
    resolved_config = resolve_alias(config)
    contents = fetch_directory_contents(tech, resolved_config)

    # TODO: test unbalanced directories, e.g.
    # root/
    # ├── dir1/
    # │   └── file1
    # └── dir2/
    #     ├── dir3/
    #     │   └── file2
    #     ├── file3
    #     └── file2

    if len(contents) > 1:
        typer.echo(f"Downloading directory '{resolved_config}' for {tech}...")
        download_directory(tech, resolved_config, force=force, depth=depth)
    else:
        download_file(tech, resolved_config, force=force)
