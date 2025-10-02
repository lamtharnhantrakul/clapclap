#!/usr/bin/env python3
"""
Convert MusicCaps MP4 files to audio and organize them in test_data.
Follows naming conventions from DCASE and LibriSpeech datasets.
"""

import subprocess
import shutil
import os
from pathlib import Path

# Use environment variable for source, default for Docker
SOURCE_DIR = Path(os.environ.get("MUSICCAPS_SOURCE", "/musiccaps"))
OUTPUT_DIR = Path("/app/test_data/music_caps")

def convert_mp4_to_wav(mp4_file, output_file):
    """Convert MP4 to WAV using ffmpeg."""
    cmd = [
        'ffmpeg',
        '-i', str(mp4_file),
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # WAV codec
        '-ar', '16000',  # 16kHz sample rate (matching LibriSpeech)
        '-ac', '1',  # Mono
        '-y',  # Overwrite output file
        str(output_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_musiccaps():
    """Process all MusicCaps files."""

    # Get all MP4 files
    mp4_files = sorted(SOURCE_DIR.glob("*.mp4"))

    print(f"Found {len(mp4_files)} MP4 files in MusicCaps directory")
    print("=" * 80)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0

    for mp4_file in mp4_files:
        video_id = mp4_file.stem

        # Convert to WAV
        wav_output = OUTPUT_DIR / f"{video_id}.wav"

        print(f"Converting {video_id}.mp4 to WAV...")
        if convert_mp4_to_wav(mp4_file, wav_output):
            print(f"  ✓ Created {wav_output.name}")

            # Copy description file with _description suffix
            rtf_file = SOURCE_DIR / f"{video_id}.rtf"
            if rtf_file.exists():
                # Read RTF and extract text content
                with open(rtf_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extract description from RTF
                try:
                    import re

                    # Find the actual text content after RTF control codes
                    # Look for text that starts with typical music description patterns
                    match = re.search(r'\\strokec3\s+(.*?)\}', content, re.DOTALL)
                    if match:
                        text = match.group(1)
                    else:
                        # Fallback: remove all RTF control codes
                        text = re.sub(r'\\[a-z]+\d*\s?', ' ', content)
                        text = re.sub(r'[{}]', '', text)

                    # Clean up whitespace
                    text = ' '.join(text.split())
                    text = text.strip()

                    # Remove any remaining RTF artifacts
                    # Remove font names and common RTF metadata
                    text = re.sub(r'\.Apple[A-Za-z]+(-[A-Za-z]+)*;?\s*', '', text)
                    text = re.sub(r'\\[*];?\s*', '', text)
                    text = re.sub(r';\s*;+', '', text)

                    # Clean up repeated separators
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()

                    # If text starts with unwanted patterns, extract the actual description
                    if text and (text[0] in ';*' or text.startswith('AppleSystem')):
                        # Find the first sentence that looks like a music description
                        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
                        for sent in sentences:
                            # Check if sentence starts with a music-related word
                            first_words = sent.split()[:3]
                            if any(word[0].isupper() and word.lower() in ['the', 'this', 'a', 'an'] or
                                   word.lower() in ['the', 'this', 'features', 'contains', 'includes']
                                   for word in first_words):
                                text = sent
                                break

                    if not text.endswith('.'):
                        text += '.'

                    # Write as plain text with _description suffix
                    desc_output = OUTPUT_DIR / f"{video_id}_description.txt"
                    with open(desc_output, 'w') as f:
                        f.write(text)

                    print(f"  ✓ Created {desc_output.name}")
                    print(f"    Description: {text[:60]}...")
                except Exception as e:
                    print(f"  ✗ Error processing description: {e}")
            else:
                print(f"  ⚠ No description file found for {video_id}")

            processed += 1
        else:
            print(f"  ✗ Failed to convert {video_id}.mp4")

        print("-" * 80)

    print(f"\n✓ Processed {processed}/{len(mp4_files)} files")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_musiccaps()
