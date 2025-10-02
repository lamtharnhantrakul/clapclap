# Experiment 1b: LibriSpeech + DCASE Audio Mixup (15-Second Standardized)

## Objective

This experiment evaluates whether CLAP (Contrastive Language-Audio Pretraining) can better match audio-text pairs when both the audio and text descriptions are combined, compared to individual components. **This variant uses 15-second standardized audio to control for duration effects.**

**Hypothesis**: When mixing speech audio (LibriSpeech) with environmental sounds (DCASE), a combined natural language description should yield higher CLAP similarity scores than either individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **DCASE**: Environmental sound events with descriptions (35 samples from `test_data/dcase/`)

## Methodology

1. **Audio Standardization (Key Difference from 1a)**:
   - **If audio > 15 seconds**: Take a random 15-second crop
   - **If audio < 15 seconds**: Zero-pad at the end to reach 15 seconds
   - **If audio = 15 seconds**: Use as-is
2. **Audio Mixing**: Randomly pair standardized LibriSpeech and DCASE audio files and mix them at 50/50 ratio
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
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_1b_dcase_librispeech_15s/scripts/mix_librispeech_dcase.py --num-mixtures 5
```

## Output

- `output/mix_XX_*.wav` - Mixed audio files (all exactly 15 seconds)
- `output/mix_XX_*_description.txt` - Combined text descriptions
- `output/experiment_summary.txt` - Comprehensive results with CLAP scores and statistics

## Key Parameters

- **Number of mixtures**: 5 (default, configurable with `--num-mixtures`)
- **Audio duration**: 15 seconds (standardized)
- **Mix ratio**: 50/50 (equal weighting)
- **Sample rate**: 16 kHz (all audio resampled)
- **Random seed**: 42 (for reproducibility)

## Comparison with Experiment 1a

| Aspect | Experiment 1a | Experiment 1b |
|--------|---------------|---------------|
| Duration handling | Original (variable) | Standardized to 15s |
| Padding strategy | Pad shorter to match longer | Pad to 15s or crop to 15s |
| Purpose | Test natural audio mixtures | Control for duration effects |

## Expected Insights

This controlled variant helps isolate the effect of audio duration on CLAP performance. By standardizing all audio to 15 seconds, we can better understand if compositional description matching works independently of temporal length variations, which is important for fair model evaluation and understanding CLAP's robustness to duration changes.
