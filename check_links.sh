#!/bin/bash

# Find all markdown files
find content -name "*.md" | while IFS= read -r file; do
  # Get the directory of the current file
  dir=$(dirname "$file")

  # Find all links in the file
  # This regex is not perfect, but it should catch most relative links to files.
  # It looks for markdown links `](link)` and captures the `link`.
  links=$(grep -oP '\]\(\K[^)]+' "$file")

  # Loop through each link
  for link in $links; do
    # Skip absolute URLs
    if [[ "$link" == "http"* ]]; then
      continue
    fi

    # Remove anchors from links
    link_no_anchor=$(echo "$link" | cut -d'#' -f1)

    # Skip empty links
    if [ -z "$link_no_anchor" ]; then
      continue
    fi

    # Skip links to directories for now
    if [[ "$link_no_anchor" == */ ]]; then
      continue
    fi

    # Construct the full path to the linked file
    # If the link starts with a /, it's relative to the content root.
    # Otherwise, it's relative to the current file's directory.
    if [[ "$link_no_anchor" == /* ]]; then
      # Note: Hugo's content paths are relative to the `content` dir, but the links are usually from the site root.
      # This logic might need to be more sophisticated depending on how permalinks are set up.
      # For now, let's assume links starting with / are relative to the project root.
      path_to_check_static="static${link_no_anchor}" # Most assets are in static
      path_to_check_content="content${link_no_anchor}" # Or maybe in content

      if [ ! -e "$path_to_check_static" ] && [ ! -e "$path_to_check_content" ]; then
        echo "Broken link in $file: $link (checked paths: $path_to_check_static, $path_to_check_content)"
      fi
    else
      path_to_check="$dir/$link_no_anchor"
      # Check if the file exists
      if [ ! -e "$path_to_check" ]; then
        echo "Broken link in $file: $link (checked path: $path_to_check)"
      fi
    fi
  done
done
