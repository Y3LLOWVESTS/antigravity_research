#!/usr/bin/env bash

# ==============================================================================
# Antigravity Research — Markdown Codebundle Generator
#
# PURPOSE
# -------
# Build a single Markdown file containing the source code, tests, simulations,
# configuration, and human-readable documentation needed to review the
# Antigravity Research repository without uploading the repository itself.
#
# The generated bundle is intended primarily for:
#
# - AI-assisted code and scientific review;
# - human code review;
# - architecture review;
# - cross-session project context;
# - auditing scientific assumptions and implementation details.
#
# DESIGN GOALS
# ------------
# 1. Include the files that define the project and its scientific reasoning.
# 2. Include a filtered repository tree before file contents.
# 3. Exclude generated data, logs, figures, caches, virtual environments,
#    binaries, Git internals, and previous codebundles.
# 4. Preserve exact source text without modifying the original files.
# 5. Use Markdown fences that remain valid even when a source file itself
#    contains triple-backtick Markdown examples.
# 6. Record file sizes and SHA-256 hashes so the bundle can be audited.
# 7. Require no third-party Python packages.
#
# INCLUDED CONTENT
# ----------------
# The bundle includes human-readable project files with extensions such as:
#
#     .py
#     .md
#     .sh
#     .toml
#     .yaml / .yml
#     .json
#     .bib
#     .rst
#
# It also includes selected extensionless or dotfiles such as:
#
#     .gitignore
#     .python-version
#
# Typical included project areas:
#
#     src/
#     tests/
#     simulations/
#     theory/
#     models/
#     literature/
#     journal/
#     scripts/
#
# EXCLUDED CONTENT
# ----------------
# The following are intentionally excluded from file contents:
#
#     .git/
#     .venv/
#     venv/
#     __pycache__/
#     .pytest_cache/
#     .ruff_cache/
#     .mypy_cache/
#     .idea/
#     .vscode/
#     node_modules/
#     codebundles/
#     results/data/
#     results/figures/
#     results/logs/
#
# Generated scientific results are excluded because they can be recreated from
# the simulation code and can substantially increase bundle size. Their paths
# may still appear in the repository-tree inventory.
#
# Binary and media files such as PNG, PDF, ZIP, compiled Python bytecode, shared
# libraries, and executables are also excluded from embedded file contents.
#
# OUTPUT
# ------
# A timestamped Markdown file is written under:
#
#     codebundles/
#
# Example:
#
#     codebundles/ANTIGRAVITY_RESEARCH_CODEBUNDLE_20260827-013000.md
#
# SAFETY
# ------
# - Source files are read only.
# - Existing codebundles are never overwritten.
# - The script does not run simulations or tests.
# - The script does not modify source code.
# - The output directory is automatically excluded from future bundles.
#
# USAGE
# -----
# From the repository root:
#
#     ./make_codebundle.sh
#
# The final output path is printed at completion.
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Repository resolution
# ------------------------------------------------------------------------------

SCRIPT_DIR="$(
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1
    pwd
)"

ROOT="$SCRIPT_DIR"
cd "$ROOT"

PROJECT_NAME="ANTIGRAVITY_RESEARCH"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"

OUTPUT_DIR="$ROOT/codebundles"
OUTPUT_FILE="$OUTPUT_DIR/${PROJECT_NAME}_CODEBUNDLE_${TIMESTAMP}.md"

mkdir -p "$OUTPUT_DIR"

# ------------------------------------------------------------------------------
# Temporary workspace
#
# Temporary files are deleted automatically when the script exits.
# ------------------------------------------------------------------------------

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/antigravity-codebundle.XXXXXX")"

cleanup() {
    rm -rf "$TMP_DIR"
}

trap cleanup EXIT

FILE_LIST="$TMP_DIR/included-files.txt"
TREE_LIST="$TMP_DIR/tree.txt"
MANIFEST="$TMP_DIR/manifest.txt"

: > "$FILE_LIST"
: > "$TREE_LIST"
: > "$MANIFEST"

# ------------------------------------------------------------------------------
# Inclusion policy
#
# We deliberately use an allowlist of known text-oriented file types instead
# of trying to include everything that merely happens to look textual.
#
# This makes accidental inclusion of large generated files, databases,
# archives, binary data, and editor state much less likely.
# ------------------------------------------------------------------------------

