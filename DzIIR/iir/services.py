import os

import numpy
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from scipy.io import wavfile
from scipy.signal import iirfilter, lfilter, freqz
from scipy.fft import fft, fftfreq


ROOT_DIR = os.path.dirname(os.path.abspath(__name__))
MY_MEDIA_DIR = ROOT_DIR + '/static/media/'
matplotlib.use('Agg')


def sum_all_arrays(y1, y2, y3, y4, y5):
    return y1 + y2 + y3 + y4 + y5


def audio_read(filename: str):
    return wavfile.read(f'{MY_MEDIA_DIR}/audio/{filename}')


def audio_save(filename: str, data, fs_audio: int):
    y = np.asarray(data, dtype=np.int16)
    wavfile.write(f'{MY_MEDIA_DIR}/audio/{filename}', fs_audio, y)


class CustomIIRFilter:
    def __init__(self, fs: int, order: int, ftype='butter', output='ba'):
        self.fs = fs
        self.order = order
        self.ftype = ftype
        self.output = output

    @property
    def _nyquist(self):
        return int(self.fs / 2)

    def _get_norm_freq(self, freq: int):
        return freq / self._nyquist

    def get_iir_filter(self, btype: str = 'bandpass',
                       f1: int = 0,
                       f2: int = 0):
        f1_norm = self._get_norm_freq(f1)
        f2_norm = self._get_norm_freq(f2)

        if btype == 'bandpass':
            if f1 >= f2:
                raise ValueError('f1 cant be bigger than f2')
            f = [f1_norm, f2_norm]
        elif btype == 'lowpass':
            f = [f1_norm]
        elif btype == 'highpass':
            f = [f2_norm]
        else:
            raise NotImplementedError('NotImplemented FilterType')

        b, a = iirfilter(self.order, f,
                         btype=btype,
                         ftype=self.ftype,
                         output=self.output)
        return b, a

    @staticmethod
    def filter(data: numpy.ndarray, b: numpy.ndarray,
               a: numpy.ndarray):
        return lfilter(b, a, data)


class CustomPlotStuff:
    def __init__(self, linewidth: str = 2, fontsize: int = 20):
        self.linewidth = linewidth
        self.fontsize = fontsize

    def save_filter_plot(self, f_name: str, fs: int, b, a):
        wz, hz = freqz(b, a)
        fg = plt.figure()
        plt.plot(hz)
        plt.show()
        # Calculate Magnitude from hz in dB
        mag = 20 * np.log10(abs(hz))
        # Frequency in Hz from wz
        freq = wz * fs / (2*np.pi)
        # Plot filter magnitude and phase responses using subplot.
        fig = plt.figure(figsize=(10, 6))

        # Plot Magnitude response
        plt.plot(freq, mag, 'r', linewidth=self.linewidth)
        plt.axis([1, fs / 2, -100, 5])
        plt.title('АЧХ фильтра', fontsize=self.fontsize)
        plt.xlabel('Частота', fontsize=self.fontsize)
        plt.ylabel('Амплитуда', fontsize=self.fontsize)
        plt.grid()

        plt.subplots_adjust(hspace=0.5)
        fig.tight_layout()
        plt.savefig(f'{MY_MEDIA_DIR}/plots/{f_name}')
        plt.close()

    @staticmethod
    def save_signal_fft_plot(data: numpy.ndarray, f_name: str, fs: int,
                             title: str):
        data_len = len(data)
        fft_data = fft(data)  # Calculate fft
        freq_bins = fftfreq(data_len, 1/fs)
        plt.figure(title)
        plt.plot(freq_bins, abs(fft_data))
        plt.grid()
        plt.savefig(f'{MY_MEDIA_DIR}/plots/{f_name}')
        plt.close()

    @staticmethod
    def save_signal_plot(data: numpy.ndarray, f_name: str):
        plt.figure()
        plt.plot(data)
        plt.grid()
        plt.savefig(f'{MY_MEDIA_DIR}/plots/{f_name}')
        plt.close()


def do_some_stuff(n1: int, n2: int, n3: int, n4: int, n5: int):
    """ Entry point function """
    fs = 44100
    order = 2

    fig = CustomPlotStuff()

    fltr1 = CustomIIRFilter(fs=fs, order=order)
    fltr2 = CustomIIRFilter(fs=fs, order=order)
    fltr3 = CustomIIRFilter(fs=fs, order=order)
    fltr4 = CustomIIRFilter(fs=fs, order=order)
    fltr5 = CustomIIRFilter(fs=fs, order=order)

    b1, a1 = fltr1.get_iir_filter(btype='bandpass', f1=1000, f2=2000)
    b2, a2 = fltr2.get_iir_filter(btype='bandpass', f1=3000, f2=4000)
    b3, a3 = fltr3.get_iir_filter(btype='bandpass', f1=6000, f2=7000)
    b4, a4 = fltr3.get_iir_filter(btype='bandpass', f1=9000, f2=10000)
    b5, a5 = fltr3.get_iir_filter(btype='highpass', f2=16500)

    fig.save_filter_plot(f_name='1/fltr1.png', fs=fs, b=b1, a=a1)
    fig.save_filter_plot(f_name='2/fltr2.png', fs=fs, b=b2, a=a2)
    fig.save_filter_plot(f_name='3/fltr3.png', fs=fs, b=b3, a=a3)
    fig.save_filter_plot(f_name='4/fltr4.png', fs=fs, b=b4, a=a4)
    fig.save_filter_plot(f_name='5/fltr5.png', fs=fs, b=b5, a=a5)

    fs_audio, x = audio_read('rock.wav')

    y1 = fltr1.filter(x, b1, a1)
    y2 = fltr2.filter(x, b2, a2)
    y3 = fltr3.filter(x, b3, a3)
    y4 = fltr4.filter(x, b4, a4)
    y5 = fltr5.filter(x, b5, a5)

    y1 = np.multiply(y1, n1)
    y2 = np.multiply(y2, n2)
    y3 = np.multiply(y3, n3)
    y4 = np.multiply(y4, n4)
    y5 = np.multiply(y5, n5)

    fig.save_signal_fft_plot(y1, 'y1.png', fs=fs,
                             title='АЧХ после 1-фильтра')
    fig.save_signal_fft_plot(y2, 'y2.png', fs=fs,
                             title='АЧХ после 2-фильтра')
    fig.save_signal_fft_plot(y3, 'y3.png', fs=fs,
                             title='АЧХ после 3-фильтра')
    fig.save_signal_fft_plot(y4, 'y4.png', fs=fs,
                             title='АЧХ после 4-фильтра')
    fig.save_signal_fft_plot(y5, 'y5.png', fs=fs,
                             title='АЧХ после 5-фильтра')

    y_sum = sum_all_arrays(y1, y2, y3, y4, y5)
    fig.save_signal_fft_plot(y_sum, 'y_sum.png', fs=fs,
                             title='АЧХ выходного сигнала')

    fig.save_signal_plot(data=x, f_name='input_signal.png')
    fig.save_signal_plot(data=y_sum, f_name='output_signal.png')
    audio_save('output.wav', data=y_sum, fs_audio=fs_audio)
