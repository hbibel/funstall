import subprocess
from logging import Logger
from textwrap import indent
from typing import TypedDict


class ExecuteContext(TypedDict):
    logger: Logger


def execute(ctx: ExecuteContext, cmd: list[str]) -> tuple[bool, int, str]:
    ctx["logger"].debug("Invoking `%s`", " ".join(cmd))
    done = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = done.stdout.decode(errors="ignore")
    ctx["logger"].debug("output:\n%s", indent(output, "    "))
    return (True, done.returncode == 0, output)
