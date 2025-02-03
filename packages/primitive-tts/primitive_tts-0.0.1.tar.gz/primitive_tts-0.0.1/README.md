# Primitive TTS

Primitive TTS is a text-to-speech (TTS) library intended to have as simple of an implementation as possible. Its creation was brought about by the fact that although numerous other speech synthesis libraries exist, they almost ubiquitously seem to suffer from one of the following issues:

* Complex or strict dependencies, often failing to install on various _`*nix`_ distributions
* Unclear licensing of produced voices
* Have received low, or no maintenance in several years
* The available voices don't quite fit what I'm building

In an attempt to remedy this, Primitive TTS achieves is built using:

* Minimal dependencies - [`wave`](https://docs.python.org/3/library/wave.html) audio for example is natively supported in Python
* Allows commercial use for the generated speech
* Is designed with simplicity in mind to encourage and allow for low effort of maintainability

The generated speech is far from perfect, is not high quality, **and** when a simple alternative comes along I'll switch to that.

Anecdotally, there was a period of time from 2000 to 2015 where excessive plastic housings and computer monitored hardware seemed to be rapidly encroaching around the engines and other reparable areas of both pedestrian and industrial vehicles. Not that this is fully a first hand observation, but rather what I observed through lense of my father (who is notably the main influence that led me to pursue technology as a line of work). With over 50 years experience as a mechanic working on countless different machines, he still needed additional specialized tools and training. That's where the inspiration for Primitive TTS comes in. There is a significant learning curve between a standard multimeter, and proprietary diagnostic software - not to mention the factors of price and access. I'm seeing similar themes within the current bloom of artificial intelligence. Various AI models are limited to specific brands of hardware, and have significant resource requirements (memory, GPU, etc.). I know for certain that within a few years these limitations will ebb as the software becomes more distilled and standard catches up with it. But until then I think it might help to have at least some software that can be fixed and edited easily, using standard and widely available tools.

## Design

Primitive TTS uses a set of 39 phonemes that are compatible with [The CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) - phonemes being the distinct units of sound in a given language, and represented herein by the following letter codes:

```
AA, AE, AH, AO, AW, AY, B, CH, D, DH, EH, ER, EY,
F, G, HH, IH, IY, JH, K, L , M, N, NG, OW, OY, P,
R, S, SH, T, TH, UH, UW, V, W, Y, Z, ZH
```

To generate speech, text is split into tokens (words) and each word is split into chunks consisting of two letters. For example, the word `"system"` becomes `["sy", "st", "em"]`. Each two-letter chunk is mapped to a set of phonemes, which in this example would be `[S, AY], [S, T], [AH, M]`. Speech is then produced by stitching together the `wav` files corresponding to each phoneme.

Odd length words are handled by selecting one letter at random and doubling it. This generally seems ok because there is also logic that removed duplicate consecutive phonemes before generating the combined wave file, this deduplication reduces jitter in the generated speech.

Splitting words two letter chunks results in a relatively small finite set of possible letter combinations for the 26 letters of the english language (26² = 676).

## Language Support

Currently only american english is supported, but theoretically support for other languages could be added by adding new phoneme mappings (see the `en` and `en.py` set as examples).

## Voices

This library is only going to support one "voice", which although not expressly named anywhere within the code, is refereed to as the "Salvius voice". This voice aims to be principally recognizable as _the voice of the humanoid robot, [Salvius](https://salvius.org)_.

## Installation

```bash
pip install primitive-tts
```

## Usage

```python
from primitive_tts.speech import speak

speak('system online')
```

## Samples

> "system online"

<audio controls>
  <source src="./samples/system-online.wav" type="audio/wav">
  Audio sample cannot be rendered.
</audio>

> "lorem ipsum"

<audio controls>
  <source src="./samples/lorem-ipsum.wav" type="audio/wav">
  Audio sample cannot be rendered.
</audio>

> Attention captain I have finished my analysis

<audio controls>
  <source src="./samples/attention-captain-I-have-finished-my-analysis.wav" type="audio/wav">
  Audio sample cannot be rendered.
</audio>



> The quick brown fox jumps over the lazy dog

<audio controls>
  <source src="./samples/the-quick-brown-fox-jumps-over-the-lazy-dog.wav" type="audio/wav">
  Audio sample cannot be rendered.
</audio>

