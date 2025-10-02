# Experiment 3b: LibriSpeech + DCASE + MusicCaps 3-Way Audio Mixup (15-Second Standardized)

## Objective

This experiment extends the 2-way mixup experiments by testing CLAP's ability to match audio-text pairs when **three distinct sound sources** are mixed simultaneously: speech, environmental sounds, and music. **This variant uses 15-second standardized audio to control for duration effects.**

**Hypothesis**: When mixing three audio sources (speech + environmental + music), a compositional natural language description combining all three should yield higher CLAP similarity scores than any individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **DCASE**: Environmental sound events with descriptions (35 samples from `test_data/dcase/`)
- **MusicCaps**: Music recordings with detailed descriptions (5 samples from `test_data/music_caps/`)

## Methodology

1. **Audio Standardization (Key Difference from 3a)**:
   - **If audio > 15 seconds**: Take a random 15-second crop
   - **If audio < 15 seconds**: Zero-pad at the end to reach 15 seconds
   - **If audio = 15 seconds**: Use as-is
2. **Audio Mixing**: Randomly select triplets (LibriSpeech + DCASE + MusicCaps) and mix at equal ratios (33.3% each)
3. **Description Combination**: Merge descriptions using natural language template:
   - Pattern: `"[speech] with [ambient] and [music] playing in the background"`
   - Example: `"a woman speaking with a clear voice while narrating a story with a pig is grunting with water in the background and a male voice singing over mellow piano playing in the background"`
4. **Evaluation**: Calculate CLAP similarity scores for:
   - Mixed audio ↔ Combined description
   - Mixed audio ↔ Speech-only description
   - Mixed audio ↔ DCASE-only description
   - Mixed audio ↔ Music-only description

## Running the Experiment

```bash
# From repository root
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_3b_librispeech_dcase_musiccaps_15s/scripts/mix_three_sources.py --num-mixtures 5
```

## Output

- `output/mix_XX_*.wav` - Mixed audio files (all exactly 15 seconds)
- `output/mix_XX_*_description.txt` - Combined text descriptions
- `output/experiment_summary.txt` - Comprehensive results with CLAP scores and statistics

## Key Parameters

- **Number of mixtures**: 5 (default, configurable with `--num-mixtures`)
- **Audio duration**: 15 seconds (standardized)
- **Mix ratio**: 33.3/33.3/33.4 (approximately equal 3-way weighting)
- **Sample rate**: 16 kHz (all audio resampled)
- **Random seed**: 42 (for reproducibility)

## Comparison with Experiment 3a

| Aspect | Experiment 3a | Experiment 3b |
|--------|---------------|---------------|
| Duration handling | Original (variable) | Standardized to 15s |
| Padding strategy | Pad shorter to match longest | Pad to 15s or crop to 15s |
| Purpose | Test natural audio mixtures | Control for duration effects |

## Expected Insights

This controlled 3-way mixup variant isolates the effect of audio duration when testing CLAP's limits with complex multi-source scenes. Since MusicCaps samples tend to be longer than LibriSpeech and DCASE, standardization ensures that:

1. **Fairness**: All comparisons are made on equal temporal footing
2. **Controlled complexity**: Scene complexity is due to source diversity, not duration variation
3. **Duration independence**: Tests if compositional benefits hold across consistent time windows

This is the most challenging experiment in the series, combining maximum source diversity (3 types) with controlled duration (15s), providing insights into CLAP's upper limits for compositional audio-language understanding in complex, real-world acoustic scenarios.
