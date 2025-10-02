#!/usr/bin/env python3
"""
Generate audio descriptions for LibriSpeech samples.
Creates description files based on transcription content and LibriSpeech characteristics.
"""

import os
from pathlib import Path
import random

# LibriSpeech characteristics
# - Read audiobook speech at 16kHz
# - Clean recordings from LibriVox project
# - Various speaking styles (narrative, dialogue, etc.)

LIBRISPEECH_DIR = Path("/Users/yaboihanoi/Code/clapclap/test_data/librispeech")

# Generic voice descriptors that can apply to any speaker
VOICE_QUALITIES = [
    "a clear voice",
    "a steady voice",
    "a measured voice",
    "an expressive voice",
    "a calm voice",
    "a narrative voice",
    "a pleasant voice",
    "a well-articulated voice"
]

RECORDING_CONTEXT = [
    "reading an audiobook",
    "reading from a book",
    "narrating a story",
    "reading aloud",
    "performing a reading"
]

def analyze_transcription(text):
    """Analyze transcription to determine appropriate voice description."""
    text_lower = text.lower()

    # Determine tone based on content
    if any(word in text_lower for word in ['illustration', 'buns', 'next man']):
        return "a neutral voice", "reading an audiobook"
    elif any(word in text_lower for word in ['metaphysic', 'subtlety', 'philosophy']):
        return "a thoughtful voice", "reading from a philosophical text"
    elif any(word in text_lower for word in ['lament', 'bitter', 'divorce', 'judgment']):
        return "a serious voice", "reading dramatically from a book"
    elif len(text.split()) < 10:
        return "a clear voice", "speaking briefly"
    else:
        # Default descriptors
        quality = random.choice(VOICE_QUALITIES)
        context = random.choice(RECORDING_CONTEXT)
        return quality, context

def generate_descriptions():
    """Generate description files for all LibriSpeech samples."""

    transcription_files = sorted(LIBRISPEECH_DIR.glob("*_gt_transcription.txt"))

    print(f"Processing {len(transcription_files)} LibriSpeech samples...")
    print("=" * 80)

    for trans_file in transcription_files:
        # Read transcription
        with open(trans_file, 'r') as f:
            transcription = f.read().strip()

        # Generate description based on content
        voice_quality, context = analyze_transcription(transcription)

        # Create description (gender-neutral, to be manually updated)
        description = f"a person speaking with {voice_quality} while {context}"

        # Create description file
        base_name = trans_file.stem.replace('_gt_transcription', '')
        desc_file = LIBRISPEECH_DIR / f"{base_name}_description.txt"

        with open(desc_file, 'w') as f:
            f.write(description)

        print(f"{base_name}:")
        print(f"  Transcription: {transcription[:60]}...")
        print(f"  Description: {description}")
        print("-" * 80)

    print(f"\n✓ Generated {len(transcription_files)} description files")

if __name__ == "__main__":
    generate_descriptions()
