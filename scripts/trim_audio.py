#!/usr/bin/env python3
"""
Trim audio files to maximum 2 minutes duration.
Leaves shorter files untouched.
"""

import subprocess
from pathlib import Path
import os

# Use environment variable for target directory, default for Docker
TARGET_DIR = Path(os.environ.get("TARGET_DIR", "/app/test_data/music_caps"))
MAX_DURATION = 120  # 2 minutes in seconds

def get_duration(audio_file):
    """Get duration of audio file using ffprobe."""
    cmd = [
        'ffprobe',
        '-i', str(audio_file),
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0

def trim_audio(input_file, output_file, duration):
    """Trim audio file to specified duration."""
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-t', str(duration),
        '-c', 'copy',  # Copy codec without re-encoding when possible
        '-y',  # Overwrite output file
        str(output_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_audio_files():
    """Process all audio files in target directory."""

    if not TARGET_DIR.exists():
        print(f"Error: Directory {TARGET_DIR} does not exist")
        return

    wav_files = sorted(TARGET_DIR.glob("*.wav"))

    print(f"Found {len(wav_files)} WAV files in {TARGET_DIR}")
    print("=" * 80)

    trimmed_count = 0
    skipped_count = 0

    for wav_file in wav_files:
        duration = get_duration(wav_file)

        print(f"\n{wav_file.name}")
        print(f"  Duration: {duration:.2f}s ({duration/60:.2f}min)")

        if duration > MAX_DURATION:
            # Create temporary file for trimmed version
            temp_file = wav_file.parent / f"{wav_file.stem}_temp.wav"

            print(f"  ⚠ Exceeds {MAX_DURATION}s - trimming to 2 minutes...")

            if trim_audio(wav_file, temp_file, MAX_DURATION):
                # Replace original with trimmed version
                temp_file.replace(wav_file)
                print(f"  ✓ Trimmed to {MAX_DURATION}s")
                trimmed_count += 1
            else:
                print(f"  ✗ Failed to trim")
                if temp_file.exists():
                    temp_file.unlink()
        else:
            print(f"  ✓ Under {MAX_DURATION}s - no trimming needed")
            skipped_count += 1

    print("\n" + "=" * 80)
    print(f"✓ Processed {len(wav_files)} files")
    print(f"  Trimmed: {trimmed_count}")
    print(f"  Skipped: {skipped_count}")

if __name__ == "__main__":
    process_audio_files()
