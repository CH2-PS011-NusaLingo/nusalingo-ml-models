
import wave
import numpy as np

channels = 1
rates = 16000


def voice_input(filename):

  """
  Loads a sound file and returns its audio data as a NumPy array.

  Args:
    filename: The path to the sound file.

  Returns:
    A NumPy array containing the audio samples.
  """
  with wave.open(filename, "rb") as wav:
    nchannels,sampwidth,framerate  , nframes, _, _ = wav.getparams()
    frames = [wav.readframes(1) for _ in range(nframes)]
    
    audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
    # Optionally, convert to single-precision float for further processing
    # audio_data = audio_data.astype(np.float32)
  return audio_data
