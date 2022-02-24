import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import scipy.io.wavfile as wav
import sys

IR_PATH = sys.argv[1]
AF_PATH = sys.argv[2]
OUT_FILE = sys.argv[3]

PLOT_ME = False
if(len(sys.argv)>4):
    PLOT_ME = True

print("\n   IR file: "+ IR_PATH + "\n  WAV file: " + AF_PATH)

#unit conversions
db_to_mag = lambda x: 10 ** (x/20)
mag_to_db = lambda x: 20 * np.log10(x)

# impulse response
fs, ir_sig = wav.read(IR_PATH) # impulse response
ir_sig = ir_sig[ir_sig != 0] # remove unusable coeffs

# audio file to convolve
af_fs, af_sig = wav.read(AF_PATH) # audio file

assert(af_fs == fs)

#convolving
wet_signal = scipy.signal.fftconvolve(af_sig, ir_sig)
#normalize to [-1,1]
wet_signal = wet_signal / np.max(np.abs(wet_signal))

# accomodate signal sizes
dry_signal = np.concatenate((af_sig,np.zeros(len(wet_signal) - len(af_sig))))
output_signal = dry_signal + db_to_mag(-2) * wet_signal

wav.write("WET_"+OUT_FILE, fs, wet_signal)
wav.write(OUT_FILE, fs, output_signal)

plt.figure()


def creat_spect(sig,f_s,p_ath, fig_num):
    plt.figure(fig_num)
    plt.specgram(sig, Fs=f_s, NFFT=512, noverlap=500, vmin=-100)
    plt.colorbar()
    plt.title(p_ath)
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Frequency (Hz)")
    

if PLOT_ME:
    print("LOADING SPECTROGRAMS. . .")
    creat_spect(ir_sig,fs,"Impulse Response: "+IR_PATH,1)
    creat_spect(af_sig,fs,"Input audio: "+AF_PATH,2)
    creat_spect(wet_signal,fs,"WET audio "+ AF_PATH,3)
    creat_spect(output_signal,fs,"Convolved: "+ OUT_FILE,4)
    print("JUST ONE MORE SECOND :) . . .")
    plt.show()