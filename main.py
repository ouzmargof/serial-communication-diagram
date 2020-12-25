import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QDialog, QWidget,
    QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout,
    QPushButton, QLabel, QComboBox)


class MainWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        self.initUi()
        
    def setupUi(self, Dialog):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MainWidget())
        self.setLayout(self.layout)

    def initUi(self):
        self.setWindowTitle('Serial communication diagram')
        


class MainWidget(QWidget):
    def __init__(self, ):
        super().__init__()
        
        self.data = DataModel()

        self.setupUiGroupboxData()
        self.setupUiGroupboxControl()
        self.setupUiFigure()
        self.setupUi()
        
        self.setupSlots()
        self.updateFigure()


    def setupUi(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupbox_data)
        hbox.addWidget(self.groupbox_control)

        self.layout = QVBoxLayout()
        self.layout.addLayout(hbox)
        self.layout.addWidget(self.groupbox_plot)
        self.setLayout(self.layout)


    def setupUiGroupboxData(self):
        grid = QGridLayout()
        
        lbl_char = QLabel('Charactere')
        self.cb_char = QComboBox()
        for i in range(32, 127):
            self.cb_char.addItem(chr(i))
        self.cb_char.setCurrentIndex(33)

        lbl_dec_name = QLabel('Decimal')
        lbl_bin_name = QLabel('Binary')
        lbl_hex_name = QLabel('Hexadecimal')
        
        self.lbl_dec_val = QLabel('65')
        self.lbl_bin_val = QLabel('0b1000001')
        self.lbl_hex_val = QLabel('0x41')

        grid.addWidget(lbl_char, 0, 0)
        grid.addWidget(lbl_dec_name, 1, 0)
        grid.addWidget(lbl_bin_name, 2, 0)
        grid.addWidget(lbl_hex_name, 3, 0)
        grid.addWidget(self.cb_char, 0, 1)
        grid.addWidget(self.lbl_dec_val, 1, 1)
        grid.addWidget(self.lbl_bin_val, 2, 1)
        grid.addWidget(self.lbl_hex_val, 3, 1)

        self.groupbox_data = QGroupBox('Data')
        self.groupbox_data.setLayout(grid)


    def setupUiGroupboxControl(self):
        grid = QGridLayout()
        
        lbl_data = QLabel('Data')
        lbl_stop = QLabel('Stop')
        lbl_parity = QLabel('Parity')
        lbl_mode = QLabel('Mode')

        self.cb_data = QComboBox()
        self.cb_data.addItem('7 bits')
        self.cb_data.addItem('8 bits')
        self.cb_data.setCurrentIndex(1)

        self.cb_parity = QComboBox()
        self.cb_parity.addItem('none')
        self.cb_parity.addItem('even')
        self.cb_parity.addItem('odd')
        self.cb_parity.setCurrentIndex(1)

        self.cb_stop = QComboBox()
        self.cb_stop.addItem('1 bit')
        self.cb_stop.addItem('2 bits')
        self.cb_data.setCurrentIndex(1)

        self.cb_mode = QComboBox()
        self.cb_mode.addItem('TTL')
        self.cb_mode.addItem('RS232')
        self.cb_mode.setCurrentIndex(0)

        grid.addWidget(lbl_data, 0, 0)
        grid.addWidget(lbl_parity, 1, 0)
        grid.addWidget(lbl_stop, 2, 0)
        grid.addWidget(lbl_mode, 3, 0)
        grid.addWidget(self.cb_data, 0, 1)
        grid.addWidget(self.cb_parity, 1, 1)
        grid.addWidget(self.cb_stop, 2, 1)
        grid.addWidget(self.cb_mode, 3, 1)
        
        self.groupbox_control = QGroupBox('Control')
        self.groupbox_control.setLayout(grid)


    def setupUiFigure(self):
        self.plot_fig = plt.figure()
        self.plot_canvas = FigureCanvas(self.plot_fig)
        vbox = QVBoxLayout()
        vbox.addWidget(self.plot_canvas)
        self.groupbox_plot = QGroupBox('Diagram')
        self.groupbox_plot.setLayout(vbox)


    def setupSlots(self):
        self.cb_char.currentTextChanged.connect(self.onCbCharCurrentTextChanged)
        self.cb_data.currentTextChanged.connect(self.onCbDataCurrentTextChanged)
        self.cb_parity.currentTextChanged.connect(self.onCbParityCurrentTextChanged)
        self.cb_stop.currentTextChanged.connect(self.onCbStopCurrentTextChanged)
        self.cb_mode.currentTextChanged.connect(self.onCbModeCurrentTextChanged)


    def onCbCharCurrentTextChanged(self):
        c = self.cb_char.currentText()
        self.data.set_char(c)
        self.updateUi()
        self.updateFigure()


    def onCbDataCurrentTextChanged(self):
        c = 7 if '7' in self.cb_data.currentText() else 8
        self.data.set_length_data(c)
        self.updateFigure()


    def onCbParityCurrentTextChanged(self):
        c = self.cb_parity.currentText()
        self.data.set_parity(c)
        self.updateFigure()


    def onCbStopCurrentTextChanged(self):
        c = 1 if '1' in self.cb_stop.currentText() else 2
        self.data.set_length_stop(c)
        self.updateFigure()


    def onCbModeCurrentTextChanged(self):
        c = self.cb_mode.currentText()
        self.data.set_mode(c)
        self.updateFigure()


    def updateFigure(self):
        self.plot_fig.clf()
        
        x, y = self.data.get_xy()

        ax = self.updateFigureAx()
        ax.grid(dashes=(10, 5))
        ax.set_xticks(np.arange(x.size))
        ax.set_yticks([min(y), max(y)])
        ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        ax.legend(bbox_to_anchor=(0, 1, 1, 0.1), mode='expand', ncol=5)

        ax.step(x, y, where='post', color='black', linewidth=3)

        self.plot_fig.tight_layout()
        self.plot_canvas.draw_idle()


    def updateFigureAx(self):
        ALPHA = 0.1
        COL = ['k', 'b', 'r', 'y', 'g', 'k']

        ax = self.plot_fig.add_subplot(1, 1, 1)
        
        is_data_seven = self.data.get_length_data() == 7
        is_parity_none = self.data.get_parity() == 'none'
        is_stop_one = self.data.get_length_stop() == 1

        end_data = 9 if is_data_seven else 10
        end_parity = end_data if is_parity_none else end_data+1
        end_stop = end_parity+1 if is_stop_one else end_parity+2

        ax.axvspan(0, 1, color=COL[0], alpha=ALPHA)
        ax.axvspan(1, 2, color=COL[1], alpha=ALPHA, label='start')
        ax.axvspan(2, end_data, color=COL[2], alpha=ALPHA, label='data')
        ax.axvspan(end_data, end_parity, color=COL[3], alpha=ALPHA, label='parity')
        ax.axvspan(end_parity, end_stop, color=COL[4], alpha=ALPHA, label='stop')
        ax.axvspan(end_stop, 14, color=COL[5], alpha=ALPHA, label='idle')

        return ax


    def updateUi(self):
        self.lbl_dec_val.setText(self.data.get_dec())
        self.lbl_bin_val.setText(self.data.get_bin())
        self.lbl_hex_val.setText(self.data.get_hex())



