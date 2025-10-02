# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CLAP (Contrastive Language-Audio Pretraining) similarity tool that calculates semantic similarity between audio files and text descriptions. It supports two backends: Microsoft CLAP (default, ~600MB) and LAION CLAP (~1.8GB).

## Development Commands

### Build and Run

```bash
# Build Docker image
docker-compose build

# Run CLAP similarity (basic)
docker-compose run --rm clap-run python clap_similarity.py /app/test_data/examples/piano_and_beats.mp3 /app/test_data/examples/positive_example.txt --no-cuda

# Use wrapper script (easier)
./scripts/run_clap.sh test_data/examples/piano_and_beats.mp3 test_data/examples/positive_example.txt output.txt

# Rebuild with fresh cache
./scripts/rebuild.sh
```

### Dataset Validation

```bash
# Evaluate DCASE dataset (35 samples)
docker-compose run --rm clap-run python data_sanity_checks/evaluate_dcase.py

# Results saved to: data_sanity_checks/dcase_results.txt
```

### Backend Selection

```bash
# Microsoft CLAP (default, recommended)
--backend msclap

# LAION CLAP (research)
--backend laion

# CPU-only mode
--no-cuda
```

## Architecture

### Core Components

**clap_similarity.py** - Main entry point with dual backend support:
- `calculate_similarity_msclap()` - Microsoft CLAP backend implementation
- `calculate_similarity_laion()` - LAION CLAP backend implementation
- Both backends use **normalized embeddings** for proper cosine similarity (-1 to 1 range)
- Embeddings are normalized using `np.linalg.norm()` before dot product calculation

**Similarity Calculation Pattern:**
```python
# Critical: Always normalize embeddings before computing similarity
audio_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
text_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
similarity = audio_norm @ text_norm.T  # Cosine similarity
```

### Directory Structure

```
clapclap/
├── clap_similarity.py          # Main script with dual backends
├── scripts/
│   ├── run_clap.sh            # Wrapper for easy execution
│   └── rebuild.sh             # Docker rebuild utility
├── data_sanity_checks/        # Dataset validation
│   └── evaluate_dcase.py      # Batch evaluation script
├── test_data/                 # Test datasets
│   ├── examples/              # Example files for testing
│   ├── dcase/                 # DCASE samples (audio + text pairs)
│   └── librispeech/           # LibriSpeech samples (speech + transcriptions)
└── Dockerfile                 # Includes test_data and data_sanity_checks
```

### Docker Architecture

- **Volume Mount**: Current directory (`.`) is mounted to `/app` in container
- **Model Cache**: CLAP models cached in Docker volume `clap-model-cache` (persists across runs)
- **Build Context**: Dockerfile copies `test_data/` and `data_sanity_checks/` into image
- **No separate data volume**: All test data accessed via main mount

### Dataset Validation Pattern

Scripts in `data_sanity_checks/` follow this pattern:
1. Import from parent: `sys.path.insert(0, str(Path(__file__).parent.parent))`
2. Use relative paths: `SCRIPT_DIR.parent / "test_data" / "dataset_name"`
3. Batch process all samples with same model instance
4. Save results to text file in same directory
5. Output summary statistics (mean, std, min, max, median)

## Key Implementation Details

### Cosine Similarity Normalization

**Critical**: Both CLAP backends require explicit normalization of embeddings. Raw dot product is incorrect. The normalized calculation ensures scores are in [-1, 1] range:

```python
# Wrong (produces unnormalized scores)
similarity = audio_embeddings @ text_embeddings.T

# Correct (produces proper cosine similarity)
audio_norm = audio_embeddings / np.linalg.norm(audio_embeddings, axis=1, keepdims=True)
text_norm = text_embeddings / np.linalg.norm(text_embeddings, axis=1, keepdims=True)
similarity = audio_norm @ text_norm.T
```

### Test Data Organization

- `test_data/examples/` - Manual test files (piano_and_beats.mp3, positive/negative examples)
- `test_data/dcase/` - 20 randomly sampled DCASE audio event files with descriptions
- `test_data/librispeech/` - 20 randomly sampled LibriSpeech speech files with transcriptions
- Each audio file has corresponding `.txt` file with same basename

### Wrapper Script Behavior

`scripts/run_clap.sh`:
- Converts relative paths to absolute paths
- Extracts relative path from repo root for Docker
- Runs container with `/app/$RELATIVE_PATH`
- Captures stdout/stderr to output file
- Always uses `--no-cuda` flag

## Typical Similarity Score Ranges

Based on DCASE validation (35 samples):
- Mean: ~0.52
- Range: 0.40 - 0.69
- Negative examples: ~0.002

Interpretation:
- \> 0.3: High similarity (good match)
- 0.1 - 0.3: Moderate similarity
- < 0.1: Low similarity (poor match)

## When Adding New Features

### Adding Dataset Validation
1. Create script in `data_sanity_checks/`
2. Follow import pattern: `sys.path.insert(0, str(Path(__file__).parent.parent))`
3. Use relative paths from script directory
4. Save results to `.txt` file in same directory
5. Output summary statistics

### Adding New Test Data
1. Place in appropriate `test_data/` subdirectory
2. Ensure audio files have matching `.txt` files
3. Update Dockerfile if needed (currently copies all test_data/)
4. Rebuild Docker image to include new data

### Modifying CLAP Backends
- Always normalize embeddings before computing similarity
- Both backends use numpy arrays, not tensors, for final calculation
- Microsoft CLAP: `model.get_audio_embeddings()`, `model.get_text_embeddings()`
- LAION CLAP: `model.get_audio_embedding_from_filelist()`, `model.get_text_embedding()`
