"""CLI entry point for codex-technomanticus-arcana."""

import sys


def main() -> None:
    commands = {
        "build": _build,
        "validate": _validate,
    }

    args = sys.argv[1:]
    if not args or args[0] not in commands:
        _usage(commands)
        sys.exit(1)

    sys.exit(commands[args[0]]())


def _build() -> int:
    from scripts.build_deck import main as build_main
    return build_main()


def _validate() -> int:
    from scripts.validate_cards import main as validate_main
    return validate_main()


def _usage(commands: dict) -> None:
    cmds = " | ".join(commands)
    print(f"Usage: cta [{cmds}]")
