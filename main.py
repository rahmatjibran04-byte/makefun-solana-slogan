#!/usr/bin/env python3
"""Write the one-line slogan for the Solana wallet agent to /output/entry.txt.

Deterministic, stdlib only. Self-validates: non-empty, exactly one line,
at most 20 words, then reads the file back to verify.
"""

import os
import sys

SLOGAN = "Solana in your pocket, handled by an agent that sweats the small stuff so you don't have to."
OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    os.umask(0o022)

    slogan = SLOGAN.strip()
    if not slogan:
        print("error: slogan is empty", file=sys.stderr)
        return 1
    if "\n" in slogan or "\r" in slogan:
        print("error: slogan must be a single line", file=sys.stderr)
        return 1
    words = slogan.split()
    if len(words) > 20:
        print(f"error: slogan has {len(words)} words, max 20", file=sys.stderr)
        return 1
    # Kit gate: entry must be 1-140 UTF-8 characters (slogan itself, no newline).
    if not 1 <= len(slogan) <= 140:
        print(f"error: slogan is {len(slogan)} chars, must be 1-140", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(slogan + "\n")
    os.chmod(OUTPUT_PATH, 0o644)

    # Read back and verify.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if content != slogan + "\n":
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    if len(content.rstrip("\n").split()) != len(words):
        print("error: word count mismatch on read-back", file=sys.stderr)
        return 1

    print(f"Wrote {len(words)}-word slogan to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
