# Test Data

This directory contains test datasets for validating the CLAP (Contrastive Language-Audio Pretraining) similarity tool. Each dataset consists of audio files paired with text descriptions to test how well CLAP matches audio content with semantic descriptions.

## Datasets

### DCASE (35 samples)
**Audio Event Detection Dataset**

- **Format**: WAV files
- **Content**: Environmental sounds and audio events (buzzers, water, mechanical sounds, etc.)
- **Text Files**: `*_description.txt` - Natural language descriptions of audio events
- **Use Case**: Testing CLAP on non-speech, non-music audio events

**Example**:
- Audio: `dev_001.wav`
- Description: `dev_001_description.txt` - "a buzzer is ringing with water in the background"

### LibriSpeech (20 samples)
**Speech/Audiobook Dataset**

- **Format**: FLAC files (16kHz, mono)
- **Content**: Audiobook recordings with various speakers
- **Text Files**:
  - `*_gt_transcription.txt` - Ground truth transcription of spoken words
  - `*_description.txt` - Audio description (e.g., "a man speaking with a calm voice while reading from a book")
- **Use Case**: Testing CLAP on human speech and voice quality recognition

**Example**:
- Audio: `174-168635-0007.flac`
- Transcription: `174-168635-0007_gt_transcription.txt`
- Description: `174-168635-0007_description.txt`

### MusicCaps (5 samples)
**Music Description Dataset**

- **Format**: WAV files (16kHz, mono, trimmed to 2 minutes)
- **Content**: Various music genres and styles
- **Text Files**: `*_description.txt` - Detailed music descriptions including instruments, mood, genre
- **Use Case**: Testing CLAP on music understanding and instrument recognition

**Example**:
- Audio: `-0Gj8-vB1q4.wav`
- Description: `-0Gj8-vB1q4_description.txt` - "The low quality recording features a ballad song that contains sustained strings, mellow piano melody and soft female vocal singing over it..."

## File Naming Conventions

All datasets follow consistent naming patterns:

```
<audio_file_name>.<ext>               # Audio file
<audio_file_name>_description.txt     # Audio description
<audio_file_name>_gt_transcription.txt # Ground truth transcription (LibriSpeech only)
```

## Expected CLAP Similarity Scores

Based on validation tests:

**Positive Matches** (matching audio-text pairs):
- DCASE: Mean ~0.52 (range 0.40-0.69)
- LibriSpeech: Mean ~0.54 (range 0.43-0.67)
- MusicCaps: Mean ~0.38 (range 0.21-0.52)

**Negative Matches** (mismatched audio-text pairs):
- Cross-dataset tests: Mean ~0.04-0.25
- Indicates CLAP correctly distinguishes unrelated content

## Usage

These datasets are used by scripts in `data_sanity_checks/` to validate CLAP performance:

```bash
# Evaluate positive matches
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_dcase.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_librispeech.py
docker-compose run --rm clap-run python3 /app/data_sanity_checks/evaluate_musiccaps.py

# Test negative samples (cross-dataset)
docker-compose run --rm clap-run python3 /app/data_sanity_checks/test_negative_samples.py
```

## Dataset Sources

- **DCASE**: Detection and Classification of Acoustic Scenes and Events
- **LibriSpeech**: Open-source audiobook corpus (16kHz)
- **MusicCaps**: Music captioning dataset with YouTube audio samples
