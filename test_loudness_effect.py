#!/usr/bin/env python3
"""
Test the effect of background music loudness on CLAP similarity scores.
Runs CLAP similarity analysis on all generated mixtures.
"""

import os
import json
import sys
from pathlib import Path
import torch
import msclap


def calculate_clap_score(audio_path, text_description, use_cuda=False):
    """
    Calculate CLAP similarity score between audio and text.

    Args:
        audio_path: Path to audio file
        text_description: Text description to compare
        use_cuda: Whether to use CUDA

    Returns:
        float: Similarity score
    """
    # Load model
    model = msclap.CLAP(version='2023', use_cuda=use_cuda)

    # Get embeddings
    audio_embeddings = model.get_audio_embeddings([audio_path], resample=True)
    text_embeddings = model.get_text_embeddings([text_description])

    # Calculate similarity
    similarity = audio_embeddings @ text_embeddings.T
    score = float(similarity[0][0])

    return score


def test_all_mixtures(mixtures_dir, text_prompts, use_cuda=False):
    """
    Test CLAP scores for all mixtures with different text prompts.

    Args:
        mixtures_dir: Directory containing mixture audio files
        text_prompts: Dictionary of prompt names and text descriptions
        use_cuda: Whether to use CUDA

    Returns:
        dict: Results organized by prompt and music level
    """
    # Load mixture metadata
    metadata_path = os.path.join(mixtures_dir, "mixtures_metadata.json")
    with open(metadata_path, 'r') as f:
        mixtures = json.load(f)

    results = {}

    print("Testing CLAP similarity scores...")
    print("=" * 80)

    for prompt_name, prompt_text in text_prompts.items():
        print(f"\nPrompt: '{prompt_name}'")
        print(f"Text: {prompt_text}")
        print("-" * 80)

        results[prompt_name] = {
            'text': prompt_text,
            'scores': []
        }

        for mixture in mixtures:
            music_level = mixture['music_level']
            audio_path = mixture['output_path']

            # Calculate CLAP score
            score = calculate_clap_score(audio_path, prompt_text, use_cuda)

            results[prompt_name]['scores'].append({
                'music_level': music_level,
                'score': score
            })

            print(f"  Music level {music_level:4.2f}: Score = {score:8.4f}")

        print("-" * 80)

    return results


def save_results(results, output_path):
    """Save results to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)


def print_summary(results):
    """Print summary of results."""
    print("\n" + "=" * 80)
    print("SUMMARY: Effect of Background Music Loudness on CLAP Scores")
    print("=" * 80)

    for prompt_name, data in results.items():
        scores = data['scores']
        print(f"\nPrompt: '{prompt_name}'")
        print(f"Text: {data['text']}")

        # Find min, max, and range
        min_score_entry = min(scores, key=lambda x: x['score'])
        max_score_entry = max(scores, key=lambda x: x['score'])
        score_range = max_score_entry['score'] - min_score_entry['score']

        print(f"  Min score: {min_score_entry['score']:.4f} (music level: {min_score_entry['music_level']:.2f})")
        print(f"  Max score: {max_score_entry['score']:.4f} (music level: {max_score_entry['music_level']:.2f})")
        print(f"  Range: {score_range:.4f}")


if __name__ == "__main__":
    # Configuration
    mixtures_dir = "/app/temp/mixtures"
    output_path = "/app/temp/loudness_test_results.json"

    # Test prompts
    text_prompts = {
        "speech_only": "a person speaking",
        "speech_with_music": "a person speaking with piano music in the background",
        "detailed_speech_with_music": "a person speaking with the sound of piano melody with rhythmic beats and electronic drums in the background",
        "music_only": "piano melody with rhythmic beats and electronic drums",
        "ambient": "people talking in a quiet room",
    }

    # Check if CUDA is available
    use_cuda = torch.cuda.is_available() and '--no-cuda' not in sys.argv

    # Run tests
    results = test_all_mixtures(mixtures_dir, text_prompts, use_cuda)

    # Save results
    save_results(results, output_path)
    print(f"\n✓ Results saved to: {output_path}")

    # Print summary
    print_summary(results)
