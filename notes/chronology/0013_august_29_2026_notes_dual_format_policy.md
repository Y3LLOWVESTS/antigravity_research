### BEGIN NOTE - AUGUST 29 2026 - DUAL NOTES FORMAT POLICY

# ANTIGRAVITY_RESEARCH — Monolithic Notes and Chronology Policy

## Purpose

The project intentionally maintains the research history in two complementary forms.

`NOTES.MD` remains the complete long-running monolithic research record.

`notes/chronology/` contains the same research history divided into smaller chronological Markdown files.

Both forms are intentional and should be preserved.

## Why the monolithic notes remain important

The monolithic `NOTES.MD` file is especially useful for project continuity.

It provides one file containing the accumulated research history, mathematical results, failed branches, decision gates, implementation context, and carry-forward instructions.

This makes it convenient to provide the complete project history to a new ChatGPT or other AI-assisted research session without uploading many separate chronology files.

It is also useful for whole-project searching, archival continuity, and human review of the research as one continuous record.

Therefore:

NOTES.MD must not be replaced by a small index or discarded merely because it is large.

## Why the smaller chronology also remains important

The monolithic notes have grown to approximately tens of thousands of lines and contain more than one thousand mathematical display expressions.

During the August 29, 2026 documentation audit, otherwise valid mathematics was observed to render successfully when placed in the smaller chronology files while the same mathematics could fail with GitHub's `Unable to render expression` message inside the very large monolithic document.

The live-math syntax was separately audited and repaired.

This provides strong evidence that at least some remaining failures in the monolithic page are caused by GitHub rendering scale or complexity rather than malformed equations.

The chronology files therefore provide the preferred GitHub-readable representation of the research history.

For mathematical reading on GitHub:

`notes/chronology/` is preferred.

For single-file project handoff, archival continuity, and AI-session context:

`NOTES.MD` is preferred.

## August 29, 2026 documentation repair

The previous monolithic notes were split into chronological slices so that the mathematical record could be inspected and rendered in smaller documents.

The split was verified by reconstructing the chronology and confirming byte-for-byte equality with the repaired monolithic research history before the monolithic form was restored.

A repository-wide live-math audit was also performed.

The audit removed or normalized known GitHub-sensitive live-math constructs while preserving the intended scientific content and numerical values.

The README was then updated to explain the distinction between the two note representations and to direct GitHub readers toward `notes/chronology/` when reliable mathematical rendering is required.

## Going-forward workflow

Every substantial new carry-forward research note should be preserved in both representations.

The preferred workflow is:

1. Write each new research handoff as a self-contained chronological note.
2. Store that note as the next numbered file under `notes/chronology/`.
3. Append the same note content to the end of `NOTES.MD`.
4. Preserve chronological order in both representations.
5. Run the Markdown live-math audit before closeout when the note contains substantial mathematics.
6. Run `git diff --check` before committing.
7. Do not silently rewrite valid mathematics merely because the giant monolithic GitHub page fails to render it.
8. When an equation fails in `NOTES.MD`, first check whether the identical expression renders correctly in its smaller chronology file.
9. If the smaller file renders correctly and the live-math audit is clean, treat large-document rendering exhaustion as the leading explanation rather than changing scientifically correct mathematics.
10. Never delete historical research merely to reduce the size of the monolithic handoff file.

## Synchronization rule

The scientific content of a chronological note and its corresponding monolithic entry should remain identical.

The two representations serve different operational purposes, not different scientific purposes.

Changes to an old research note that alter scientific meaning should therefore be made deliberately and propagated to both representations.

Pure navigation material may differ where necessary, but the actual research record should not drift.

## Authority and interpretation

The two notes representations are historical and carry-forward records.

They do not supersede the project's authority hierarchy.

The active scientific frontier, branch ranking, decision gates, and stop rules remain governed by `RESEARCH_BUILDPLAN.md`.

Durable completed proofs, falsifications, and major research slices remain preserved in `journal/`.

The README remains the concise public-facing project state.

The codebundle remains the authoritative representation of current source code, tests, simulations, and implementation state.

## Permanent policy summary

MONOLITHIC_NOTES=

PRESERVE

MONOLITHIC_NOTES_PURPOSE=

SINGLE_FILE_HISTORY_AND_AI_SESSION_HANDOFF

CHRONOLOGY_NOTES=

PRESERVE

CHRONOLOGY_NOTES_PURPOSE=

GITHUB_READING_AND_RELIABLE_MATH_RENDERING

NEW_CARRY_FORWARD_NOTES=

ADD_TO_BOTH_FORMS

SCIENTIFIC_CONTENT_BETWEEN_FORMS=

KEEP_SYNCHRONIZED

VALID_MATH_FAILING_ONLY_IN_GIANT_MONOLITH=

CHECK_SMALL_CHRONOLOGY_VERSION_BEFORE_REWRITING

ACTIVE_FRONTIER_AUTHORITY=

RESEARCH_BUILDPLAN.md

DURABLE_COMPLETED_RESULT_AUTHORITY=

journal/

### END NOTE - AUGUST 29 2026 - DUAL NOTES FORMAT POLICY

