#!/bin/bash

# Comprehensive script to remove -fallow-argument-mismatch from ALL compiler flags
# This will prevent the flag from being added to C compilation

echo "Removing -fallow-argument-mismatch from ALL compiler flags..."

# Find all cmake files containing the problematic flag
files=$(grep -r -l "fallow-argument-mismatch" --include="*.cmake" . 2>/dev/null)

if [ -z "$files" ]; then
    echo "No files found containing -fallow-argument-mismatch"
    exit 0
fi

count=$(echo "$files" | wc -l)
echo "Found $count files containing the flag"

# Process each file
echo "$files" | while read -r file; do
    if [ -f "$file" ]; then
        echo "Processing: $file"

        # Create a backup
        cp "$file" "$file.backup"

        # Remove the flag from ALL compiler flags (not just Fortran)
        sed -i 's/-fallow-argument-mismatch//g' "$file"

        echo "  - Updated $file"
    fi
done

echo "Done! All instances of -fallow-argument-mismatch have been removed."
echo "You can now try building again."
echo ""
echo "To restore the files later, run: find . -name '*.cmake.backup' -exec bash -c 'cp \"{}\" \"\${1%.backup}\"' _ {} \;"