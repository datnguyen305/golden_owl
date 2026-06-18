# Vietnamese Text-to-Speech Proposal

## 1. Problem

Text-to-Speech (TTS) converts written text into spoken audio by modeling the relationship between linguistic input and acoustic output; modern neural TTS systems commonly predict an acoustic representation such as a mel-spectrogram before generating waveform audio with a neural vocoder [1][4].

For Vietnamese, the system must generate speech with correct pronunciation and tone realization. Vietnamese has lexical tones, and tone differences involve pitch contour, duration, and phonation, so tone errors can change perceived meaning [6].

## 2. Goal

The goal is to design a Vietnamese TTS system that:

- Converts Vietnamese text into natural speech.
- Preserves Vietnamese tone marks and pronunciation.
- Handles common written forms such as numbers, dates, abbreviations, and punctuation.
- Produces waveform audio that can be saved or played.
- Can later be extended to multi-speaker or expressive speech synthesis.

## 3. Proposed Pipeline

The proposed system uses a two-stage neural TTS pipeline:

```text
Raw Vietnamese text
  -> text normalization
  -> Vietnamese text/token processing
  -> acoustic model
  -> mel-spectrogram
  -> neural vocoder
  -> waveform audio
```

This two-stage design is widely used in neural TTS: Tacotron 2 predicts mel-spectrograms from text and then uses a vocoder to synthesize waveform audio [1], while FastSpeech 2 also predicts mel-spectrograms but uses a non-autoregressive architecture for faster and more stable generation [2].

## 4. Data Preparation

The model needs paired Vietnamese data:

```text
Vietnamese transcript -> recorded speech audio
```

Example:

```text
"Xin chào, hôm nay thời tiết rất đẹp." -> audio_001.wav
```

For the first version, I recommend a clean single-speaker dataset. Single-speaker training simplifies the modeling problem because the model does not need to separate speaker identity from pronunciation, rhythm, and prosody.

Recommended audio format:

- WAV format
- 16 kHz or 22.05 kHz sample rate
- Clean recording environment
- Correct transcript-audio alignment
- Short or medium-length utterances

Clean data is important because neural TTS models directly learn pronunciation, duration, and acoustic quality from the paired text-audio examples [1][2].

## 5. Text Normalization

Vietnamese written text must be converted into a spoken form before synthesis. This is necessary because raw written text may contain symbols that are not directly pronounceable.

Examples:

```text
"Tôi có 2 con mèo." -> "Tôi có hai con mèo."
"TP.HCM" -> "thành phố Hồ Chí Minh"
"10/05/2024" -> "ngày mười tháng năm năm hai nghìn không trăm hai mươi bốn"
```

The normalization module should handle:

- Numbers
- Dates
- Money
- Units
- Abbreviations
- Acronyms
- Punctuation
- Foreign names

This step is especially important in Vietnamese because tone marks are written with diacritics, and these marks should be preserved or represented explicitly during modeling [6].

## 6. Text Representation

Two input representations are possible:

### Character-Based Input

Character-based input is simple and keeps Vietnamese tone marks directly in the text. Tacotron 2 demonstrates that character-level input can be used successfully for neural TTS in an end-to-end system [1].

### Phoneme-Based Input

Phoneme-based input can improve pronunciation control because it represents how text should be spoken instead of only how it is written. For Vietnamese, the phoneme representation should include tone information because Vietnamese tones are phonemic and affect meaning [6].

Recommended approach:

```text
Version 1: character-based Vietnamese input
Version 2: Vietnamese phoneme input with tone features
```

This keeps the first system simple while leaving a clear path for better pronunciation.

## 7. Acoustic Model Options

### Option A: Tacotron 2

Tacotron 2 is a sequence-to-sequence TTS model that predicts mel-spectrograms from text and uses a neural vocoder to generate waveform audio [1].

Advantages:

- Conceptually easy to understand.
- Produces natural speech with enough clean data.
- Strong baseline for neural TTS.

Problems:

- Autoregressive decoding is slower.
- Attention failures can cause skipped or repeated words, especially on long sentences.

### Option B: FastSpeech 2

FastSpeech 2 is a non-autoregressive TTS model that predicts mel-spectrograms using duration, pitch, and energy information [2].

Advantages:

- Faster inference than autoregressive models.
- More stable for long sentences.
- Pitch and duration modeling are useful for tonal languages like Vietnamese.
- Better suited for controllable production systems.

Problems:

- Needs duration information or an aligner.
- Training pipeline is more complex than a basic Tacotron-style baseline.

### Option C: VITS

VITS is an end-to-end TTS model using conditional variational autoencoding, normalizing flows, and adversarial training [3].

Advantages:

- High naturalness.
- End-to-end training.
- Models variation in rhythm and pitch.

Problems:

- More complex to train and debug.
- Requires careful data preparation and hyperparameter tuning.

## 8. Recommended Model

I recommend:

```text
FastSpeech 2 + HiFi-GAN
```

