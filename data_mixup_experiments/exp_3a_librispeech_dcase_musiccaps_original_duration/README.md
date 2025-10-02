# Experiment 3a: LibriSpeech + DCASE + MusicCaps 3-Way Audio Mixup (Original Duration)

## Objective

This experiment extends the 2-way mixup experiments by testing CLAP's ability to match audio-text pairs when **three distinct sound sources** are mixed simultaneously: speech, environmental sounds, and music.

**Hypothesis**: When mixing three audio sources (speech + environmental + music), a compositional natural language description combining all three should yield higher CLAP similarity scores than any individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **DCASE**: Environmental sound events with descriptions (35 samples from `test_data/dcase/`)
- **MusicCaps**: Music recordings with detailed descriptions (5 samples from `test_data/music_caps/`)

## Methodology

1. **Audio Mixing**: Randomly select triplets (LibriSpeech + DCASE + MusicCaps) and mix at equal ratios (33.3% each)
2. **Duration Handling**: Audio files are mixed at their original durations (no standardization)
   - Shorter files are zero-padded to match the longest file
   - Mixed audio preserves the maximum length of the three sources
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
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_3a_librispeech_dcase_musiccaps_original_duration/scripts/mix_three_sources.py --num-mixtures 5
```

## Output

- `output/mix_XX_*.wav` - Mixed audio files
- `output/mix_XX_*_description.txt` - Combined text descriptions
- `output/experiment_summary.txt` - Comprehensive results with CLAP scores and statistics

## Key Parameters

- **Number of mixtures**: 5 (default, configurable with `--num-mixtures`)
- **Mix ratio**: 33.3/33.3/33.4 (approximately equal 3-way weighting)
- **Sample rate**: 16 kHz (all audio resampled)
- **Random seed**: 42 (for reproducibility)

## Comparison with 2-Way Experiments

| Aspect | Exp 1a/2a (2-way) | Experiment 3a (3-way) |
|--------|-------------------|----------------------|
| Number of sources | 2 | 3 |
| Mix complexity | Moderate | High |
| Description length | Moderate | Long, complex |
| Real-world analogy | Podcast with music | Busy café scene |

## Expected Insights

This experiment tests CLAP's limits with highly complex audio scenes containing three simultaneous sources. Real-world audio often contains multiple overlapping sounds, so understanding how CLAP handles 3-way compositional descriptions is crucial for applications like:
- Complex scene understanding
- Multi-source audio captioning
- Audio search in rich acoustic environments
- Robustness evaluation of audio-language models

This experiment also reveals whether compositional description benefits scale with scene complexity or if there's a saturation point where individual components perform comparably.
