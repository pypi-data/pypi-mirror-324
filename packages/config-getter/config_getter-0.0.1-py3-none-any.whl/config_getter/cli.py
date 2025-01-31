from pathlib import Path

import requests
import typer

app = typer.Typer()

GITHUB_BASE_URL = (
    "https://raw.githubusercontent.com/cooperellidge/get-config/main/config"
)


def download_and_place_file(tech: str, config: str, *, force: bool) -> None:  # noqa: D103
    url = f"{GITHUB_BASE_URL}/{tech}/{config}"
    response = requests.get(url, stream=True, timeout=15)

    if not response.ok:
        typer.echo(f"Error: Could not download {config} for {tech}")
        raise typer.Exit(code=1)

    path = Path(config)

    dest_path = Path.cwd() / path

    if dest_path.exists() and not force:
        typer.echo(f"Warning: {config} already exists. Use --force to overwrite.")
        raise typer.Exit(code=1)

    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)

    with dest_path.open("w", encoding="utf-8") as f:
        f.write(response.text)

    typer.echo(f"{config} for {tech} added successfully!")


@app.command()
def main(
    tech: str = typer.Argument(..., help="Technology category (e.g., python, docker)"),
    config: str = typer.Argument(
        ..., help="Configuration file to fetch (e.g., ruff, gitignore)"
    ),
    *,
    force: bool = typer.Option(
        default=False,
        is_flag=True,
        help="Overwrite existing file",
    ),
) -> None:
    """Fetch and place a configuration file into the current project."""
    download_and_place_file(tech, config, force=force)


if __name__ == "__main__":
    app()
