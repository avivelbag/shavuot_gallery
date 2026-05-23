#!/usr/bin/env bash
# Merge driver for JSON-array files where each branch appends new objects.
# Takes the union of "ours" and "theirs", deduplicating by .id, sorted by .id.
# Invoked by git with: %O %A %B %L %P  (we only use %A "ours" and %B "theirs")
set -euo pipefail

ours="$2"
theirs="$3"

jq -s '.[0] + .[1] | unique_by(.id)' "$ours" "$theirs" > "$ours.merged"
mv "$ours.merged" "$ours"
