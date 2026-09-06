#!/usr/bin/env bash

# ==============================================================================
# Antigravity Research — Journal Bundle Generator
#
# PURPOSE
# -------
# Combine all dated Markdown research journals under journal/ into one
# chronological Markdown bundle for AI/human review and cross-session upload.
#
# INCLUDED
# --------
#     journal/20*.md
#
# EXCLUDED
# --------
#     journal/TEMPLATE.md
#     journal/LICENSE.md
#     non-dated journal support files
#     previous generated bundles
#
# OUTPUT
# ------
#     codebundles/ANTIGRAVITY_RESEARCH_JOURNAL_BUNDLE_<timestamp>.md
#
# The source journals are read only and are never modified.
# ==============================================================================

SCRIPT_DIR="$(
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1
    pwd
)"

ROOT="$SCRIPT_DIR"
JOURNAL_DIR="$ROOT/journal"
OUTPUT_DIR="$ROOT/codebundles"

PROJECT_NAME="ANTIGRAVITY_RESEARCH"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"
GENERATED_AT="$(date '+%Y-%m-%d %H:%M:%S %Z')"

OUTPUT_FILE="$OUTPUT_DIR/${PROJECT_NAME}_JOURNAL_BUNDLE_${TIMESTAMP}.md"

mkdir -p "$OUTPUT_DIR"

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/antigravity-journals.XXXXXX")"
FILE_LIST="$TMP_DIR/journals.txt"

cleanup() {
    rm -rf "$TMP_DIR"
}

trap cleanup EXIT

find "$JOURNAL_DIR" \
    -maxdepth 1 \
    -type f \
    -name '20*.md' \
    -print \
    | LC_ALL=C sort \
    > "$FILE_LIST"

INCLUDED_COUNT="$(
    wc -l < "$FILE_LIST" | tr -d ' '
)"

if [ "$INCLUDED_COUNT" -eq 0 ]; then
    echo "ERROR: No dated journal files found in:"
    echo "$JOURNAL_DIR"
else
    TOTAL_SOURCE_BYTES=0

    while IFS= read -r journal_path; do
        [ -n "$journal_path" ] || continue

        size_bytes="$(
            wc -c < "$journal_path" | tr -d ' '
        )"

        TOTAL_SOURCE_BYTES="$(
            awk \
                -v a="$TOTAL_SOURCE_BYTES" \
                -v b="$size_bytes" \
                'BEGIN { printf "%.0f", a + b }'
        )"
    done < "$FILE_LIST"

    FIRST_JOURNAL="$(
        head -n 1 "$FILE_LIST"
    )"

    LATEST_JOURNAL="$(
        tail -n 1 "$FILE_LIST"
    )"

    FIRST_REL="${FIRST_JOURNAL#"$ROOT"/}"
    LATEST_REL="${LATEST_JOURNAL#"$ROOT"/}"

    {
        printf '# Antigravity Research — Journal Bundle\n\n'

        printf '> Generated automatically by `make_journal_bundle.sh` from the dated research journals under `journal/`.\n\n'

        printf '## Bundle Metadata\n\n'
        printf -- '- **Project:** `%s`\n' "$PROJECT_NAME"
        printf -- '- **Generated:** `%s`\n' "$GENERATED_AT"
        printf -- '- **Included journals:** `%s`\n' "$INCLUDED_COUNT"
        printf -- '- **First journal:** `%s`\n' "$FIRST_REL"
        printf -- '- **Latest journal:** `%s`\n' "$LATEST_REL"
        printf -- '- **Combined source bytes:** `%s`\n\n' "$TOTAL_SOURCE_BYTES"

        printf '## Review Guidance\n\n'
        printf '%s\n\n' \
            'This bundle contains the chronological durable research journal for ANTIGRAVITY_RESEARCH.' \
            'Each journal is preserved as raw Markdown so headings, equations, tables, and code blocks remain intact.' \
            'Journal entries describe the scientific state when they were written. Later completed results may supersede earlier frontier descriptions.' \
            'When entries conflict, prefer the newest completed result unless a later journal explicitly preserves the earlier conclusion.' \
            'Current implementation details should still be checked against the latest source code, results, carry-over notes, and active buildplans.'

        printf '## Inclusion Policy\n\n'
        printf 'Included:\n\n'
        printf '```text\n'
        printf 'journal/20*.md\n'
        printf '```\n\n'

        printf 'Excluded:\n\n'
        printf '```text\n'
        printf 'journal/TEMPLATE.md\n'
        printf 'journal/LICENSE.md\n'
        printf 'non-dated support documents\n'
        printf 'previous generated bundles\n'
        printf '```\n\n'

        printf '## Journal Index\n\n'
        printf '| # | Journal | Bytes |\n'
        printf '| ---: | --- | ---: |\n'

        index=0

        while IFS= read -r journal_path; do
            [ -n "$journal_path" ] || continue

            index=$((index + 1))
            relative="${journal_path#"$ROOT"/}"
            size_bytes="$(
                wc -c < "$journal_path" | tr -d ' '
            )"

            printf '| %s | `%s` | %s |\n' \
                "$index" \
                "$relative" \
                "$size_bytes"
        done < "$FILE_LIST"

        printf '\n---\n\n'
        printf '# Journal Contents\n\n'
    } > "$OUTPUT_FILE"

    journal_number=0

    while IFS= read -r journal_path; do
        [ -n "$journal_path" ] || continue

        journal_number=$((journal_number + 1))
        relative="${journal_path#"$ROOT"/}"

        {
            printf '<!-- ====================================================================== -->\n'
            printf '<!-- BEGIN JOURNAL %s OF %s: %s -->\n' \
                "$journal_number" \
                "$INCLUDED_COUNT" \
                "$relative"
            printf '<!-- ====================================================================== -->\n\n'
        } >> "$OUTPUT_FILE"

        cat "$journal_path" >> "$OUTPUT_FILE"

        printf '\n\n' >> "$OUTPUT_FILE"

        {
            printf '<!-- ====================================================================== -->\n'
            printf '<!-- END JOURNAL %s OF %s: %s -->\n' \
                "$journal_number" \
                "$INCLUDED_COUNT" \
                "$relative"
            printf '<!-- ====================================================================== -->\n\n'
            printf '%s\n\n' '---'
        } >> "$OUTPUT_FILE"
    done < "$FILE_LIST"

    BUNDLE_SIZE_BYTES="$(
        wc -c < "$OUTPUT_FILE" | tr -d ' '
    )"

    BUNDLE_SIZE_MIB="$(
        awk \
            -v size="$BUNDLE_SIZE_BYTES" \
            'BEGIN { printf "%.2f", size / (1024 * 1024) }'
    )"

    echo
    echo "=== ANTIGRAVITY RESEARCH JOURNAL BUNDLE COMPLETE ==="
    echo "OUTPUT=$OUTPUT_FILE"
    echo "INCLUDED_JOURNALS=$INCLUDED_COUNT"
    echo "FIRST_JOURNAL=$FIRST_REL"
    echo "LATEST_JOURNAL=$LATEST_REL"
    echo "SOURCE_BYTES=$TOTAL_SOURCE_BYTES"
    echo "BUNDLE_BYTES=$BUNDLE_SIZE_BYTES"
    echo "BUNDLE_MIB=$BUNDLE_SIZE_MIB"
    echo "RAW_MARKDOWN_PRESERVED=YES"
    echo "TEMPLATE_EXCLUDED=YES"
    echo "LICENSE_EXCLUDED=YES"
    echo "SOURCE_JOURNALS_MODIFIED=NO"
    echo "STATUS=GREEN"
fi
