# CLAP Similarity Tool

Calculate similarity between audio files and text descriptions using CLAP (Contrastive Language-Audio Pretraining) models.

Supports both **Microsoft CLAP** and **LAION CLAP** backends.

## 📁 Project Structure

```
clapclap/
├── clap_similarity.py          # Main CLAP similarity calculation script
├── scripts/                    # Utility scripts
│   ├── run_clap.sh            # Easy-to-use wrapper script
│   └── rebuild.sh             # Docker rebuild script
├── data_sanity_checks/        # Dataset validation tests
│   ├── evaluate_dcase.py      # DCASE dataset evaluation
│   └── dcase_results.txt      # Evaluation results
├── test_data/                 # Test datasets and examples
│   ├── examples/              # Example audio and text files
│   ├── dcase/                 # DCASE dataset samples (20 files)
│   └── librispeech/           # LibriSpeech dataset samples (20 files)
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Docker compose configuration
└── requirements.txt           # Python dependencies
```

## Prerequisites

- Docker and Docker Compose installed
- Docker daemon running

## 🚀 Quick Start

### Option 1: Using the Shell Script (Easiest)

The `run_clap.sh` script makes it simple to run CLAP similarity calculations:

```bash
./scripts/run_clap.sh <audio_file> <text_file> [output_file]
```

**Example:**
```bash
./scripts/run_clap.sh test_data/examples/piano_and_beats.mp3 test_data/examples/positive_example.txt result.txt
```

Results are automatically saved to the specified output file (or `clap_result.txt` if not specified).

### Option 2: Using Docker Compose Directly

**First time: Build the Docker image**

```bash
docker-compose build
```

**Run similarity calculation:**

```bash
docker-compose run --rm clap-run python clap_similarity.py \
    /app/test_data/examples/piano_and_beats.mp3 \
    /app/test_data/examples/positive_example.txt \
    --no-cuda
```

### Option 3: Using Python Directly (No Docker)

```bash
python clap_similarity.py <audio_file> <text_file> [--backend msclap|laion] [--no-cuda]
```

## 📊 Dataset Validation

Evaluate CLAP performance on test datasets:

```bash
# DCASE dataset evaluation (35 samples)
docker-compose run --rm clap-run python data_sanity_checks/evaluate_dcase.py
```

Results are saved to `data_sanity_checks/dcase_results.txt` with:
- Individual similarity scores for each sample
- Summary statistics (mean, std, min, max, median)

**Example Results:**
```
Mean similarity: 0.5197
Std deviation: 0.0682
Min similarity: 0.3989
Max similarity: 0.6852
```

## Backend Comparison

| Backend | Model Size | Download Speed | Performance |
|---------|-----------|----------------|-------------|
| **Microsoft CLAP** | ~600MB | Faster | Recommended for most use cases |
| **LAION CLAP** | ~1.8GB | Slower | Research-focused |

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

## Supported Audio Formats

- MP3, WAV, FLAC, OGG, and other formats supported by librosa

## Text File Format

Text files should contain a single description of the audio content:

```
piano melody with rhythmic beats and electronic drums
```

## Similarity Scores

- Scores range from **-1 to 1** (cosine similarity)
- Higher values indicate greater similarity
- Typical ranges:
  - **> 0.3**: High similarity
  - **0.1 to 0.3**: Moderate similarity
  - **< 0.1**: Low similarity

## Model Persistence

CLAP models are downloaded once and stored in a Docker volume (`clap-model-cache`). They persist across container restarts.

### Rebuild with fresh model cache

```bash
./scripts/rebuild.sh
```

Or manually:

```bash
docker volume rm clap-model-cache
docker-compose build --no-cache
```

## Troubleshooting

### Models downloading slowly
The models are large (600MB - 1.8GB). First run will take time. Subsequent runs use cached models.

### Out of memory errors
Use CPU mode with `--no-cuda` flag.

### Docker volume issues
Remove and recreate the volume:
```bash
docker volume rm clap-model-cache
docker-compose build
```

## Notes

- Model cache persists in Docker volume `clap-model-cache`
- Microsoft CLAP is recommended for most users (faster, good performance)
- LAION CLAP is recommended for research or specific model requirements
- All test data and examples are included in `test_data/` directory
