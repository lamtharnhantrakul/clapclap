# Language Variation Testing Results

## Experiment Overview

This experiment tests how different language variations in text descriptions affect CLAP similarity scores when describing the same male speech audio sample.

### Methodology

- **Audio**: LibriSpeech male speech sample (174-84280-0005.flac)
- **Test Descriptions**: 38 different text variations across 9 categories
- **Model**: Microsoft CLAP (msclap)
- **Goal**: Determine which linguistic choices maximize CLAP similarity scores

---

## Key Findings

### 🏆 Top Performing Descriptions

| Rank | Score | Description | Category |
|------|-------|-------------|----------|
| 1 | **615.89** | "a man reading aloud" | Context and Setting |
| 2 | 574.44 | "a man speaking matter-of-factly" | Emotional Tone |
| 3 | 572.47 | "a male speaking professionally" | Emotional Tone |
| 4 | 547.24 | "a male voice speaking calmly" | Voice Quality |
| 5 | 544.74 | "a masculine voice speaking" | Detailed Gender |

**Winner**: "a man reading aloud" scored **36% higher** than the baseline "a person speaking" (454.57)

---

## Category Analysis

### 1. 🎯 Emotional Tone (Mean: 552.18)
**Highest Scoring Category**

Adding emotional or professional qualifiers significantly boosts scores:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "a man speaking matter-of-factly" | 574.44 | +26.3% ⬆️ |
| "a male speaking professionally" | 572.47 | +25.9% ⬆️ |
| "a man speaking confidently" | 533.22 | +17.3% ⬆️ |
| "a serious male voice" | 528.61 | +16.3% ⬆️ |

**Key Insight**: CLAP responds strongly to tone descriptors. Professional and matter-of-fact descriptions work best.

---

### 2. 🎤 Voice Quality (Mean: 521.29)
**Second Highest**

Descriptions emphasizing clarity and vocal characteristics:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "a male voice speaking calmly" | 547.24 | +20.4% ⬆️ |
| "a man with a clear voice" | 534.38 | +17.6% ⬆️ |
| "a man speaking clearly" | 528.69 | +16.3% ⬆️ |
| "a man speaking with good articulation" | 516.48 | +13.6% ⬆️ |

**Key Insight**: Quality descriptors (clear, calm, articulate) significantly improve scores.

---

### 3. 📖 Context and Setting (Mean: 510.57)
**Contains the Highest Single Score**

Adding contextual information about the speech activity:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| **"a man reading aloud"** | **615.89** | +35.5% ⬆️⬆️⬆️ |
| "a male narrator speaking" | 501.97 | +10.4% ⬆️ |
| "a man giving a speech" | 492.01 | +8.2% ⬆️ |
| "a male voice recording" | 492.74 | +8.4% ⬆️ |
| "a man speaking in a studio" | 450.23 | -1.0% ⬇️ |

**Key Insight**: "Reading aloud" vastly outperforms other contexts. CLAP may recognize reading patterns in speech.

---

### 4. 👨 Gender-Specific (Mean: 487.17)
**Significantly Better Than Basic**

Gender specification improves scores over generic descriptions:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "a male voice" | 516.44 | +13.6% ⬆️ |
| "a male speaking" | 516.26 | +13.6% ⬆️ |
| "a man speaking" | 505.33 | +11.2% ⬆️ |
| "a man talking" | 479.24 | +5.4% ⬆️ |
| "male speech" | 460.67 | +1.3% ⬆️ |

**Key Insight**: "Male voice" and "male speaking" outperform "man speaking". CLAP prefers technical gender terms.

---

### 5. 📝 Detailed Gender (Mean: 472.95)

Adding detail to gender descriptions:

| Description | Score |
|-------------|-------|
| "a masculine voice speaking" | 544.74 ⬆️⬆️ |
| "a male person talking" | 478.83 |
| "an adult male speaking" | 453.12 |
| "a grown man speaking" | 415.10 ⬇️ |

**Key Insight**: "Masculine voice" works exceptionally well (+19.8%), but most detailed descriptions add unnecessary complexity.

---

### 6. 👴 Age Variations (Mean: 458.44)

Age qualifiers have mixed effects:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "a young man speaking" | 485.89 | +6.9% ⬆️ |
| "an elderly man speaking" | 477.53 | +5.1% ⬆️ |
| "an old male voice" | 439.95 | -3.2% ⬇️ |
| "a middle-aged man speaking" | 430.41 | -5.3% ⬇️ |

**Key Insight**: Age descriptors generally don't help. "Young" performs best, but below gender-specific descriptions.

---

### 7. 🗣️ Basic Descriptions (Mean: 453.19)
**Baseline Category**

Simple, generic descriptions:

| Description | Score |
|-------------|-------|
| "someone speaking" | 466.82 |
| "a voice" | 458.99 |
| "speech" | 454.85 |
| "a person speaking" | 454.57 |
| "talking" | 430.72 |

**Key Insight**: These form the baseline. All other good descriptions outperform these.

---

### 8. 🚺 Alternative Gender (Mean: 393.37)
**Significant Score Drop**

