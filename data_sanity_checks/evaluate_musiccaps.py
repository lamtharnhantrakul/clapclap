#!/usr/bin/env python3
"""
Evaluate CLAP similarity scores for MusicCaps test dataset.
Calculates similarity between each audio file and its corresponding description.
"""

import sys
from pathlib import Path
import numpy as np

# Add parent directory to path to import clap_similarity
sys.path.insert(0, str(Path(__file__).parent.parent))

from clap_similarity import calculate_similarity_msclap

# Dataset path - use environment-aware path
SCRIPT_DIR = Path(__file__).parent
MUSICCAPS_DIR = SCRIPT_DIR.parent / "test_data" / "music_caps"

def evaluate_musiccaps():
    """Evaluate CLAP similarity for all MusicCaps samples."""

    # Get all audio files
    audio_files = sorted(MUSICCAPS_DIR.glob("*.wav"))

    if not audio_files:
        print("Error: No audio files found in MusicCaps directory")
        return

    print(f"Evaluating {len(audio_files)} MusicCaps samples...")
    print("=" * 80)

    scores = []
    results = []

    for audio_file in audio_files:
        # Get corresponding description file with _description suffix
        text_file = audio_file.parent / f"{audio_file.stem}_description.txt"

        if not text_file.exists():
            print(f"Warning: No description file found for {audio_file.name}")
            continue

        # Read text description
        with open(text_file, 'r') as f:
            text_description = f.read().strip()

        # Calculate similarity
        import msclap
        model = msclap.CLAP(version='2023', use_cuda=False)

        audio_embeddings = model.get_audio_embeddings([str(audio_file)], resample=True)
        text_embeddings = model.get_text_embeddings([text_description])

        # Normalize and calculate cosine similarity
        audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
        text_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
        similarity = audio_norm @ text_norm.T
        similarity_score = float(similarity[0][0])

        scores.append(similarity_score)

        # Store result
        result_line = f"{audio_file.name}: {similarity_score:.4f} - {text_description}"
        results.append(result_line)

        print(f"{audio_file.name}: {similarity_score:.4f}")
        print(f"  Description: {text_description}")
        print("-" * 80)

    # Calculate statistics
    summary = []
    summary.append("=" * 80)
    summary.append("SUMMARY STATISTICS")
    summary.append("=" * 80)
    summary.append(f"Number of samples: {len(scores)}")
    summary.append(f"Mean similarity: {np.mean(scores):.4f}")
    summary.append(f"Std deviation: {np.std(scores):.4f}")
    summary.append(f"Min similarity: {np.min(scores):.4f}")
    summary.append(f"Max similarity: {np.max(scores):.4f}")
    summary.append(f"Median similarity: {np.median(scores):.4f}")
    summary.append("=" * 80)

    print("\n" + "\n".join(summary))

    # Write results to file
    output_file = SCRIPT_DIR / "musiccaps_results.txt"
    with open(output_file, 'w') as f:
        f.write(f"MusicCaps CLAP Similarity Evaluation Results\n")
        f.write(f"Evaluating {len(audio_files)} samples\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            f.write(result + "\n")

        f.write("\n")
        for line in summary:
            f.write(line + "\n")

    print(f"\nResults saved to: {output_file}")

    return scores, summary

if __name__ == "__main__":
    evaluate_musiccaps()
