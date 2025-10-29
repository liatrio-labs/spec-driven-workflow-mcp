#!/bin/bash

rm ~/.claude/commands/*

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "BASE_DIR: $BASE_DIR"
TAPE_FILE="${BASE_DIR}/slash-command-generator-demo.tape"
echo "TAPE_FILE: $TAPE_FILE"
OUTPUT_FILE="${BASE_DIR}/output/slash-command-generator-demo.mp4"
echo "OUTPUT_FILE: $OUTPUT_FILE"
NEW_OUTPUT_FILE="$OUTPUT_FILE"

# Run the tape
vhs "$TAPE_FILE"

# Rename the output file with a timestamp suffix before the .mp4 extension
if [ -f "${OUTPUT_FILE}" ]; then
    echo "Renaming existing output file"
    TIMESTAMP=$(date +%Y%m%d%H%M%S)
    NEW_OUTPUT_FILE="${BASE_DIR}/output/slash-command-generator-demo-${TIMESTAMP}.mp4"
    mv "${OUTPUT_FILE}" "${NEW_OUTPUT_FILE}"
fi

echo "Output file: $NEW_OUTPUT_FILE"

# Open the output file
echo "Opening output file"
if [ -f "${NEW_OUTPUT_FILE}" ]; then
    vlc "${NEW_OUTPUT_FILE}" > /dev/null 2>&1 &
    disown
else
    echo "Output file not found: $NEW_OUTPUT_FILE"
    exit 1
fi
