"""Print the shared rules and one kj-cinematic prompt recipe."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RECIPE_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills/pipelines/kj-cinematic/prompt-recipes.md"
)
MODALITIES = ("T2I", "I2I", "R2I", "W2I", "T2V", "I2V", "R2V", "W2V")


def read_recipe(modality: str) -> str:
    sections = re.split(r"(?m)^(?=## )", RECIPE_PATH.read_text(encoding="utf-8"))
    chapters = {
        section.splitlines()[0][3:]: section.strip()
        for section in sections[1:]
    }
    blocks = [sections[0].strip()]
    if modality not in ("T2I", "T2V"):
        blocks.append(chapters["共通引用規則"])
    blocks.append(chapters[modality])
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modality", choices=MODALITIES)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    print(read_recipe(args.modality), end="")


if __name__ == "__main__":
    main()
