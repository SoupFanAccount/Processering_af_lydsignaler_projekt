import numpy as np
from scipy.signal import lfilter, butter
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Button
from tkinter.ttk import Scale
from ttkthemes import ThemedTk

# Waveform generation functions

sample_rate=44100
def generate_waveform(wave_type, frequency, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if wave_type == 'Sine':
        return np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'Square':
        return np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == 'Triangle':
        return 2 * np.arcsin(np.sin(2 * np.pi * frequency * t)) / np.pi
    else:
        raise ValueError("Unsupported wave type")

# Filter functions
def resonator_filter(signal, center_freq, bandwidth, gain, sample_rate=44100):
    nyquist = 0.5 * sample_rate
    low = (center_freq - bandwidth / 2) / nyquist
    high = (center_freq + bandwidth / 2) / nyquist
    b, a = butter(2, [low, high], btype='band')
    filtered_signal = lfilter(b, a, signal)
    return filtered_signal * gain

def equalizer_filter(signal, gains, sample_rate=44100):
    nyquist = 0.5 * sample_rate
    b, a = butter(2, [0.2 / nyquist, 0.5 / nyquist], btype='band')
    filtered_signal = lfilter(b, a, signal) * gains[0]
    b, a = butter(2, [0.5 / nyquist, 2.0 / nyquist], btype='band')
    filtered_signal += lfilter(b, a, signal) * gains[1]
    b, a = butter(2, [2.0 / nyquist], btype='high')
    filtered_signal += lfilter(b, a, signal) * gains[2]
    return filtered_signal

# Playback function
def play_note(freq, wave_type):
    wave = generate_waveform(wave_type, freq, duration)

    res_strength = scale_res.get() / 100.0
    eq_strength = [scale_eq.get() / 100.0] * 3
    # Apply filters
    resonated_wave = resonator_filter(wave, 440, 50, res_strength)
    equalized_wave = equalizer_filter(resonated_wave, eq_strength)
    sd.play(equalized_wave, sample_rate)
    sd.wait()

#sample_rate=44100

c = 261.6
c_sharp = 277.2
d = 293.7
e_b = 311.1
e = 329.6
f = 349.2
f_sharp = 370
g = 392
g_sharp = 415.3
a = 440
b_b = 466.2
b = 493.9

duration = 0.5

root = ThemedTk(theme="arc")
root.geometry('1000x200')

frame= tk.Frame(root)
frame.grid(row=3, column=9)

waves = tk.StringVar()
waveform_menu = ttk.Combobox(frame, width=15, textvariable=waves)
waveform_menu.grid(row=1, column=3, columnspan=2)
waveform_menu['values'] = ("Sine", "Square", "Triangle")

waveform_menu.current(0)

label_res = tk.Label(frame, text="Resonator", anchor='w', justify='left').grid(row=2, column=3)
scale_res = tk.Scale(frame, from_=100, to=0, orient="vertical")
scale_res.set(50)
scale_res.grid(row=3, column=3)

label_eq = tk.Label(frame, text="Equalizer", anchor='w', justify='left').grid(row=2, column=6)
scale_eq = tk.Scale(frame, from_=100, to=0, orient="vertical")
scale_eq.set(50)
scale_eq.grid(row=3, column=6)

button_c = Button(frame, text = "C", command=lambda:play_note(c, waves.get()))
button_c_sharp = Button(frame, text = "C#", command=lambda:play_note(c_sharp, waves.get())).grid(row=0, column=0)
button_d = Button(frame, text = "D", command=lambda:play_note(d, waves.get())).grid(row=0, column=1)
button_e_b = Button(frame, text = "Eb", command=lambda:play_note(e_b, waves.get())).grid(row=0, column=2)
button_f = Button(frame, text = "F", command=lambda:play_note(f, waves.get())).grid(row=0, column=3)
button_f_sharp = Button(frame, text = "F#", command=lambda:play_note(f_sharp, waves.get())).grid(row=0, column=4)
button_g = Button(frame, text = "G", command=lambda:play_note(g, waves.get())).grid(row=0, column=5)
button_g_sharp = Button(frame, text = "G#", command=lambda:play_note(g_sharp, waves.get())).grid(row=0, column=6)
button_a = Button(frame, text = "A", command=lambda:play_note(a, waves.get())).grid(row=0, column=7)
button_b_b = Button(frame, text = "Bb", command=lambda:play_note(b_b, waves.get())).grid(row=0, column=8)
button_b = Button(frame, text = "B", command=lambda:play_note(b, waves.get())).grid(row=0, column=9)

root.mainloop()
