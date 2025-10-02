#!/usr/bin/env python3
"""
CLAP Similarity Script
Calculates similarity between audio files and text descriptions using CLAP model.
Supports both Microsoft CLAP and LAION CLAP backends.
"""

import argparse
import sys
from pathlib import Path
import torch
import numpy as np


def load_text_file(text_path: str) -> str:
    """Load text description from file."""
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def calculate_similarity_msclap(audio_path: str, text_description: str, use_cuda: bool = True):
    """Calculate similarity using Microsoft CLAP."""
    import msclap

    device = 'cuda' if use_cuda and torch.cuda.is_available() else 'cpu'
    print(f"Backend: Microsoft CLAP")
    print(f"Using device: {device}")

    # Load model
    print("Loading CLAP model...")
    model = msclap.CLAP(version='2023', use_cuda=use_cuda)

    # Get embeddings
    print("Processing audio...")
    audio_embeddings = model.get_audio_embeddings([audio_path], resample=True)

    print("Processing text...")
    text_embeddings = model.get_text_embeddings([text_description])

    # Calculate similarity (cosine similarity)
    # Normalize embeddings to ensure proper cosine similarity calculation
    audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
    text_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
    similarity = audio_norm @ text_norm.T
    similarity_score = float(similarity[0][0])

    return similarity_score


def calculate_similarity_laion(audio_path: str, text_description: str, use_cuda: bool = True):
    """Calculate similarity using LAION CLAP."""
    import laion_clap

    device = 'cuda' if use_cuda and torch.cuda.is_available() else 'cpu'
    print(f"Backend: LAION CLAP")
    print(f"Using device: {device}")

    # Load model
    print("Loading CLAP model...")
    model = laion_clap.CLAP_Module(enable_fusion=False, device=device)
    model.load_ckpt()  # Downloads model on first run, cached afterwards

    # Get embeddings
    print("Processing audio...")
    audio_embed = model.get_audio_embedding_from_filelist(
        x=[audio_path],
        use_tensor=False
    )

    print("Processing text...")
    text_embed = model.get_text_embedding(
        [text_description],
        use_tensor=False
    )

    # Calculate similarity (cosine similarity)
    # Normalize embeddings to ensure proper cosine similarity calculation
    audio_norm = audio_embed / np.linalg.norm(audio_embed, axis=1, keepdims=True)
    text_norm = text_embed / np.linalg.norm(text_embed, axis=1, keepdims=True)
    similarity = audio_norm @ text_norm.T
    similarity_score = float(similarity[0][0])

    return similarity_score


def calculate_similarity(audio_path: str, text_path: str, backend: str = 'msclap', use_cuda: bool = True):
    """Calculate similarity between audio and text using CLAP."""

    # Check if files exist
    if not Path(audio_path).exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if not Path(text_path).exists():
        print(f"Error: Text file not found: {text_path}", file=sys.stderr)
        sys.exit(1)

    # Load text description
    text_description = load_text_file(text_path)
    print(f"Audio file: {audio_path}")
    print(f"Text description: {text_description}")
    print("-" * 60)

    # Calculate similarity based on backend
    try:
        if backend == 'msclap':
            similarity_score = calculate_similarity_msclap(audio_path, text_description, use_cuda)
        elif backend == 'laion':
            similarity_score = calculate_similarity_laion(audio_path, text_description, use_cuda)
        else:
            print(f"Error: Unknown backend '{backend}'. Use 'msclap' or 'laion'.", file=sys.stderr)
            sys.exit(1)

        print("-" * 60)
        print(f"Similarity Score: {similarity_score:.4f}")
        print("-" * 60)

        return similarity_score

    except Exception as e:
        print(f"Error during similarity calculation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate CLAP similarity between audio and text"
    )
    parser.add_argument(
        "audio_file",
        type=str,
        help="Path to audio file"
    )
    parser.add_argument(
        "text_file",
        type=str,
        help="Path to text description file"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="msclap",
        choices=["msclap", "laion"],
        help="CLAP backend to use (default: msclap)"
    )
    parser.add_argument(
        "--no-cuda",
        action="store_true",
        help="Disable CUDA and use CPU"
    )

    args = parser.parse_args()

    calculate_similarity(
        args.audio_file,
        args.text_file,
        backend=args.backend,
        use_cuda=not args.no_cuda
    )


if __name__ == "__main__":
    main()
