# Experiment 2b: LibriSpeech + MusicCaps Audio Mixup (15-Second Standardized)

## Objective

This experiment evaluates whether CLAP can effectively match combined audio-text pairs when mixing speech with music, with **15-second standardized audio to control for duration effects**.

**Hypothesis**: When mixing speech audio (LibriSpeech) with music (MusicCaps), a combined natural language description should yield higher CLAP similarity scores than either individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **MusicCaps**: Music recordings with detailed descriptions (5 samples from `test_data/music_caps/`)

## Methodology

1. **Audio Standardization (Key Difference from 2a)**:
   - **If audio > 15 seconds**: Take a random 15-second crop
   - **If audio < 15 seconds**: Zero-pad at the end to reach 15 seconds
   - **If audio = 15 seconds**: Use as-is
2. **Audio Mixing**: Randomly pair standardized LibriSpeech and MusicCaps audio files and mix them at 50/50 ratio
3. **Description Combination**: Merge descriptions using natural language template:
   - Pattern: `"[speech description] while [music description]"`
   - Example: `"a woman speaking with a clear voice while narrating a story while The low quality recording features a ballad song that contains sustained strings, mellow piano melody and soft female vocal singing over it"`
4. **Evaluation**: Calculate CLAP similarity scores for:
   - Mixed audio ↔ Combined description
   - Mixed audio ↔ Speech-only description
   - Mixed audio ↔ Music-only description

## Running the Experiment

```bash
# From repository root
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_2b_musiccaps_librispeech_15s/scripts/mix_librispeech_musiccaps.py --num-mixtures 5
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

## Comparison with Experiment 2a

| Aspect | Experiment 2a | Experiment 2b |
|--------|---------------|---------------|
| Duration handling | Original (variable) | Standardized to 15s |
| Padding strategy | Pad shorter to match longer | Pad to 15s or crop to 15s |
| Purpose | Test natural audio mixtures | Control for duration effects |

## Expected Insights

This controlled variant isolates duration effects when testing speech+music mixtures. MusicCaps samples often have longer durations than LibriSpeech, so standardization helps determine if CLAP's performance differences are due to temporal length or inherent content complexity. This is especially relevant since music typically has sustained harmonic structure that may be affected differently by duration changes compared to transient speech.
