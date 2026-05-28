#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/compare_overleaf_export.sh /path/to/overleaf-export.zip [text|full]
  scripts/compare_overleaf_export.sh /path/to/unzipped/overleaf/project [text|full]

Compares an Overleaf export against the prepared local sync bundle at:
  snapshots/overleaf-sync-2026-04-16/{text-only,full}

Outputs a report directory under:
  snapshots/overleaf-compare/<timestamp>/
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

input_path=$1
profile=${2:-text}

case "$profile" in
  text) baseline_name="text-only" ;;
  full) baseline_name="full" ;;
  *)
    echo "Unknown profile: $profile" >&2
    usage
    exit 1
    ;;
esac

repo_root=$(cd "$(dirname "$0")/.." && pwd)
baseline_dir="$repo_root/snapshots/overleaf-sync-2026-04-16/$baseline_name"

if [[ ! -d "$baseline_dir" ]]; then
  echo "Baseline directory not found: $baseline_dir" >&2
  exit 1
fi

timestamp=$(date +"%Y%m%d-%H%M%S")
report_root="$repo_root/snapshots/overleaf-compare/$timestamp-$baseline_name"
export_root="$report_root/export"
diff_root="$report_root/diffs"

mkdir -p "$export_root" "$diff_root"

if [[ -d "$input_path" ]]; then
  cp -R "$input_path"/. "$export_root"/
elif [[ -f "$input_path" ]]; then
  unzip -q "$input_path" -d "$export_root/raw"
  shopt -s nullglob
  top_items=("$export_root"/raw/*)
  shopt -u nullglob
  if [[ ${#top_items[@]} -eq 1 && -d "${top_items[0]}" ]]; then
    cp -R "${top_items[0]}"/. "$export_root"/
    rm -rf "$export_root/raw"
  else
    cp -R "$export_root"/raw/. "$export_root"/
    rm -rf "$export_root/raw"
  fi
else
  echo "Input does not exist: $input_path" >&2
  exit 1
fi

summary_file="$report_root/summary.txt"
missing_file="$report_root/missing-in-export.txt"
extra_file="$report_root/extra-in-export.txt"
changed_file="$report_root/changed-files.txt"

baseline_list=$(mktemp)
export_list=$(mktemp)
trap 'rm -f "$baseline_list" "$export_list"' EXIT

(cd "$baseline_dir" && find . -type f | sed 's#^\./##' | sort) > "$baseline_list"
(cd "$export_root" && find . -type f | sed 's#^\./##' | sort) > "$export_list"

comm -23 "$baseline_list" "$export_list" > "$missing_file"
comm -13 "$baseline_list" "$export_list" > "$extra_file"
comm -12 "$baseline_list" "$export_list" > "$changed_file.tmp"

: > "$changed_file"
while IFS= read -r relpath; do
  baseline_path="$baseline_dir/$relpath"
  export_path="$export_root/$relpath"
  if ! cmp -s "$baseline_path" "$export_path"; then
    echo "$relpath" >> "$changed_file"
    case "$relpath" in
      *.tex|*.bib|*.sty|*.cls|*.cfg|*.md|*.txt)
        mkdir -p "$diff_root/$(dirname "$relpath")"
        diff -u "$export_path" "$baseline_path" > "$diff_root/$relpath.diff" || true
        ;;
    esac
  fi
done < "$changed_file.tmp"
rm -f "$changed_file.tmp"

missing_count=$(wc -l < "$missing_file" | tr -d ' ')
extra_count=$(wc -l < "$extra_file" | tr -d ' ')
changed_count=$(wc -l < "$changed_file" | tr -d ' ')
diff_count=$(find "$diff_root" -type f | wc -l | tr -d ' ')

{
  echo "Compare profile: $profile"
  echo "Baseline: $baseline_dir"
  echo "Export: $input_path"
  echo "Report: $report_root"
  echo
  echo "Missing in export: $missing_count"
  echo "Extra in export: $extra_count"
  echo "Changed files: $changed_count"
  echo "Text diffs written: $diff_count"
} > "$summary_file"

cat "$summary_file"

if [[ $changed_count -gt 0 ]]; then
  echo
  echo "Changed files:"
  cat "$changed_file"
fi
