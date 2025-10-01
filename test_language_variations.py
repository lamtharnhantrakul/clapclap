#!/usr/bin/env python3
"""
Test the effect of language variations in text descriptions on CLAP similarity scores.
Compares a male speech audio file with various text descriptions.
"""

import os
import json
import sys
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


def test_language_variations(audio_path, use_cuda=False):
    """
    Test CLAP scores for various language descriptions of male speech.

    Args:
        audio_path: Path to speech audio file
        use_cuda: Whether to use CUDA

    Returns:
        dict: Results organized by category
    """

    # Define text variations organized by category
    text_variations = {
        "Basic Descriptions": [
            "a person speaking",
            "someone speaking",
            "speech",
            "a voice",
            "talking",
        ],

        "Gender-Specific": [
            "a man speaking",
            "a male speaking",
            "a male voice",
            "a man talking",
            "male speech",
            "a gentleman speaking",
        ],

        "Detailed Gender": [
            "an adult male speaking",
            "a grown man speaking",
            "a male person talking",
            "a masculine voice speaking",
        ],

        "Voice Quality": [
            "a man speaking clearly",
            "a male voice speaking calmly",
            "a man with a clear voice",
            "a male speaking in a neutral tone",
            "a man speaking with good articulation",
        ],

        "Context and Setting": [
            "a man reading aloud",
            "a male narrator speaking",
            "a man giving a speech",
            "a male voice recording",
            "a man speaking in a studio",
        ],

        "Age Variations": [
            "a young man speaking",
            "a middle-aged man speaking",
            "an elderly man speaking",
            "an old male voice",
        ],

        "Emotional Tone": [
            "a man speaking confidently",
            "a male speaking professionally",
            "a man speaking matter-of-factly",
            "a serious male voice",
        ],

        "Alternative Gender": [
            "a woman speaking",
            "a female voice",
            "a girl talking",
            "female speech",
        ],

        "Non-Speech": [
            "music playing",
            "piano and drums",
            "instrumental background",
            "ambient noise",
            "silence",
        ],
    }

    results = {}

    print("Testing language variations for male speech...")
    print("=" * 80)
    print(f"Audio: {audio_path}")
    print("=" * 80)

    for category, variations in text_variations.items():
        print(f"\n{category}:")
        print("-" * 80)

        results[category] = {
            'descriptions': []
        }

        for text in variations:
            # Calculate CLAP score
            score = calculate_clap_score(audio_path, text, use_cuda)

            results[category]['descriptions'].append({
                'text': text,
                'score': score
            })

            print(f"  {score:8.4f} | {text}")

        # Calculate category statistics
        scores = [d['score'] for d in results[category]['descriptions']]
        results[category]['stats'] = {
            'mean': sum(scores) / len(scores),
            'min': min(scores),
            'max': max(scores),
            'range': max(scores) - min(scores)
        }

        print(f"  {'─' * 78}")
        print(f"  Category Mean: {results[category]['stats']['mean']:.4f} | "
              f"Range: {results[category]['stats']['range']:.4f}")

    return results


def save_results(results, output_path):
    """Save results to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)


def print_summary(results):
    """Print summary and analysis of results."""
    print("\n" + "=" * 80)
    print("SUMMARY: Language Variation Effects on CLAP Scores")
    print("=" * 80)

    # Find overall best and worst descriptions
    all_descriptions = []
    for category, data in results.items():
        for desc in data['descriptions']:
            all_descriptions.append({
                'category': category,
                'text': desc['text'],
                'score': desc['score']
            })

    all_descriptions.sort(key=lambda x: x['score'], reverse=True)

    print("\n🏆 TOP 10 HIGHEST SCORING DESCRIPTIONS:")
    print("-" * 80)
    for i, desc in enumerate(all_descriptions[:10], 1):
        print(f"{i:2d}. {desc['score']:8.4f} | {desc['text']}")
        print(f"    Category: {desc['category']}")

    print("\n⚠️  LOWEST 5 SCORING DESCRIPTIONS:")
    print("-" * 80)
    for i, desc in enumerate(all_descriptions[-5:], 1):
        print(f"{i:2d}. {desc['score']:8.4f} | {desc['text']}")
        print(f"    Category: {desc['category']}")

    print("\n📊 CATEGORY RANKINGS (by mean score):")
    print("-" * 80)
    category_scores = [
        (category, data['stats']['mean'])
        for category, data in results.items()
    ]
    category_scores.sort(key=lambda x: x[1], reverse=True)

    for i, (category, mean_score) in enumerate(category_scores, 1):
        print(f"{i:2d}. {mean_score:8.4f} | {category}")


if __name__ == "__main__":
    # Configuration
    audio_path = "/app/data/174-84280-0005.flac"
    output_path = "/app/temp/language_test_results.json"

    # Check if CUDA is available
    use_cuda = torch.cuda.is_available() and '--no-cuda' not in sys.argv

    # Run tests
    results = test_language_variations(audio_path, use_cuda)

    # Save results
    save_results(results, output_path)
    print(f"\n✓ Results saved to: {output_path}")

    # Print summary
    print_summary(results)
