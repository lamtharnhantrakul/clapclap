# Experiment 2a: LibriSpeech + MusicCaps Audio Mixup (Original Duration)

## Objective

This experiment evaluates whether CLAP can effectively match combined audio-text pairs when mixing speech with music, extending beyond the speech+environmental sounds tested in Experiment 1a.

**Hypothesis**: When mixing speech audio (LibriSpeech) with music (MusicCaps), a combined natural language description should yield higher CLAP similarity scores than either individual description alone.

## Dataset Sources

- **LibriSpeech**: Speech recordings with human voice descriptions (20 samples from `test_data/librispeech/`)
- **MusicCaps**: Music recordings with detailed descriptions (5 samples from `test_data/music_caps/`)

## Methodology

1. **Audio Mixing**: Randomly pair LibriSpeech and MusicCaps audio files and mix them at 50/50 ratio
2. **Duration Handling**: Audio files are mixed at their original durations (no standardization)
   - Shorter files are zero-padded to match the longer file
   - Mixed audio preserves the maximum length of the two sources
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
docker-compose run --rm clap-run python3 /app/data_mixup_experiments/exp_2a_musiccaps_librispeech_original_duration/scripts/mix_librispeech_musiccaps.py --num-mixtures 5
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

## Comparison with Experiment 1a

| Aspect | Experiment 1a | Experiment 2a |
|--------|---------------|---------------|
| Second audio source | DCASE (environmental) | MusicCaps (music) |
| Description style | Short, event-based | Long, detailed musical |
| Audio characteristics | Transient sounds | Harmonic, sustained |

## Expected Insights

This experiment tests CLAP's ability to handle speech+music mixtures, which are common in real-world scenarios (e.g., podcasts with background music, audiobooks, presentations). Music descriptions from MusicCaps are typically longer and more detailed than DCASE descriptions, providing insights into how CLAP handles compositional descriptions with varying complexity and description length.
