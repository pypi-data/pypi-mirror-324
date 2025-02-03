import wave
import pathlib
import random
import subprocess

try:
    import sounddevice
    import soundfile
except ImportError:
    sounddevice = None

from primitive_tts.en import MAP


DEBUG = False


def string_to_tokens(text):
    """
    Convert a string to a list of tokens.
    """

    # TODO: Remove non-alphabetic characters

    return text.lower().split(' ')


def word_to_chunks(word):
    """
    Break a word into chunks of 2 characters.
    """
    chunks = []

    # Even length words can be split into 2 character chunks
    if len(word) % 2 != 0:
        # Prefer 2 character chunks
        # Pick a random character to double up
        double_index = random.choice(range(len(word)))
        character = word[double_index]
        word = word[:double_index] + character + word[double_index:]

    chunks = [word[i:i + 2] for i in range(0, len(word), 2)]

    return chunks


def word_to_phonemes(word_chunks):
    """
    Return the phonemes for a word in a given language.
    """

    chunks = []

    for chunk in word_chunks:
        chunks.extend(MAP[chunk])

    return chunks


def speak(text, language='en', output_file='output.wav'):
    """
    Speak the provided text.
    """
    words = string_to_tokens(text)

    phonemes = []

    for index, word in enumerate(words):
        word_chunks = word_to_chunks(word)
        if DEBUG:
            print('word_chunks >>>', word_chunks)
        word_phonemes = word_to_phonemes(word_chunks)
        for word_phoneme in word_phonemes:
            # Avoid consecutive duplicate phonemes for smoother sound
            # This includes phonemes that end with the letter that the next phoneme starts with
            if len(phonemes) == 0 or (phonemes[-1] != word_phoneme and phonemes[-1][-1] != word_phoneme[0]):
                phonemes.append(word_phoneme)

        if index < len(words) - 1:
            phonemes.append('__')

    if DEBUG:
        print('phonemes >>>', ''.join([f'{p}-' for p in phonemes]))

    parent_dir = pathlib.Path(__file__).parent.resolve()
    sample_dir = parent_dir / 'phonemes' / language

    sample_rate = 44100  # Samples per second
    num_channels = 1  # Mono audio
    sample_width = 2  # 16-bit audio (2 bytes per sample)
    num_frames = 0  # Initially, the file is empty

    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(
            (num_channels, sample_width, sample_rate, num_frames, 'NONE', 'not compressed')
        )

        for phoneme in phonemes:
            word_file = f'{phoneme}.wav'
            wav_path = str(sample_dir / word_file)

            try:
                with wave.open(wav_path, 'rb') as wav_in:
                    if not wav_out.getnframes():
                        wav_out.setparams(wav_in.getparams())
                    wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))
            except FileNotFoundError as e:
                raise Exception(f'Entry for {word_file} does not exist') from e

        if sounddevice is None:
            # Fall back to subprocess if sounddevice is not available
            subprocess.run(['aplay', output_file])
        else:
            data, fs = soundfile.read(output_file)
            sounddevice.play(data, fs)
            sounddevice.wait()
