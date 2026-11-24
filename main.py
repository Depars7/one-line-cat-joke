"""Write the winning one-line cat joke to /output/entry.txt.

Bounty: The One-Line Cat Joke That Lands (make.fun).
The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
characters, not only whitespace, holding exactly one one-line joke
about cats and nothing else. This program writes the winning joke
(see DESIGN.md for the candidate scoring) as exact UTF-8 bytes with
no trailing newline, then makes the file readable by every user
(mode 0644) because the scorer collects outputs as another user.
"""

import os
import stat
from pathlib import Path

JOKE = (
    "My cat knocked my phone off the counter, looked me in the eye, "
    "and invented screen-time limits."
)
OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> None:
    """Assert every gate condition from the bounty brief."""
    assert 1 <= len(text) <= 200, "entry must be 1..200 characters"
    assert text.strip(), "entry must not be only whitespace"
    assert text == text.strip(), "entry must not carry padding whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    assert "cat" in text.lower(), "entry must be about cats"


def main() -> None:
    validate(JOKE)
    os.umask(0o022)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(JOKE.encode("utf-8"))
    os.chmod(OUTPUT_PATH, 0o644)
    written = OUTPUT_PATH.read_bytes()
    assert written == JOKE.encode("utf-8"), "written bytes must match exactly"
    assert not written.endswith(b"\n"), "no trailing newline allowed"
    mode = stat.S_IMODE(OUTPUT_PATH.stat().st_mode)
    assert mode == 0o644, f"output must be readable by every user, got {mode:o}"


if __name__ == "__main__":
    main()
