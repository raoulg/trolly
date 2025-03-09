def main() -> None:
    """Run the trolly experiment web server."""
    from .app import run_app
    run_app()
