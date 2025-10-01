# CLAP Similarity Tool

Calculate similarity between audio files and text descriptions using CLAP (Contrastive Language-Audio Pretraining) models.

Supports both **Microsoft CLAP** and **LAION CLAP** backends.

## Prerequisites

- Docker and Docker Compose installed
- Docker daemon running

## Quick Start

### 1. Build the Docker image (first time only)

```bash
docker-compose build
```

This will download all dependencies and set up the environment. The CLAP models will be downloaded on first run and cached for future use.

### 2. Run similarity calculation

**Using Microsoft CLAP (default, recommended):**

```bash
docker-compose run --rm clap-run python clap_similarity.py /app/data/piano_and_beats.mp3 /app/data/description.txt
```

**Using LAION CLAP:**

```bash
docker-compose run --rm clap-run python clap_similarity.py /app/data/piano_and_beats.mp3 /app/data/description.txt --backend laion
```

**CPU-only mode (disable CUDA):**

```bash
docker-compose run --rm clap-run python clap_similarity.py /app/data/piano_and_beats.mp3 /app/data/description.txt --no-cuda
```

## Backend Comparison

| Backend | Model Size | Download Speed | Performance |
|---------|-----------|----------------|-------------|
| **Microsoft CLAP** | ~600MB | Faster | Recommended for most use cases |
| **LAION CLAP** | ~1.8GB | Slower | Research-focused |

## Model Persistence

The CLAP models are downloaded once and stored in a Docker volume (`clap-model-cache`). They persist across container restarts, so you won't need to re-download them.

### Rebuild with fresh model cache

To force a rebuild and clear the cached models:

```bash
./rebuild.sh
```

Or manually:

```bash
# Remove the volume
docker volume rm clap-model-cache

# Rebuild the image
docker-compose build --no-cache
```

## Usage Examples

### Microsoft CLAP (Default)

```bash
# Compare audio with positive example
docker-compose run --rm clap-run python clap_similarity.py \
  /app/data/piano_and_beats.mp3 \
  /app/data/positive_example.txt

# Compare audio with negative example
docker-compose run --rm clap-run python clap_similarity.py \
  /app/data/piano_and_beats.mp3 \
  /app/data/negative_example1.txt
```

### LAION CLAP

```bash
# Use LAION backend
docker-compose run --rm clap-run python clap_similarity.py \
  /app/data/piano_and_beats.mp3 \
  /app/data/description.txt \
  --backend laion
```

### Compare backends

```bash
# Test with Microsoft CLAP
docker-compose run --rm clap-run python clap_similarity.py \
  /app/data/piano_and_beats.mp3 \
  /app/data/description.txt \
  --backend msclap

# Test with LAION CLAP
docker-compose run --rm clap-run python clap_similarity.py \
  /app/data/piano_and_beats.mp3 \
  /app/data/description.txt \
  --backend laion
```

## Command-Line Options

```
python clap_similarity.py <audio_file> <text_file> [options]

Positional arguments:
  audio_file            Path to audio file
  text_file             Path to text description file

Optional arguments:
  --backend {msclap,laion}
                        CLAP backend to use (default: msclap)
  --no-cuda             Disable CUDA and use CPU
  -h, --help           Show help message
```

## File Structure

- `data/` - Directory containing your audio and text files
- `clap_similarity.py` - Main script for calculating similarity
- `Dockerfile` - Container definition
- `docker-compose.yml` - Orchestration configuration
- `requirements.txt` - Python dependencies
- `rebuild.sh` - Script to rebuild with fresh cache

## Supported Audio Formats

- MP3, WAV, FLAC, OGG, and other formats supported by librosa

## Text File Format

Text files should contain a single description of the audio content, for example:

```
piano melody with drum beats in the background
```

## Similarity Scores

- Scores range from **-1 to 1**
- Higher values indicate greater similarity
- Typical ranges:
  - **> 0.3**: High similarity
  - **0.1 to 0.3**: Moderate similarity
  - **< 0.1**: Low similarity

## Troubleshooting

### Models downloading slowly

The models are large (600MB - 1.8GB). First run will take time. Subsequent runs use the cached models.

### Out of memory errors

Use CPU mode with `--no-cuda` flag.

### Docker volume issues

Remove and recreate the volume:

```bash
docker volume rm clap-model-cache
docker-compose build
```

## Notes

- Audio files are mounted read-only from the `data/` directory
- Model cache persists in Docker volume `clap-model-cache`
- Microsoft CLAP is recommended for most users (faster downloads, good performance)
- LAION CLAP is recommended for research purposes or when you need the specific model variant
