from PyQt6 import QtCore, QtWidgets, QtGui
from UI.mainWin import Ui_MainWindow
import equalizer as eq
import sys
from Graph import*
app= QtWidgets.QApplication(sys.argv)

class Ctrl(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, data, sample_rate):
        super().__init__()
        self.setupUi(self)
        self.OkBtn.clicked.connect(self.btnOk_clicked)
        self.data = data
        self.sample_rate = sample_rate
        self.graph = Graph(self.data, self.sample_rate)
       # self.graph.plotTimeDomain()
        self.graph.plotFrequencyDomain("input")
        #Initialize the plot in the label
        #self.inputFT.setPixmap(QtGui.QPixmap("UI/time_domain.png"))
        self.inputFT.setPixmap(QtGui.QPixmap("UI/frequency_domain_input.png"))
        self.app=app

    def btnOk_clicked(self):
        sub_bass = self.SubBass.value()
        bass = self.Bass.value()
        low_mid = self.LowMids.value()
        upper_mid = self.HighMids.value()
        presence = self.Presence.value()
        brilliance = self.Brilliance.value()
    
        #Initilize the sliders in 0
        sub_bass = sub_bass - 50
        bass = bass - 50
        low_mid = low_mid - 50
        upper_mid = upper_mid - 50
        presence = presence - 50
        brilliance = brilliance - 50

        #Recalculate the values to be between -12 and 12
        sub_bass = sub_bass * 0.24
        bass = bass * 0.24
        low_mid = low_mid * 0.24
        upper_mid = upper_mid * 0.24
        presence = presence * 0.24
        brilliance = brilliance * 0.24
        # Test the all the values
        print(f"SubBass: {sub_bass} Bass: {bass} LowMid: {low_mid} UpperMid: {upper_mid} Presence: {presence} Brilliance: {brilliance}")

        # Apply the equalizer
        signalEQ = eq.equalizer(self.data, self.sample_rate, sub_bass, bass, low_mid, upper_mid, presence, brilliance)
        # Store the signal
        eq.store_signal(signalEQ, self.sample_rate, "audio_equalized.wav")

        self.graph = Graph(signalEQ, self.sample_rate)
        self.graph.plotTimeDomain()
        self.graph.plotFrequencyDomain("output")
        #Initialize the plot in the label
        self.OutputFT.setPixmap(QtGui.QPixmap("UI/frequency_domain_output.png"))



