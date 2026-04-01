#!/usr/bin/env bash

set -euo pipefail

front_matter_value() {
  key="$1"
  file="$2"
  sed -n "/^---$/,/^---$/s/^${key}:[[:space:]]*//p" "$file" | head -n 1
}

normalise_permalink() {
  permalink="$1"
  printf '%s' "$permalink" | tr -d '"' | tr -d "'" | sed 's#^/##; s#/$##'
}

copy_posts() {
  find _posts -name "*.md" | while read -r file; do
    filename=$(basename "$file")
    slug=$(echo "${filename%.md}" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')
    dest="_site/${slug}.md"
    mkdir -p "$(dirname "$dest")"
    cp "$file" "$dest"
    echo "Copied $file -> $dest"
  done
}

copy_ways() {
  find _ways -name "*.md" | while read -r file; do
    filename=$(basename "$file")
    permalink=$(front_matter_value permalink "$file")
    if [ -n "$permalink" ]; then
      output_path=$(normalise_permalink "$permalink")
      [ -z "$output_path" ] && output_path="ways/${filename%.md}"
      dest="_site/${output_path}.md"
    else
      dest="_site/ways/${filename}"
    fi
    mkdir -p "$(dirname "$dest")"
    cp "$file" "$dest"
    echo "Copied $file -> $dest"
  done
}

copy_posts
copy_ways