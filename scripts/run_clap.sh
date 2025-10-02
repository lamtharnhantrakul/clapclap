#!/bin/bash
# CLAP Similarity Runner
# Runs CLAP similarity calculation in Docker container and saves results to file

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <audio_file> <text_file> [output_file]"
    echo ""
    echo "Arguments:"
    echo "  audio_file   - Path to audio file"
    echo "  text_file    - Path to text description file"
    echo "  output_file  - (Optional) Path to output results file (default: clap_result.txt)"
    echo ""
    echo "Example:"
    echo "  $0 data/piano_and_beats.mp3 data/positive_example.txt results.txt"
    exit 1
fi

AUDIO_FILE="$1"
TEXT_FILE="$2"
OUTPUT_FILE="${3:-clap_result.txt}"

# Check if files exist
if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file not found: $AUDIO_FILE"
    exit 1
fi

if [ ! -f "$TEXT_FILE" ]; then
    echo "Error: Text file not found: $TEXT_FILE"
    exit 1
fi

# Get absolute paths
AUDIO_ABS=$(cd "$(dirname "$AUDIO_FILE")" && pwd)/$(basename "$AUDIO_FILE")
TEXT_ABS=$(cd "$(dirname "$TEXT_FILE")" && pwd)/$(basename "$TEXT_FILE")
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
if [ ! -d "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="."
fi
OUTPUT_ABS=$(cd "$OUTPUT_DIR" && pwd)/$(basename "$OUTPUT_FILE")

# Get relative paths from current directory
SCRIPT_DIR=$(pwd)
AUDIO_REL="${AUDIO_ABS#$SCRIPT_DIR/}"
TEXT_REL="${TEXT_ABS#$SCRIPT_DIR/}"

echo "Running CLAP similarity calculation..."
echo "Audio: $AUDIO_FILE"
echo "Text: $TEXT_FILE"
echo "Output: $OUTPUT_FILE"
echo ""

# Run Docker container and capture output
docker-compose run --rm clap-run python clap_similarity.py \
    "/app/$AUDIO_REL" \
    "/app/$TEXT_REL" \
    --no-cuda > "$OUTPUT_ABS" 2>&1

# Check if successful
if [ $? -eq 0 ]; then
    echo "✓ Results saved to: $OUTPUT_ABS"
    echo ""
    echo "--- Results ---"
    cat "$OUTPUT_ABS"
else
    echo "✗ Error occurred during CLAP calculation"
    cat "$OUTPUT_ABS"
    exit 1
fi
