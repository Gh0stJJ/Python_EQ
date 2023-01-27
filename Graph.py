import matplotlib.pyplot as plt
import numpy as np

class Graph:

    def __init__(self, data, sample_rate):
        self.data = data
        self.sample_rate = sample_rate
        self.fourier = np.fft.fft(data)
        self.magnitud=self.compute_freq(data)

    def plotTimeDomain(self,state:str):
        # Plot the signal in the time domain
        
        samples_normalized = self.data / np.max(np.abs(self.data))
        time = np.arange(len(samples_normalized))
        #plt.ylim(-2**15,2**15)
        plt.figure(figsize=(15,3))
        plt.plot(time, samples_normalized, label='Original',color='red') if state == "input" else plt.plot(self.data, label='Original',color='green')
        plt.title(f'Señal original con fs a {self.sample_rate} Hz') if state == "input" else plt.title(f'Señal muestreada a {self.sample_rate} Hz')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        #plt.legend()
        #save the plot
        plt.savefig("UI/time_domain_"+state+".png")

    def get_coef(self,n):
        return self.fourier[n] #Returns Xn 
        #Coeficiente de Fourier
    
    def compute_freq(self,xs):
        mag=[]
        N = len(xs)
        for n in range(int(N/2)):  #Limite de Nyquist Tomamos la mitad del sample rate
            mag.append(np.abs(self.get_coef(n))*2)
        return(mag)

    def fix_Hz_interp(self,ks,tasa_muestreo,Npoints):
        freq_Hz = ks*tasa_muestreo/Npoints
        freq_Hz  = [int(i) for i in freq_Hz ] 
        return(freq_Hz )
    

    def plotFrequencyDomain(self,state:str):
        # Plot the signal in the frequency domain
        fixed_magnitud = self.magnitud[50000:]
        ks   = np.linspace(0,len(self.magnitud),10)
        ksHz = self.fix_Hz_interp(ks,self.sample_rate,len(self.magnitud))
        plt.figure()

        plt.plot(fixed_magnitud,color='red') if state == "input" else plt.plot(fixed_magnitud,color='green')
        plt.xticks(ks,ksHz)
        plt.title("Dominio de la frecuencia")
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud")
        plt.savefig("UI/frequency_domain_"+state+".png")

    '''def plotSpectrogram(self):
        # Plot the spectrogram
        plt.figure()
        plt.specgram(self.data, Fs=self.sample_rate)
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.title('Spectrogram')
        #save the plot
        plt.savefig('spectrogram.png') '''

    def plotAll(self):
        self.plotTimeDomain()
        self.plotFrequencyDomain()
        self.plotSpectrogram()

    def show(self):
        plt.show()


