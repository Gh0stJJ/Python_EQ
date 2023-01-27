
import equalizer
from scipy.io import wavfile
import Ctrl as Ctrl
import numpy as np

def main():
    # Read the signal
    sample_rate, samples= wavfile.read('input_songs/Ghost Voices.wav')
    samples = (samples[:,0] + samples[:,1]) / 2 # Stereo to mono
    # Create the UI
    app = Ctrl.Ctrl(samples, sample_rate)
    app.show()
    app.app.exec()
    
if __name__ == "__main__":
    main()
