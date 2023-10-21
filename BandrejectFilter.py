from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import scipy
import subprocess
import io

#file name (without .wav)
file_name = "yourFileName"

# Sample frequency (Hz)
samp_freq = 48000

# Frequency to be removed from signal (Hz)
# you can play your sound on your computer and listen to it on a phone by "Spectroid" app on google play store
# with this way, you can find the frequency you want to remove
notch_freq = 674.0

# Quality factor
quality_factor = 30.0

b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)

print("reading...")
rate, orginal_signal = scipy.io.wavfile.read(f"{file_name}.wav")

print("filtering...")
notched_signal = signal.filtfilt(b_notch, a_notch, orginal_signal)

print("re-sampling...")
max_value    =  np.max(np.abs(notched_signal))
final_signal = (notched_signal/max_value).astype(np.float32)

final_signal /= 1.414
final_signal *= 32767

print("saving...")
memoryBuff = io.BytesIO()

#if you dont want to convert .wav to mp3 (or you dont want to use ffmpeg) you can un-comment these two lines and delete the rest.
#scipy.io.wavfile.write(f"{file_name}_filtered.wav", rate, final_signal.astype(np.int16))
#print("finished!")


scipy.io.wavfile.write(memoryBuff, rate, final_signal.astype(np.int16))
# you need ffmpeg on system path
output_name = file_name + "_filtered.mp3"
print("Converting into mp3 !")
command = ['ffmpeg', '-i', '-', output_name]
subprocess.run(command, input=memoryBuff.getvalue(), shell=True)
print("finished!")
