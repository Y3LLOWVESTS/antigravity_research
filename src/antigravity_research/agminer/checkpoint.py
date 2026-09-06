"""
Bounded finalist-checkpoint policy.

Ordinary failures and ordinary Tier-1 candidates do not retain field arrays.
"""

from __future__ import annotations

from pathlib import Path


def enforce_checkpoint_limit(
    checkpoint_dir: str | Path,
    *,
    limit: int,
) -> list[Path]:
    directory = Path(checkpoint_dir)

    if not directory.exists():
        return []

    files = sorted(
        (
            path
            for path in directory.iterdir()
            if path.is_file()
        ),
        key=lambda path: (
            path.stat().st_mtime,
            path.name,
        ),
        reverse=True,
    )

    removed: list[Path] = []

    for path in files[limit:]:
        path.unlink()
        removed.append(path)

    return removed
