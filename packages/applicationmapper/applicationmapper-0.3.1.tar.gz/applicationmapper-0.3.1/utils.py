from textwrap import indent as _indent


def indent(text: str) -> str:
    return _indent(text, "  ")


def enumerate_lines(text: str) -> str:
    lines = text.splitlines()
    padding = len(lines) // 10 + 1
    return "\n".join(f"{str(idx + 1).rjust(padding)}. {line}" for idx, line in enumerate(lines))
