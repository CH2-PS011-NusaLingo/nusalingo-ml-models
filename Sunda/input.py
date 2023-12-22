# File : input.py


import wave
import numpy as np



def voice_input(filename):
    """
    Loads an audio file and returns its audio data as a NumPy array,
    ensuring consistency with the provided recording parameters.

    Args:
        filename: The path to the sound file.

    Returns:
        A NumPy array containing the audio samples.
    """

    with wave.open(filename, "rb") as wav:
        nchannels, sampwidth, framerate, nframes, _, _ = wav.getparams()

        # Verify consistency with recording parameters
        assert nchannels == 1, "Expected mono audio"
        assert framerate == 16000, "Expected sample rate of 16000"
        assert sampwidth == 2, "Expected 16-bit audio"  # 16-bit for paInt16

        frames = wav.readframes(nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)

    return audio_data


