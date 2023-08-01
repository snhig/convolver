
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pyqtgraph as pg
import numpy as np
from threading import Thread
from scipy import signal
import scipy.signal
import scipy.io.wavfile as wav
import os

DB_TO_MAG = lambda x: 10 ** (x/20)
MAG_TO_DB = lambda x: 20 * np.log10(x)

def covolve(ir_path, af_path):
    # impulse response
    fs, ir_sig = wav.read(ir_path) # impulse response
    ir_sig = ir_sig[ir_sig != 0] # remove unusable coeffs
    # audio file to convolve
    af_fs, af_sig = wav.read(af_path) # audio file
    assert(af_fs == fs)
    #convolving
    wet_signal = scipy.signal.fftconvolve(af_sig, ir_sig)
    #normalize to [-1,1]
    wet_signal = wet_signal / np.max(np.abs(wet_signal))
    # accomodate signal sizes
    dry_signal = np.concatenate((af_sig,np.zeros(len(wet_signal) - len(af_sig))))
    output_signal = dry_signal + DB_TO_MAG(-2) * wet_signal
    
    return dry_signal, wet_signal, output_signal, ir_sig, fs

def write_file(file_name_path, fs, sig):
    wav.write(file_name_path, fs, sig)


class CovolverGUI(QMainWindow):
    def __init__(self, application:QApplication) -> None:
        super().__init__()
        self.ir_path = ""
        self.sample_path = ""
        self.app = application
        self.setWindowTitle("Covolver")
        self.app.setStyle("Fusion")
        
        self.convolver_control = ConvolverControl()
        self.setCentralWidget(self.convolver_control)
        
        self.construct_toolbar()
        self.bind_gui()
        
        

            
    def construct_toolbar(self):
        self.file_menu = self.menuBar().addMenu("&File")
        # add load action to file menu
        self.load_action = QAction("&Load", self)
        self.file_menu.addAction(self.load_action)
        self.write_action = QAction("&Write", self)
        
        
        
        
        self.fp_labels = QLabel("IR: None  |  Sample: None")
        self.statusBar().addPermanentWidget(self.fp_labels)

        
    def bind_gui(self):
        self.load_action.triggered.connect(self.load_action_trig)
        self.write_action.triggered.connect(self.write_action_trig)
        
        
    def load_action_trig(self):
        # promptuser to load a file
        # self.sample_path = os.getcwd() + '\\test_in.wav'
        # self.ir_path = os.getcwd() + '\\ir.wav'
        
        # self.fp_labels.setText("IR: " + self.ir_path.split('\\')[-1] + ' | Sample: ' + self.sample_path.split('\\')[-1])
        # self.convolver_control.convovle_trigger(self.ir_path, self.sample_path)

        sample_path, _ = QFileDialog.getOpenFileName(self, "Load Sample", "", "WAV Files (*.wav)")
        if sample_path != '':
            # load the file
            impluse_response_path, _ = QFileDialog.getOpenFileName(self, "Load Impulse Response", "", "WAV Files (*.wav)")
            
            if impluse_response_path != '':
                self.sample_path = sample_path
                self.ir_path = impluse_response_path
                
                self.fp_labels.setText(f"IR: {self.ir_path.split('/')[-1]} |  Sample: {self.sample_path.split('/')[-1]}")
                self.convolver_control.convovle_trigger(self.ir_path, self.sample_path)
                
                self.file_menu.addAction(self.write_action)
                
    
    
        
    def write_action_trig(self):
        fs = self.convolver_control.fs
        out_sig = self.convolver_control.out_sig
        wet_sig = self.convolver_control.wet_sig
        
        # choose a directory
        out_path = QFileDialog.getExistingDirectory(self, "Save Output", dir=os.getcwd())
        if out_path != '':
            # get datetime in filesame format
            file_time = QDateTime.currentDateTime().toString("\\yyyy-MM-dd_hh-mm-ss")
            write_file(out_path +file_time +'_out_mixed.wav', fs, out_sig)
            write_file(out_path +file_time + '_out_wet.wav', fs, wet_sig)
        
        
        
        
class ConvolverControl(QWidget):
    convolve_finished = Signal()
    def __init__(self) -> None:
        super().__init__()
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.setWindowTitle("Load")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0,100)
        self.loading_bar.setVisible(False)
        self.main_layout.addWidget(self.loading_bar)
        
        self.graph_area = QHBoxLayout()
        self.main_layout.addLayout(self.graph_area)

        self.convolve_finished.connect(self.add_graphs)

    def convolve_back(self, ir_path, sample_path):
        self.loading_bar.setValue(24)
        self.loading_bar.setVisible(True)
        self.dry_sig, self.wet_sig, self.out_sig, self.ir_sig, self.fs = covolve(ir_path, sample_path)
        self.loading_bar.setValue(50)
        self.convolve_finished.emit()
        
    def add_graphs(self):
        
        ir_plot, ir_im = self.create_spectrogram_widget(self.ir_sig, self.fs, "Impulse Response")
        self.loading_bar.setValue(55)
        
        dry_plot, dry_im = self.create_spectrogram_widget(self.dry_sig, self.fs, "Dry Signal")
        self.loading_bar.setValue(70)
        
        wet_plot, wet_im = self.create_spectrogram_widget(self.wet_sig, self.fs, "Wet Signal")
        self.loading_bar.setValue(85)
        
        out_plot, out_im = self.create_spectrogram_widget(self.out_sig, self.fs, "Output Signal")
        self.loading_bar.setValue(100)
        
        
        
        self.loading_bar.setVisible(False)
                
        self.graph_area.addWidget(ir_plot)
        self.graph_area.addWidget(dry_plot)
        self.graph_area.addWidget(wet_plot)
        self.graph_area.addWidget(out_plot)
        
    def convovle_trigger(self, ir_path, sample_path):
        self.thr = Thread(target=self.convolve_back, args=(ir_path, sample_path))
        self.thr.start()    
    
    def create_spectrogram_widget(self, data, fs, title):
    # Compute the spectrogram using numpy's specgram function
        f, t, Sxx = signal.spectrogram(data, fs)
        print('Sxx shape:', Sxx.shape)
        print('f shape:', f.shape)
        print(f'{title}: {data}')
        # Create a plot widget
        plot = pg.PlotWidget()

        # Set plot properties
        plot.setLabel('left', 'Frequency (Hz)')
        plot.setLabel('bottom', 'Time (s)')
        #plot.setLogMode(x=False, y=True)  # Use log scale for frequency
        #plot.setLimits(xMin=0, xMax=t[-1], yMin=f[0], yMax=f[-1])
        # add plot title
        plot.setTitle(title)
        # Plot the spectrogram
        img = pg.ImageItem()
        #plot.addColorBar( img, colorMap='viridis', values=(min(f), max(f)))
        plot.setYRange(0,10)
        plot.addItem(img)
        img.setImage(Sxx, xvals=t, yvals=f)
        

        return plot, img






if __name__ == '__main__':
    app = QApplication([])
    window = CovolverGUI(app)
    window.show()
    app.exec()