#!/usr/bin/env python3
"""
Sample audio files from DCASE and LibriSpeech datasets.
Creates test_data directory with randomly sampled files and their labels.
"""

import csv
import random
import shutil
from pathlib import Path

# Dataset paths
DCASE_DIR = Path("/Users/yaboihanoi/Desktop/DCASE-TASK7-2024-Open-Source/dev")
LIBRISPEECH_DIR = Path("/Users/yaboihanoi/Desktop/LibriSpeech/dev-clean")
OUTPUT_DIR = Path("/Users/yaboihanoi/Code/clapclap/test_data")

# Number of samples
NUM_SAMPLES = 20

def sample_dcase():
    """Sample 20 random files from DCASE dataset."""
    # Read caption file
    caption_file = DCASE_DIR / "caption.csv"
    audio_dir = DCASE_DIR / "audio"

    with open(caption_file, 'r') as f:
        reader = csv.DictReader(f)
        all_files = list(reader)

    # Random sample
    sampled = random.sample(all_files, NUM_SAMPLES)

    # Create output directory
    dcase_output = OUTPUT_DIR / "dcase"
    dcase_output.mkdir(parents=True, exist_ok=True)

    # Copy files and create text files
    for item in sampled:
        audio_file = item['file']
        caption = item['caption']

        # Copy audio file
        src = audio_dir / audio_file
        dst = dcase_output / audio_file
        shutil.copy2(src, dst)

        # Create text file with caption
        text_file = dcase_output / f"{Path(audio_file).stem}.txt"
        with open(text_file, 'w') as f:
            f.write(caption)

        print(f"DCASE: {audio_file} -> {caption}")

    return sampled

def sample_librispeech():
    """Sample 20 random files from LibriSpeech dataset."""
    # Find all .flac files and their transcription files
    all_audio_files = list(LIBRISPEECH_DIR.glob("*/*/*.flac"))

    # Random sample
    sampled_files = random.sample(all_audio_files, NUM_SAMPLES)

    # Create output directory
    librispeech_output = OUTPUT_DIR / "librispeech"
    librispeech_output.mkdir(parents=True, exist_ok=True)

    sampled_data = []

    for audio_file in sampled_files:
        # Get the transcription file (format: speaker-chapter.trans.txt)
        # Audio file format: speaker-chapter-utterance.flac
        speaker_chapter = '-'.join(audio_file.stem.split('-')[:2])
        trans_file = audio_file.parent / f"{speaker_chapter}.trans.txt"

        # Read transcription
        with open(trans_file, 'r') as f:
            for line in f:
                file_id, *text_parts = line.strip().split()
                if file_id == audio_file.stem:
                    transcription = ' '.join(text_parts)
                    break

        # Copy audio file
        dst = librispeech_output / audio_file.name
        shutil.copy2(audio_file, dst)

        # Create text file with transcription
        text_file = librispeech_output / f"{audio_file.stem}.txt"
        with open(text_file, 'w') as f:
            f.write(transcription)

        print(f"LibriSpeech: {audio_file.name} -> {transcription[:50]}...")
        sampled_data.append((audio_file.name, transcription))

    return sampled_data

if __name__ == "__main__":
    print("Sampling DCASE dataset...")
    print("=" * 60)
    dcase_samples = sample_dcase()

    print("\n" + "=" * 60)
    print("Sampling LibriSpeech dataset...")
    print("=" * 60)
    librispeech_samples = sample_librispeech()

    print("\n" + "=" * 60)
    print(f"Done! Files saved to {OUTPUT_DIR}")
    print(f"DCASE: {NUM_SAMPLES} files in {OUTPUT_DIR / 'dcase'}")
    print(f"LibriSpeech: {NUM_SAMPLES} files in {OUTPUT_DIR / 'librispeech'}")
