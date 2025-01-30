from dagster._core.libraries import DagsterLibraryRegistry

from dagster_shell.ops import create_shell_command_op, create_shell_script_op, shell_op
from dagster_shell.utils import (
    execute as execute_shell_command,
    execute_script_file as execute_shell_script,
)
from dagster_shell.version import __version__

DagsterLibraryRegistry.register("dagster-shell", __version__)

__all__ = [
    "create_shell_command_op",
    "create_shell_script_op",
    "execute_shell_command",
    "execute_shell_script",
    "shell_op",
]
