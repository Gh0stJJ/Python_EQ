
import equalizer
from scipy.io import wavfile
import Ctrl as Ctrl
import numpy as np

def main():
    # Read the signal
    sample_rate, samples= wavfile.read('input_songs/Ghost Voices.wav')
    #samples = np.mean(samples, axis=1)
    # Create the UI
    app = Ctrl.Ctrl(samples, sample_rate)
    app.show()
    app.app.exec()
    
if __name__ == "__main__":
    main()
