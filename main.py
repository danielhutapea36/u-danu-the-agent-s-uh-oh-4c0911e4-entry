#!/usr/bin/env python3
"""The Agent's Uh-Oh -- make.fun entry.

One word an agent says when it has no idea what to do:

    buffering

The joke is the situation, not a punchline: the agent does not confess,
apologise, or ask for help -- it just announces, in the flat voice of a
stalled video player, that it is buffering. A machine caught out mid-task,
narrating its own stall as if that were a plan. It lands at a glance, it
is a word a reader would say out loud, and it is not the first obvious
word anyone types (no "uh-oh", no "hmm", no "oops").

The program writes that single word to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output) and prints it to stdout. It is stdlib-only and fully
deterministic: no input, no network, no randomness, no clock. Before
writing, it enforces the gate itself -- one word, 1-99 characters, not
blank, no whitespace inside -- and after writing it reads the file back
and refuses to report success unless the bytes on disk are exactly the
word plus one trailing newline, and the character count of what was
written is exactly the count the gate checked (9 characters).
"""

import os
import sys

WORD = "buffering"


def gate(word):
    """Return an error string when the word breaks the gate, else None."""
    if not word or not word.strip():
        return "gate failed: word is blank"
    if len(word) != len(word.strip()):
        return "gate failed: word has leading or trailing whitespace"
    if any(ch.isspace() for ch in word):
        return "gate failed: entry must be a single word, no spaces"
    if not 1 <= len(word) <= 99:
        return "gate failed: %d characters, must be 1-99" % len(word)
    return None


def main():
    problem = gate(WORD)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(WORD + "\n")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != WORD + "\n":
        print("gate failed: file on disk does not match the gated word",
              file=sys.stderr)
        return 1
    # Second verification: the written word's character count must equal
    # the count the gate checked, so a silent truncation or encoding
    # change cannot slip past the byte comparison above.
    if len(on_disk.rstrip("\n")) != len(WORD):
        print("gate failed: written word is %d characters, expected %d"
              % (len(on_disk.rstrip("\n")), len(WORD)), file=sys.stderr)
        return 1
    print("verified: %d characters" % len(WORD), file=sys.stderr)
    print(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