FastSpeech 2 is recommended because it directly models duration, pitch, and energy, which are important for natural speech rhythm and tone-sensitive languages [2]. HiFi-GAN is recommended as the vocoder because it is designed for efficient and high-fidelity waveform generation from mel-spectrograms [4].

This combination is practical because:

- FastSpeech 2 gives fast and stable acoustic prediction [2].
- HiFi-GAN generates high-quality waveform audio efficiently [4].
- The two-stage design is easier to debug than a fully end-to-end model.
- Pitch and duration features give a path to improve Vietnamese tone quality.

## 9. Problems and Solutions

### Problem 1: Vietnamese Tone Errors

Vietnamese tone is meaningful and involves acoustic properties such as pitch, duration, and phonation [6].

Solutions:

- Preserve Vietnamese diacritics during text processing.
- Add tone information in the phoneme representation.
- Use a model with pitch prediction such as FastSpeech 2 [2].
- Use clean recordings from native speakers.

### Problem 2: Limited Vietnamese Data

Neural TTS models need high-quality paired text-audio data to learn pronunciation, rhythm, and acoustic quality [1][2].

Solutions:

- Start with public Vietnamese datasets if licenses allow.
- Use transfer learning from a pretrained TTS model.
- Record a clean single-speaker dataset.
- Remove noisy or mismatched samples.

### Problem 3: Noisy Audio

Noisy audio can reduce generated speech quality because the model learns acoustic patterns from the training recordings.

Solutions:

- Remove noisy files.
- Normalize volume.
- Trim leading and trailing silence.
- Filter very short and very long utterances.
- Prefer studio-quality or clean microphone recordings.

### Problem 4: Text-Audio Misalignment

If the transcript does not match the audio, the acoustic model may learn wrong duration and pronunciation.

Solutions:

- Use forced alignment.
- Remove samples with poor alignment.
- Manually inspect a random subset.
- Keep utterances short enough for stable alignment.

### Problem 5: Numbers, Dates, and Abbreviations

Written text often contains symbols that do not directly correspond to spoken words.

Solutions:

- Build Vietnamese text normalization rules.
- Create abbreviation dictionaries.
- Convert numbers, dates, currency, and units into spoken Vietnamese before synthesis.

### Problem 6: Long Sentences

Long sentences can cause instability in autoregressive systems, including skipped or repeated content. Non-autoregressive models such as FastSpeech 2 reduce this risk by predicting in parallel instead of step by step [2].

Solutions:

- Split long text by punctuation.
- Generate audio sentence by sentence.
- Concatenate generated audio with short pauses.
- Prefer FastSpeech 2 for long-form reading.

### Problem 7: Foreign Words and Names

Vietnamese text often includes English names, brand names, and technical terms.

Solutions:

- Add a pronunciation dictionary.
- Convert common foreign words into Vietnamese-style pronunciation.
- Use character fallback for unknown words.

### Problem 8: Deployment Cost

Neural TTS can be expensive to deploy because the acoustic model and vocoder both require computation. HiFi-GAN is suitable for deployment because it is designed for efficient waveform generation [4].

Solutions:

- Use FastSpeech 2 for fast acoustic prediction [2].
- Use a lightweight HiFi-GAN vocoder [4].
- Export models to ONNX for CPU inference.
- Cache generated audio for repeated text.

## 10. Future Improvements

Future improvements:

- Multi-speaker TTS.
- Emotion or style control.
- Speaking speed control.
- Voice cloning.
- Better Vietnamese grapheme-to-phoneme conversion.
- Better text normalization.
- ONNX inference for deployment.
- Streaming TTS for long documents.

## 11. Conclusion

The proposed Vietnamese TTS system uses:

```text
FastSpeech 2 acoustic model + HiFi-GAN vocoder
```

This is a practical design because FastSpeech 2 supports fast non-autoregressive acoustic prediction with duration, pitch, and energy features [2], and HiFi-GAN provides efficient high-quality waveform generation [4]. The main technical challenges are Vietnamese tone correctness, data quality, text normalization, alignment, and deployment cost. These can be addressed with Vietnamese-specific preprocessing, clean paired data, pitch-aware modeling, and subjective listening evaluation.

## References

[1] Shen et al., "Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions" (Tacotron 2), ICASSP 2018. https://arxiv.org/abs/1712.05884

[2] Ren et al., "FastSpeech 2: Fast and High-Quality End-to-End Text to Speech", ICLR 2021. https://arxiv.org/abs/2006.04558

[3] Kim, Kong, and Son, "Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech" (VITS), ICML 2021. https://arxiv.org/abs/2106.06103

[4] Kong, Kim, and Bae, "HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis", NeurIPS 2020. https://arxiv.org/abs/2010.05646

[5] ITU-T Recommendation P.800, "Methods for subjective determination of transmission quality". https://www.itu.int/rec/T-REC-P.800/en

[6] Hwa-Froelich, D. A., Hodson, B. W., and Edwards, H. T., "Characteristics of Vietnamese Phonology", American Journal of Speech-Language Pathology, 2002. https://doi.org/10.1044/1058-0360(2002/031)
