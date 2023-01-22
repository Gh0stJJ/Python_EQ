from PyQt6 import QtCore, QtWidgets
from mainWin import Ui_MainWindow



class Ctrl(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, data, sample_rate):
        super().__init__()
        self.setupUi(self)
        self.OkBtn.clicked.connect(self.btnOk_clicked)

    def btnOk_clicked(self):
        sub_bass = self.SubBass.value()
        bass = self.Bass.value()
        low_mid = self.LowMids.value()
        upper_mid = self.HighMids.value()
        presence = self.Presence.value()
        brilliance = self.Brilliance.value()
        
        # Test the all the values
        print(f"SubBass: {sub_bass} Bass: {bass} LowMid: {low_mid} UpperMid: {upper_mid} Presence: {presence} Brilliance: {brilliance}")

        