is_included_file() {
    local path="$1"
    local base
    local extension
    local extension_lower

    base="$(basename "$path")"

    # Important extensionless / dotfiles that carry repository
    # configuration or project-specific documentation.
    case "$base" in
        .gitignore|.python-version|NOTICE)
            return 0
            ;;
    esac

    extension="${base##*.}"

    # macOS ships Bash 3.2, so avoid Bash-4-only ${var,,}
    # lowercase conversion.
    extension_lower="$(
        printf '%s' "$extension" \
            | tr '[:upper:]' '[:lower:]'
    )"

    case "$extension_lower" in
        py|md|sh|toml|yaml|yml|json|bib|rst)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# ------------------------------------------------------------------------------
# Path exclusion policy
#
# These paths either contain generated artifacts, transient environment state,
# repository metadata, large numerical output, or previous bundles.
# ------------------------------------------------------------------------------

is_excluded_path() {
    local path="$1"

    case "$path" in
        .git/*|\
        .venv/*|\
        venv/*|\
        __pycache__/*|\
        */__pycache__/*|\
        .pytest_cache/*|\
        */.pytest_cache/*|\
        .ruff_cache/*|\
        */.ruff_cache/*|\
        .mypy_cache/*|\
        */.mypy_cache/*|\
        .idea/*|\
        */.idea/*|\
        .vscode/*|\
        */.vscode/*|\
        node_modules/*|\
        */node_modules/*|\
        codebundles/*|\
        results/data/*|\
        results/figures/*|\
        results/logs/*|\
        *.egg-info/*|\
        */*.egg-info/*|\
        *.backup-*|\
        *.math-punctuation-backup-*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# ------------------------------------------------------------------------------
# Build the included-file list.
#
# LC_ALL=C produces stable lexical ordering independent of locale.
# ------------------------------------------------------------------------------

while IFS= read -r path; do
    relative="${path#./}"

    if is_excluded_path "$relative"; then
        continue
    fi

    if is_included_file "$relative"; then
        printf '%s\n' "$relative" >> "$FILE_LIST"
    fi
done < <(
    find . \
        -type f \
        -print \
        | LC_ALL=C sort
)

# ------------------------------------------------------------------------------
# Repository tree
#
# The tree intentionally shows more than the embedded-file list. This gives the
# reviewer awareness that generated datasets, figures, logs, and other project
# artifacts exist even though their contents are not copied into the bundle.
#
# Extremely noisy implementation directories are still omitted.
# ------------------------------------------------------------------------------

while IFS= read -r path; do
    relative="${path#./}"

    case "$relative" in
        .git|.git/*|\
        .venv|.venv/*|\
        venv|venv/*|\
        __pycache__|__pycache__/*|\
        */__pycache__|*/__pycache__/*|\
        .pytest_cache|.pytest_cache/*|\
        */.pytest_cache|*/.pytest_cache/*|\
        .ruff_cache|.ruff_cache/*|\
        */.ruff_cache|*/.ruff_cache/*|\
        .mypy_cache|.mypy_cache/*|\
        */.mypy_cache|*/.mypy_cache/*|\
        .idea|.idea/*|\
        */.idea|*/.idea/*|\
        .vscode|.vscode/*|\
        */.vscode|*/.vscode/*|\
        node_modules|node_modules/*|\
        */node_modules|*/node_modules/*|\
        codebundles|codebundles/*|\
        *.egg-info|*.egg-info/*|\
        */*.egg-info|*/*.egg-info/*|\
        *.backup-*|\
        *.math-punctuation-backup-*)
            continue
            ;;
    esac

    printf '%s\n' "$relative" >> "$TREE_LIST"
done < <(
    find . \
        -mindepth 1 \
        -print \
        | LC_ALL=C sort
)

# ------------------------------------------------------------------------------
# Markdown syntax-language selection
#
# Correct language labels improve syntax highlighting when the generated
# bundle is viewed in GitHub, VS Code, or another Markdown renderer.
# ------------------------------------------------------------------------------

language_for_file() {
    local path="$1"
    local base
    local extension

    base="$(basename "$path")"
    extension="${base##*.}"

    case "$base" in
        .gitignore)
            printf '%s\n' "gitignore"
            return
            ;;
        .python-version)
            printf '%s\n' "text"
            return
            ;;
    esac

    case "$extension" in
        py)
            printf '%s\n' "python"
            ;;
        md)
            printf '%s\n' "markdown"
            ;;
        sh)
            printf '%s\n' "bash"
            ;;
        toml)
            printf '%s\n' "toml"
            ;;
        yaml|yml)
            printf '%s\n' "yaml"
            ;;
        json)
            printf '%s\n' "json"
            ;;
        bib)
            printf '%s\n' "bibtex"
            ;;
        rst)
            printf '%s\n' "rst"
            ;;
        *)
            printf '%s\n' "text"
            ;;
    esac
}

# ------------------------------------------------------------------------------
# Markdown fence generation
#
# A fixed ``` fence is unsafe because some project documentation contains
# Markdown examples with triple or quadruple backticks.
#
# This function scans the source file for its longest consecutive run of
# backticks and returns a fence that is at least one character longer, with a
# minimum length of three.
#
# Consequently, embedded Markdown documentation cannot accidentally terminate
# its own codebundle fence.
# ------------------------------------------------------------------------------

markdown_fence_for_file() {
    local path="$1"

    python3 - "$path" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])

text = path.read_text(
    encoding="utf-8",
    errors="replace",
)

runs = [
    len(match.group(0))
    for match in re.finditer(r"`+", text)
]

longest = max(runs, default=0)
length = max(3, longest + 1)

print("`" * length)
PY
}

# ------------------------------------------------------------------------------
# SHA-256 helper
#
# macOS normally provides `shasum`; Linux systems often provide `sha256sum`.
# Supporting both makes the script more portable.
# ------------------------------------------------------------------------------

sha256_file() {
    local path="$1"

    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$path" | awk '{print $1}'
        return
    fi

    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$path" | awk '{print $1}'
        return
    fi

    python3 - "$path" <<'PY'
from pathlib import Path
import hashlib
import sys

path = Path(sys.argv[1])

digest = hashlib.sha256()

with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(chunk)

print(digest.hexdigest())
PY
}

# ------------------------------------------------------------------------------
# Basic repository metadata
# ------------------------------------------------------------------------------

GENERATED_AT="$(date '+%Y-%m-%d %H:%M:%S %Z')"
INCLUDED_COUNT="$(wc -l < "$FILE_LIST" | tr -d ' ')"

GIT_HEAD="NOT_AVAILABLE"
GIT_BRANCH="NOT_AVAILABLE"
GIT_STATUS="NOT_AVAILABLE"
GIT_STATUS_SHORT="NOT_AVAILABLE"

if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    GIT_HEAD="$(git rev-parse HEAD 2>/dev/null || printf 'UNKNOWN')"
    GIT_BRANCH="$(git branch --show-current 2>/dev/null || printf 'UNKNOWN')"

    if git diff --quiet --ignore-submodules -- \
        && git diff --cached --quiet --ignore-submodules -- \
        && [ -z "$(git ls-files --others --exclude-standard)" ]; then
        GIT_STATUS="CLEAN"
    else
        GIT_STATUS="DIRTY_OR_UNTRACKED"
    fi

    GIT_STATUS_SHORT="$(
        git status --short 2>/dev/null             || printf 'UNKNOWN'
    )"
fi

# ------------------------------------------------------------------------------
# Build the per-file manifest before writing contents.
# ------------------------------------------------------------------------------

while IFS= read -r relative; do
    [ -n "$relative" ] || continue

    size_bytes="$(wc -c < "$relative" | tr -d ' ')"
    digest="$(sha256_file "$relative")"

    printf '%s\t%s\t%s\n' \
        "$relative" \
        "$size_bytes" \
        "$digest" \
        >> "$MANIFEST"
done < "$FILE_LIST"

# ------------------------------------------------------------------------------
# Begin Markdown output
# ------------------------------------------------------------------------------

{
    printf '# Antigravity Research — Codebundle\n\n'

    printf '> Generated automatically by `make_codebundle.sh` for source-code, scientific, and documentation review.\n\n'

    printf '## Bundle Metadata\n\n'

    printf -- '- **Project:** `%s`\n' "$PROJECT_NAME"
    printf -- '- **Generated:** `%s`\n' "$GENERATED_AT"
    printf -- '- **Included files:** `%s`\n' "$INCLUDED_COUNT"
    printf -- '- **Git branch:** `%s`\n' "$GIT_BRANCH"
    printf -- '- **Git HEAD:** `%s`\n' "$GIT_HEAD"
    printf -- '- **Working tree:** `%s`\n' "$GIT_STATUS"

    printf '\n'

    printf '## Git Working Tree Snapshot\n\n'

    printf '```text\n'
    printf '%s\n' "$GIT_STATUS_SHORT"
    printf '```\n\n'

    printf '## Review Guidance\n\n'

    cat <<'EOF'
This bundle is intended to provide enough repository context for an independent
reviewer or AI research assistant to understand the current implementation
without relying on previous conversational context.

The bundle prioritizes:

- scientific source code;
- simulation code;
- regression tests;
- mathematical and architectural documentation;
- assumptions and claims documentation;
- project configuration;
- scripts relevant to reproducing or reviewing the research.

Generated numerical results and binary artifacts are intentionally omitted from
embedded contents to keep the bundle reviewable.

When reviewing scientific conclusions, the source documentation, assumptions,
tests, simulation implementation, and claim classifications should be read
together.

EOF

    printf '## Inclusion Policy\n\n'

    cat <<'EOF'
Embedded content normally includes:

```text
*.py
*.md
*.sh
*.toml
*.yaml
*.yml
*.json
*.bib
*.rst
.gitignore
.python-version
```

The following high-volume or non-source areas are intentionally excluded from
embedded content:

```text
.git/
.venv/
venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
.idea/
.vscode/
node_modules/
codebundles/
results/data/
results/figures/
results/logs/
```

Binary and generated media files are not embedded.

EOF

    printf '## Repository Tree\n\n'
    printf '```text\n'
    cat "$TREE_LIST"
    printf '```\n\n'

    printf '## Included File Manifest\n\n'
    printf '| File | Bytes | SHA-256 |\n'
    printf '| --- | ---: | --- |\n'

    while IFS=$'\t' read -r relative size_bytes digest; do
        printf '| `%s` | %s | `%s` |\n' \
            "$relative" \
            "$size_bytes" \
            "$digest"
    done < "$MANIFEST"

    printf '\n'
    printf '%s\n\n' '---'
    printf '# File Contents\n\n'

} > "$OUTPUT_FILE"

# ------------------------------------------------------------------------------
# Append every included source/documentation file.
# ------------------------------------------------------------------------------

while IFS= read -r relative; do
    [ -n "$relative" ] || continue

    language="$(language_for_file "$relative")"
    fence="$(markdown_fence_for_file "$relative")"
    size_bytes="$(wc -c < "$relative" | tr -d ' ')"
    digest="$(sha256_file "$relative")"

    {
        printf '## `%s`\n\n' "$relative"

        printf '**Bytes:** `%s`  \n' "$size_bytes"
        printf '**SHA-256:** `%s`\n\n' "$digest"

        printf '%s%s\n' "$fence" "$language"

        cat "$relative"

        # Ensure the closing fence begins on a fresh line even when the source
        # file does not have a final newline.
        if [ -s "$relative" ] && [ "$(tail -c 1 "$relative" | wc -l | tr -d ' ')" -eq 0 ]; then
            printf '\n'
        fi

        printf '%s\n\n' "$fence"
        printf '%s\n\n' '---'
    } >> "$OUTPUT_FILE"

done < "$FILE_LIST"

# ------------------------------------------------------------------------------
# Final verification
# ------------------------------------------------------------------------------

if [ ! -s "$OUTPUT_FILE" ]; then
    echo "ERROR: Codebundle was not created."
    exit 1
fi

BUNDLE_SIZE_BYTES="$(wc -c < "$OUTPUT_FILE" | tr -d ' ')"
BUNDLE_SIZE_MB="$(
    python3 - "$BUNDLE_SIZE_BYTES" <<'PY'
import sys

size = int(sys.argv[1])
print(f"{size / (1024 * 1024):.2f}")
PY
)"

echo
echo "=== ANTIGRAVITY RESEARCH CODEBUNDLE COMPLETE ==="
echo "OUTPUT=$OUTPUT_FILE"
echo "INCLUDED_FILES=$INCLUDED_COUNT"
echo "BUNDLE_BYTES=$BUNDLE_SIZE_BYTES"
echo "BUNDLE_MIB=$BUNDLE_SIZE_MB"
echo "FILE_TREE=INCLUDED"
echo "FILE_MANIFEST=INCLUDED"
echo "SHA256_MANIFEST=INCLUDED"
echo "SOURCE_CODE=INCLUDED"
echo "TESTS=INCLUDED"
echo "SIMULATIONS=INCLUDED"
echo "DOCUMENTATION=INCLUDED"
echo "GENERATED_DATA_CONTENT=EXCLUDED"
echo "GENERATED_FIGURES=EXCLUDED"
echo "GENERATED_LOGS=EXCLUDED"
echo "VIRTUAL_ENVIRONMENT=EXCLUDED"
echo "PYTHON_CACHES=EXCLUDED"
echo "GIT_INTERNALS=EXCLUDED"
echo "PRIOR_CODEBUNDLES=EXCLUDED"
echo "STATUS=GREEN"
