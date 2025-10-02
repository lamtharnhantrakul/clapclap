# Data Sanity Checks

This directory contains validation scripts and results for testing the CLAP (Contrastive Language-Audio Pretraining) model. These sanity checks ensure that CLAP correctly matches related audio-text pairs and rejects unrelated ones.

## Purpose

These scripts verify that:
1. **Positive Matching**: CLAP assigns high similarity scores to matching audio-text pairs
2. **Negative Matching**: CLAP assigns low similarity scores to mismatched audio-text pairs
3. **Cross-Dataset Validation**: Different types of audio (speech, music, events) are properly distinguished

## Evaluation Scripts

### Positive Match Tests

These scripts test CLAP on matching audio-description pairs within each dataset:

#### `evaluate_dcase.py`
- **Tests**: 35 DCASE audio event samples against their descriptions
- **Expected Scores**: High similarity (0.40-0.69, mean ~0.52)
- **Output**: `dcase_results.txt`
- **Example Match**: "buzzer ringing" audio → "a buzzer is ringing with water in the background"

#### `evaluate_librispeech.py`
- **Tests**: 20 LibriSpeech speech samples against their audio descriptions
- **Expected Scores**: High similarity (0.43-0.67, mean ~0.54)
- **Output**: `librispeech_results.txt`
- **Example Match**: Male speech audio → "a man speaking with a well-articulated voice while reading from a book"

#### `evaluate_musiccaps.py`
- **Tests**: 5 MusicCaps music samples against their descriptions
- **Expected Scores**: Moderate-high similarity (0.21-0.52, mean ~0.38)
- **Output**: `musiccaps_results.txt`
- **Example Match**: Ballad audio → "ballad song with sustained strings, mellow piano melody and soft female vocal"

### Negative Sample Tests

These scripts test CLAP on mismatched audio-description pairs across different datasets:

#### `test_negative_samples.py` (DCASE description)
- **Tests**: DCASE audio event description against LibriSpeech (speech) and MusicCaps (music) audio
- **Expected Scores**: Low similarity (mean ~0.17)
- **Output**: `negative_sample_test_results.txt`
- **Validates**: Audio event descriptions should NOT match speech or music

#### `test_negative_samples_musiccaps.py` (MusicCaps description)
- **Tests**: Music description against LibriSpeech (speech) and DCASE (audio events) audio
- **Expected Scores**: Very low similarity (mean ~0.09)
- **Output**: `negative_sample_musiccaps_test_results.txt`
- **Validates**: Music descriptions should NOT match speech or audio events

#### `test_negative_samples_librispeech.py` (LibriSpeech description)
- **Tests**: Speech description against MusicCaps (music) and DCASE (audio events) audio
- **Expected Scores**: Low similarity (mean ~0.06)
- **Output**: `negative_sample_librispeech_test_results.txt`
- **Validates**: Speech descriptions should NOT match music or audio events

## Result Files

Each `.txt` file contains:

### 1. Individual Results
```
<filename>: <similarity_score> - <description>
```

Example:
```
dev_001.wav: 0.5234 - a buzzer is ringing with water in the background
```

### 2. Summary Statistics
```
Number of samples: 35
Mean similarity: 0.5234
Std deviation: 0.0854
Min similarity: 0.4012
Max similarity: 0.6891
Median similarity: 0.5123
```

## How to Run

All scripts should be run in Docker to ensure consistent environment:

```bash
# Positive match tests
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_dcase.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_librispeech.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_musiccaps.py

# Negative sample tests
docker-compose run --rm clap-run python3 /app/data_sanity_checks/test_negative_samples.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/test_negative_samples_musiccaps.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/test_negative_samples_librispeech.py
```

## Understanding the Scores

### Cosine Similarity Scale
CLAP uses cosine similarity, which ranges from -1 to 1:
- **1.0**: Perfect match (identical embeddings)
- **0.0**: No relationship
- **-1.0**: Complete opposite

### Interpretation Guidelines

**Positive Matches** (same dataset):
- **> 0.4**: Good match - CLAP correctly identifies related content
- **0.2 - 0.4**: Moderate match - may need better descriptions
- **< 0.2**: Poor match - indicates potential issues

**Negative Matches** (cross-dataset):
- **< 0.1**: Excellent rejection - CLAP correctly identifies unrelated content
- **0.1 - 0.3**: Good rejection - shows clear distinction
- **> 0.3**: Weak rejection - may indicate semantic overlap or model confusion

## What Good Results Look Like

✅ **Healthy CLAP Performance**:
- Positive matches: Mean > 0.35
- Negative matches: Mean < 0.25
- Clear separation between positive and negative scores

❌ **Potential Issues**:
- Positive matches < 0.3: Model may not understand the domain
- Negative matches > 0.3: Model may be overgeneralizing
- High variance in positive matches: Inconsistent descriptions or audio quality

## Common Use Cases

1. **Model Validation**: Verify CLAP is working correctly after installation
2. **Benchmark Comparison**: Compare different CLAP backends (msclap vs laion)
3. **Description Quality**: Test if text descriptions are sufficiently descriptive
4. **Dataset Quality**: Identify problematic audio files or mislabeled data
5. **Threshold Tuning**: Determine optimal similarity thresholds for your application
