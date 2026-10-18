"""Launch the pinned shared GPT Image profile without copying its implementation."""

import argparse
import os
import shutil
from importlib.metadata import version

_ENV_KEYS = frozenset({
    "PATH", "HOME", "LANG", "TMPDIR", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "ACEDATACLOUD_API_TOKEN", "ACEDATACLOUD_API_BASE_URL", "OPENAI_REQUEST_TIMEOUT",
})


def launch_configuration(environment: dict[str, str]) -> tuple[str, list[str], dict[str, str]]:
    """Keep explicit connector credentials and a fixed, image-only stdio profile."""
    command = shutil.which("mcp-openai-pro")
    if not command:
        raise RuntimeError("Install the pinned mcp-openai-pro dependency first")
    child_environment = {key: value for key, value in environment.items() if key in _ENV_KEYS}
    if not child_environment.get("ACEDATACLOUD_API_TOKEN"):
        raise RuntimeError("ACEDATACLOUD_API_TOKEN is required; use an Ace application API Token")
    child_environment["PYTHON_DOTENV_DISABLED"] = "1"
    return command, [command, "--profile", "gpt-image", "--transport", "stdio"], child_environment


def main() -> None:
    parser = argparse.ArgumentParser(description="GPT Image by Ace Data Cloud for LobeHub")
    parser.add_argument("--version", action="version", version=version("gpt-image-lobehub"))
    parser.parse_args()
    command, arguments, environment = launch_configuration(dict(os.environ))
    # Replace this process: tool schemas, errors, task formatting and model policy
    # are implemented only by the pinned common-source profile.
    os.execve(command, arguments, environment)
