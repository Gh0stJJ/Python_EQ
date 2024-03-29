
import string
from pyparsing import Any
from scipy.io import wavfile as wav
from scipy.signal import lfilter, butter

import numpy as np

def filtro_pasabanda(lowFreq:float, highFreq:float)-> Any:
    b, a = butter(4, [lowFreq, highFreq], btype='band')
    return b, a


def equalizer(data,samplerate:int,gain_sub_bass:float,gain_bass:float,gain_low_mid:float,gain_upper_mid:float,gain_presence:float,gain_brilliance:float):
    lim_nyquist = samplerate/2 # Nyquist frequency

    # Sub Bass Filter (16Hz - 60Hz) set up 
    lowFreq = 16/lim_nyquist
    highFreq = 60/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)#Filtro pasabanda de orden 4
    sub_bass = lfilter(b, a, data) #Dividir el espectro de audio  en bandas de frecuencia

    # Bass Filter (60Hz - 250Hz) set up
    lowFreq = 60/lim_nyquist
    highFreq = 250/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)
    bass = lfilter(b, a, data) #Aplicar el filtro a la señal de audio

    # Low Mid Filter (250Hz - 2kHz) set up
    lowFreq = 250/lim_nyquist
    highFreq = 2000/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)
    low_mid = lfilter(b, a, data)

    # Upper Mid Filter (2kHz - 4kHz) set up
    lowFreq = 2000/lim_nyquist
    highFreq = 4000/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)
    upper_mid = lfilter(b, a, data)

    # Presence Filter (4kHz - 6kHz) set up
    lowFreq = 4000/lim_nyquist
    highFreq = 6000/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)
    presence = lfilter(b, a, data)

    # Brilliance Filter (6kHz - 16kHz) set up
    lowFreq = 6000/lim_nyquist
    highFreq = 16000/lim_nyquist
    b, a = filtro_pasabanda(lowFreq,highFreq)
    brilliance = lfilter(b, a, data)

    # Gain in dB
    #Convertir los decibeles en factores de amplificación
    #Para ello se utiliza la siguiente formula: gain=10^(dB/20)
    gain_sub_bass = 10**(gain_sub_bass/20)
    gain_bass = 10**(gain_bass/20)
    gain_low_mid = 10**(gain_low_mid/20)
    gain_upper_mid = 10**(gain_upper_mid/20)
    gain_presence = 10**(gain_presence/20)
    gain_brilliance = 10**(gain_brilliance/20)

    # Apply gain
    sub_bass=np.multiply(sub_bass, gain_sub_bass)
    bass = bass*gain_bass
    low_mid = low_mid*gain_low_mid
    upper_mid = upper_mid*gain_upper_mid
    presence = presence*gain_presence
    brilliance = brilliance*gain_brilliance

    # Sum all bands
    return sub_bass + bass + low_mid + upper_mid + presence + brilliance


#Frequency domain equalizer
def equalizer_freq(data,samplerate:int,gain_sub_bass:float,gain_bass:float,gain_low_mid:float,gain_upper_mid:float,gain_presence:float,gain_brilliance:float):
    nyquist = samplerate/2 # Nyquist frequency
    # Sub Bass Filter (16Hz - 60Hz) set up
    low_sub_bass = int(16/nyquist*len(data))
    high_sub_bass = int(60/nyquist*len(data))

    # Bass Filter (60Hz - 250Hz) set up
    low_bass = int(60/nyquist*len(data))
    high_bass = int(250/nyquist*len(data))

    # Low Mid Filter (250Hz - 2kHz) set up
    low_low_mid = int(250/nyquist*len(data))
    high_low_mid = int(2000/nyquist*len(data))

    # Upper Mid Filter (2kHz - 4kHz) set up
    low_upper_mid = int(2000/nyquist*len(data))
    high_upper_mid = int(4000/nyquist*len(data))

    # Presence Filter (4kHz - 6kHz) set up
    low_presence = int(4000/nyquist*len(data))
    high_presence = int(6000/nyquist*len(data))

    # Brilliance Filter (6kHz - 16kHz) set up
    low_brilliance = int(6000/nyquist*len(data))
    high_brilliance = int(16000/nyquist*len(data))

    #FT of the signal
    data_fft = np.fft.fft(data)

    # Gain in dB
    #Convertir los decibeles en factores de amplificación
    #Para ello se utiliza la siguiente formula: gain=10^(dB/20) para generar valores desde 0 a 2
    #Siendo 0 el valor de la señal original y 2 el valor de la señal amplificada
    gain_sub_bass = 10**(gain_sub_bass/20)
    gain_bass = 10**(gain_bass/20)
    gain_low_mid = 10**(gain_low_mid/20)
    gain_upper_mid = 10**(gain_upper_mid/20)
    gain_presence = 10**(gain_presence/20)
    gain_brilliance = 10**(gain_brilliance/20)

    # Gen a gains table
    #Equivalente a un filtro pasabanda
    gains = np.ones(len(data_fft))
    gains[low_sub_bass:high_sub_bass] = gain_sub_bass
    gains[low_bass:high_bass] = gain_bass
    gains[low_low_mid:high_low_mid] = gain_low_mid
    gains[low_upper_mid:high_upper_mid] = gain_upper_mid
    gains[low_presence:high_presence] = gain_presence
    gains[low_brilliance:high_brilliance] = gain_brilliance
    # Apply gain
    data_fft = data_fft*gains
    # Inverse FT
    return np.fft.ifft(data_fft)


def store_signal(data,sampe_rate:int,name:string):
    #Convert the signal to 16 bits (int16) cuz windows multimedia player only supports 16 bits int Dx
    data = np.int16(data/np.max(np.abs(data)) * 32767)

    # Store the signal in a wav file
    wav.write(name, sampe_rate, data)
    

# Discrete Time resampling
#Take samples from the signal at regular time intervals
def resample(data,samplerate:int,factor_decimacion:int):
    # Resample the signal
    print("New sampling rate ",samplerate/factor_decimacion,"Hz")
    return data[0::factor_decimacion]


#Decimate the signal
def decimate(data,samplerate:int,rate:int):
    #Calculate the new number of samples
    new_samples = int(len(data)*rate/samplerate)

    #Calculate the new time interval
    new_interval = int(samplerate/rate)

    #Decimate the signal
    return decimate(data, new_interval, ftype='fir', zero_phase=True)[0:new_samples]

#Anti-aliasing filter for avoid distortion after decimation
def anti_aliasing_filter(data,sampling_rate:int,new_sampling_rate:int):
    # Cut-off frequency of the filter
    cutoff_freq = (new_sampling_rate/2) / (sampling_rate/2)
    # Low-pass filter
    b, a = butter(5, cutoff_freq, btype='low')
    # Apply the filter to the signal
    return lfilter(b, a, data)