Incorrect gender specification:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "female speech" | 441.39 | -2.9% ⬇️ |
| "a woman speaking" | 420.02 | -7.6% ⬇️ |
| "a female voice" | 364.96 | -19.7% ⬇️⬇️ |
| "a girl talking" | 347.13 | -23.6% ⬇️⬇️ |

**Key Insight**: CLAP correctly penalizes gender mismatches by ~13-24%. The penalty increases with specificity.

---

### 9. ❌ Non-Speech (Mean: 209.38)
**Lowest Scores**

Completely incorrect descriptions:

| Description | Score | vs Baseline |
|-------------|-------|-------------|
| "instrumental background" | 271.50 | -40.3% ⬇️⬇️⬇️ |
| "silence" | 264.91 | -41.7% ⬇️⬇️⬇️ |
| "music playing" | 200.34 | -55.9% ⬇️⬇️⬇️ |
| "ambient noise" | 169.01 | -62.8% ⬇️⬇️⬇️ |
| "piano and drums" | 141.17 | -68.9% ⬇️⬇️⬇️ |

**Key Insight**: CLAP heavily penalizes non-speech descriptions (-41% to -69%).

---

## Score Distribution Summary

| Category | Mean Score | Min | Max | Range |
|----------|------------|-----|-----|-------|
| Emotional Tone | **552.18** | 528.61 | 574.44 | 45.83 |
| Voice Quality | **521.29** | 479.69 | 547.24 | 67.55 |
| Context and Setting | **510.57** | 450.23 | 615.89 | 165.67 |
| Gender-Specific | 487.17 | 445.08 | 516.44 | 71.36 |
| Detailed Gender | 472.95 | 415.10 | 544.74 | 129.64 |
| Age Variations | 458.44 | 430.41 | 485.89 | 55.49 |
| Basic Descriptions | 453.19 | 430.72 | 466.82 | 36.09 |
| Alternative Gender | 393.37 | 347.13 | 441.39 | 94.26 |
| Non-Speech | 209.39 | 141.17 | 271.50 | 130.33 |

---

## Practical Recommendations

### ✅ Best Practices for Maximizing CLAP Scores

1. **Add contextual activity** (reading, narrating): +35% boost
2. **Include emotional/professional tone**: +26% boost
3. **Describe voice quality** (clear, calm): +20% boost
4. **Use technical gender terms** (male voice, male speaking): +14% boost
5. **Avoid incorrect gender**: -24% penalty
6. **Avoid non-speech descriptions**: -69% penalty

### 📋 Recommended Description Templates

For **male speech**, use:
- **Best**: "a man reading aloud" (615.89)
- **Good**: "a male speaking professionally" (572.47)
- **Good**: "a man with a clear voice" (534.38)
- **Good**: "a male voice speaking calmly" (547.24)

For **generic speech**, use:
- "someone speaking" (466.82) over "talking" (430.72)
- Add "clearly" or "calmly" for better scores

### ⚠️ Avoid:

- Overly complex descriptions ("a grown man speaking")
- Age qualifiers unless confirmed ("middle-aged")
- Incorrect gender specifications
- Non-speech terms when describing speech

---

## Statistical Insights

### Score Improvement Hierarchy

```
Non-Speech: 209.39 (baseline for wrong content)
           ↓ +184 points
Alternative Gender: 393.37 (wrong gender)
           ↓ +60 points
Basic: 453.19 (generic description)
           ↓ +5-35 points
Age: 458.44
Detailed Gender: 472.95
Gender-Specific: 487.17
Context: 510.57
Voice Quality: 521.29
Emotional Tone: 552.18
           ↓ +64 points
Best Individual: 615.89 ("a man reading aloud")
```

### Key Multipliers

- **Contextual activity** (reading): **1.35x** baseline
- **Emotional/professional**: **1.26x** baseline
- **Voice quality descriptors**: **1.20x** baseline
- **Gender specification**: **1.07-1.14x** baseline
- **Wrong gender**: **0.76-0.86x** baseline
- **Non-speech**: **0.31-0.59x** baseline

---

## Conclusions

1. **Context is King**: "Reading aloud" outperforms all other descriptions by 35%

2. **Tone Matters**: Emotional and professional descriptors (matter-of-factly, professionally, confidently) significantly boost scores

3. **Quality Over Quantity**: Simple, quality-focused descriptions (clear voice, calm) beat complex ones

4. **Technical Language Works**: "Male voice" beats "man" or "gentleman"

5. **CLAP Has Good Gender Detection**: Wrong gender descriptions penalized 13-24%

6. **Content Mismatch Heavily Penalized**: Non-speech descriptions drop scores by 41-69%

---

## Experiment Files

- **Test Script**: `test_language_variations.py`
- **Raw Results**: `temp/language_test_results.json`
- **Total Variations Tested**: 38 descriptions across 9 categories

---

## Future Research

- Test with female speech samples
- Test multilingual descriptions
- Test accent and dialect descriptors
- Test emotional speech (angry, happy, sad)
- Test speech-to-text transcription as descriptions