class DataModel():
    def __init__(self):
        super().__init__()

        self.length = 15
        self.length_data = 8
        self.length_stop = 1
        self.parity = 'even'
        self.character = 'A'
        self.mode = 'TTL'
        self.x = np.arange(self.length)
        self.y = np.zeros(self.length)
        
        self.update()


    def update(self):
        message = self.compute_message()
        if self.mode == 'TTL':
            self.y = np.array([5 if b else 0 for b in message])
        elif self.mode == 'RS232':
            self.y = np.array([-8 if b else 8 for b in message])


    def compute_message(self):
        return [1, 0] + self.compute_ascii() + self.compute_post()


    def compute_post(self):
        result = [1]*5 if self.length_data == 8 else [1]*6
        result[0] = self.compute_parity()
        return result


    def compute_ascii(self):
        result = ord(self.character)
        result = bin(result)
        result = result[2:]
        result = result.zfill(self.length_data)
        result = [int(x) for x in result]
        result = result[::-1]
        return result


    def compute_parity(self):
        sum_of_bits = sum(self.compute_ascii())
        result = 1
        if self.parity == 'odd':
            result = (sum_of_bits+1) % 2
        elif self.parity == 'even':
            result = int(not((sum_of_bits+1) % 2))
        return result


    def get_xy(self):
        return (self.x, self.y)


    def get_char(self):
        return self.character


    def get_dec(self):
        return str(ord(self.character))


    def get_bin(self):
        return str(bin(ord(self.character)))


    def get_hex(self):
        return str(hex(ord(self.character)))


    def get_length_data(self):
        return self.length_data


    def get_length_stop(self):
        return self.length_stop


    def get_parity(self):
        return self.parity


    def set_char(self, c):
        self.character = c
        self.update()


    def set_length_data(self, value):
        self.length_data = value
        self.update()


    def set_length_stop(self, value):
        self.length_stop = value
        self.update()


    def set_parity(self, value):
        self.parity = value
        self.update()

    def set_mode(self, value):
        self.mode = value
        self.update()


    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())