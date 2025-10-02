# Experiment 1a: LibriSpeech + DCASE Audio Mixup (Original Duration)

## Objective

This experiment evaluates whether CLAP (Contrastive Language-Audio Pretraining) can better match audio-text pairs when both the audio and text descriptions are combined, compared to individual components.

**Hypothesis**: When mixing speech audio (LibriSpeech) with environmental sounds (DCASE), a combined natural language description should yield higher CLAP similarity scores than either individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **DCASE**: Environmental sound events with descriptions (35 samples from `test_data/dcase/`)

## Methodology

1. **Audio Mixing**: Randomly pair LibriSpeech and DCASE audio files and mix them at 50/50 ratio
2. **Duration Handling**: Audio files are mixed at their original durations (no standardization)
   - Shorter files are zero-padded to match the longer file
   - Mixed audio preserves the maximum length of the two sources
3. **Description Combination**: Merge descriptions using natural language template:
   - Pattern: `"[speech description] while [ambient sound]"`
   - Example: `"a woman speaking with a clear voice while narrating a story while a pig is grunting with water in the background"`
4. **Evaluation**: Calculate CLAP similarity scores for:
   - Mixed audio ↔ Combined description
   - Mixed audio ↔ Speech-only description
   - Mixed audio ↔ DCASE-only description

## Running the Experiment

```bash
# From repository root
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_1a_dcase_librispeech_original_duration/scripts/mix_librispeech_dcase.py --num-mixtures 5
```

## Output

- `output/mix_XX_*.wav` - Mixed audio files
- `output/mix_XX_*_description.txt` - Combined text descriptions
- `output/experiment_summary.txt` - Comprehensive results with CLAP scores and statistics

## Key Parameters

- **Number of mixtures**: 5 (default, configurable with `--num-mixtures`)
- **Mix ratio**: 50/50 (equal weighting)
- **Sample rate**: 16 kHz (all audio resampled)
- **Random seed**: 42 (for reproducibility)

## Expected Insights

This experiment helps determine if CLAP's audio-text matching improves when descriptions are compositional and match the complexity of mixed audio scenes, which is crucial for applications like audio captioning, retrieval, and content understanding in real-world scenarios with multiple simultaneous sound sources.
