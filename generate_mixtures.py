#!/usr/bin/env python3
"""
Generate audio mixtures with varying music loudness levels.
Mixes speech with background music at different volume ratios.
"""

import librosa
import soundfile as sf
import numpy as np
import os


def mix_audio_at_level(speech_path, music_path, music_level, output_path):
    """
    Mix speech with background music at a specific loudness level.

    Args:
        speech_path: Path to speech audio file
        music_path: Path to music audio file
        music_level: Volume multiplier for music (0.0 to 1.0+)
        output_path: Path to save mixed audio
    """
    # Load both audio files
    speech, sr_speech = librosa.load(speech_path, sr=None)
    music, sr_music = librosa.load(music_path, sr=None)

    # Resample to common sample rate
    target_sr = 44100
    if sr_speech != target_sr:
        speech = librosa.resample(speech, orig_sr=sr_speech, target_sr=target_sr)
    if sr_music != target_sr:
        music = librosa.resample(music, orig_sr=sr_music, target_sr=target_sr)

    # Make them the same length (use shorter duration)
    min_length = min(len(speech), len(music))
    speech = speech[:min_length]
    music = music[:min_length]

    # Mix: speech at full volume, music at specified level
    mixed = speech * 1.0 + music * music_level

    # Normalize to prevent clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 0:
        mixed = mixed / max_val * 0.95

    # Save mixed audio
    sf.write(output_path, mixed, target_sr)

    return len(mixed) / target_sr


def generate_all_mixtures(speech_path, music_path, output_dir):
    """
    Generate mixtures at various loudness levels.

    Returns:
        list: List of (music_level, output_path, duration) tuples
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Define music loudness levels to test
    # 0.0 = no music (pure speech)
    # 0.1 = very quiet background
    # 0.3 = quiet background
    # 0.5 = moderate background
    # 0.7 = loud background
    # 1.0 = equal volume
    # 1.5 = music louder than speech
    levels = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]

    mixtures = []

    print("Generating audio mixtures...")
    print("-" * 60)

    for level in levels:
        output_filename = f"mix_music_{level:.2f}.flac"
        output_path = os.path.join(output_dir, output_filename)

        duration = mix_audio_at_level(speech_path, music_path, level, output_path)

        mixtures.append({
            'music_level': level,
            'output_path': output_path,
            'duration': duration
        })

        print(f"✓ Generated: {output_filename} (music level: {level:.2f}, duration: {duration:.2f}s)")

    print("-" * 60)
    print(f"Generated {len(mixtures)} mixtures in {output_dir}")

    return mixtures


if __name__ == "__main__":
    # Paths
    speech_path = "/app/data/174-84280-0005.flac"
    music_path = "/app/data/piano_and_beats.mp3"
    output_dir = "/app/temp/mixtures"

    # Generate mixtures
    mixtures = generate_all_mixtures(speech_path, music_path, output_dir)

    # Save metadata
    import json
    metadata_path = os.path.join(output_dir, "mixtures_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(mixtures, f, indent=2)

    print(f"\nMetadata saved to: {metadata_path}")
