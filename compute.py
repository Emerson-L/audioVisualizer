from __future__ import annotations
import librosa # type: ignore
import numpy as np
import visualize

# bin number selection (use some function to map data)
# customizable frequency ranges for each bin
# SET UP GITHUB

HOP_LENGTH = 512

#frequency_bounds = [60, 100, 150, 300, 700, 1100, 1800, 2600, 3400, 4500, 5200, 6100, 15000]

#20 - 60 sub bass 40
#60 - 250 bass 190
#250 - 500 low mid 250
#500 - 2000 mid 1500
#2000 - 4000 high mid 2000
#4000 - 6000 presence 2000
#6000 - 20000 brilliance 14000

def generate_frequency_bounds() -> list[int]:
    #frequency_bounds = []

    #math

    #frequency_bounds = [0, 10, 40, 50, 70, 90, 120, 155, 203, 250, 313, 375, 438, 500, 875, 1250, 1625, 2000, 2500,
    #               3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000]

    return [0, 10, 40, 50, 70, 90, 120, 155, 203, 250, 313, 375, 438, 500, 875, 1250, 1625, 2000, 2500,
                   3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000, 12500, 15000, 17500, 20000]

def read_audio(audio_path: str) -> tuple[np.ndarray, int]:
    y, sr = librosa.load(audio_path, duration = 45, sr = 44100) #short duration for testing
    return y, sr

#Get the indices of the array of audio data that correspond with the frequencies specified by frequency_bounds
def get_bin_indices(sr: int, frequency_bounds: list[int]) -> list[int]:
    frequencies = librosa.fft_frequencies(sr=sr)
    bin_indices = []
    i = 0
    for bound in frequency_bounds:
        while frequencies[i] < bound:
            i += 1 # size of jump, higher means faster compute

        if i not in bin_indices:
            bin_indices.append(i)
        else:
            print("ditching bound at " + str(bound))

    #print(bin_indices)

    return bin_indices


#Make an array of the decibel values for each frame
def make_db_array(y: np.ndarray, sr: int, bin_indices: list[int]) -> np.ndarray:
    s = librosa.stft(y)
    db = librosa.amplitude_to_db(np.abs(s), ref=np.max)
    song_length = librosa.get_duration(y=y, sr=sr)
    timestamps = np.linspace(0.0, song_length, int(song_length * visualize.FPS))

    db_array = np.empty(shape = (timestamps.shape[0], len(bin_indices)))
    for vid_frame, timestamp in enumerate(timestamps):
        audio_frame_index = int(timestamp * sr / HOP_LENGTH)
        frame_dbs = db[:, audio_frame_index]
        for vid_bin_index, audio_bin_index in enumerate(bin_indices):
            db_array[vid_frame][vid_bin_index] = frame_dbs[audio_bin_index] + 81

    return db_array