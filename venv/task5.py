import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task4
import task5
import task6
import cmath
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools.msvc import winreg


def task5(root):

    def combobox_selected(event):
        if combobox.get() == combobox_array[0] or combobox.get() == combobox_array[2] or combobox.get() == combobox_array[4]:
            browse2.place(x=9999, y=500 + 40 * 3)
            number_text.place(x=300, y=500 + 40 * 5)
            number_label.place(x=220, y=500 + 40 * 5)
            browse2.place(x=9999, y=500 + 40 * 3)

        else:
            browse2.place(x=410, y=500 + 40 * 3)
            number_text.place(x=9999, y=500 + 40 * 5)
            number_label.place(x=9999, y=500 + 40 * 5)
            browse2.place(x=9999, y=500 + 40 * 3)
            if(combobox.get() == combobox_array[6]):
                browse2.place(x=410, y=500 + 40 * 3)


    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
        task4.task4(root)

    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task6.task6(root)

    def browse_file():

        # Get the file path from the file dialog
        file_path = tk.filedialog.askopenfilename()
        try:
            # Check if the file path ends with .txt extension
            if file_path.endswith('.txt'):
                global data
                data = np.loadtxt(file_path, max_rows=3)
                global signal_type
                signal_type = int(data[0])
                is_periodic = int(data[1])
                global n
                n = int(data[2])
                data = np.loadtxt(file_path, skiprows=3)
                browse_label.config(text="File successfully read with NumPy!", fg='green')
                # You can perform further processing with the data here


            else:
                browse_label.config(text="Selected file is not a .txt file.", fr='red')


        except Exception as e:
            browse_label.config(text="Error reading the file:", fg='red')

    def browse_file2():

        # Get the file path from the file dialog
        file_path = tk.filedialog.askopenfilename()
        try:
            # Check if the file path ends with .txt extension
            if file_path.endswith('.txt'):
                global data2
                data2 = np.loadtxt(file_path, max_rows=3)
                global signal_type2
                signal_type2 = int(data2[0])
                is_periodic2 = int(data2[1])
                global n2
                n2 = int(data2[2])
                data2 = np.loadtxt(file_path, skiprows=3)
                browse_label2.config(text="File successfully read with NumPy!", fg='green')
                # You can perform further processing with the data here


            else:
                browse_label2.config(text="Selected file is not a .txt file.", fr='red')


        except Exception as e:
            browse_label2.config(text="Error reading the file:", fg='red')

    def smoothing(signal, window_size):
        n = len(signal) - window_size + 1
        new_signal = []
        for i in range(n):
            sum = 0
            for j in range(i, i + window_size):
                sum+=signal[j]
            new_signal.append(sum/window_size)
        return new_signal

    def sharpening(signal):
        #Y(n) = x(n)-x(n-1)
        x = signal
        first_derivative = x[1:] - x[:-1]
        # Y(n)= x(n+1)-2x(n)+x(n-1)
        second_derivative = x[2:] - 2 * x[1:-1] + x[:-2]

        return first_derivative, second_derivative

    def delay_advance_signal(signal, k):
        delayed_signal = np.zeros_like(signal)
        if k == 0:
            return signal
        elif k > 0:
            delayed_signal[k:] = signal[:-k]
        else:
            delayed_signal[:k] = signal[-k:]
        return delayed_signal

    def fold_signal(signal):
        folded_signal = []
        n = len(signal) - 1
        for i in range(len(signal)):
            folded_signal.append(signal[n-i])
        return folded_signal

    def delay_advance_folded_signal(signal, k):
        folded = fold_signal(signal)
        return delay_advance_signal(folded, k)

    def convolution(signal1, signal2):
        length = len(signal1) + len(signal2) - 1
        new_signal = []
        for k in range(length):
            sum = 0
            for x in range(k, -1 , -1):
                if(len(signal1) <= len(signal2)):
                    if x >= len(signal1): continue
                    if k-x >= len(signal2): continue
                    sum+=signal1[x]*signal2[k-x]
                else:
                    if x >= len(signal2): continue
                    if k-x >= len(signal1): continue
                    sum+=signal2[x]*signal1[k-x]

            new_signal.append(sum)

        return new_signal





    def dft(signal):
        N = len(signal)
        dft_result = [0] * N

        for k in range(N):
            dft_result[k] = sum(signal[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N))

        return dft_result

    def idft(dft_result):
        N = len(dft_result)
        idft_signal = [0] * N

        for n in range(N):
            idft_signal[n] = sum(dft_result[k] * cmath.exp(2j * cmath.pi * k * n / N) for k in range(N)) / N

        return idft_signal

    def remove_DC(signal):
        dft_result = dft(signal)
        dft_result[0] = 0
        reconstructed_signal = idft(dft_result)
        return reconstructed_signal


    def clear_button_action():
        number_text.delete(0, "end")
        wrong_label.config(text="")
        browse_label.config(text="", fg="red")
        browse_label2.config(text="", fg="red")
        ax.clear()
        ax2.clear()
        ax3.clear()
        ax.set_title('Before')
        ax2.set_title('After')
        canvas.draw()
        canvas2.draw()

    def generate_button_check():
        if browse_label.cget("foreground") != 'green':
            return False
        if combobox.get() == combobox_array[0]:
            try:
                if number_text.get() != "":
                    if int(number_text.get()) > 0 and  int(number_text.get()) <= len(data[:, 1]):
                        return True
                    else :
                        return False
                else:
                    return False
            except ValueError:
                return False
        if combobox.get() == combobox_array[2] or combobox.get() == combobox_array[4]:
            try:
                if number_text.get() != "":
                    int(number_text.get())
                else:
                    return False
            except ValueError:
                return False


    def generate_button_action():

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return
        else:
            wrong_label.config(text="")
        print("==================================================================================================================")
        ax.clear()
        ax2.clear()
        if combobox.get() ==  combobox_array[0]: #smoothing
            signal = data[:,1]
            N = np.arange(n)
            w = int(number_text.get())
            # Before
            ax.stem(N, signal)
            signalSmooth = smoothing(signal, w)
            print(signalSmooth)
            num = int(n - w + 1)
            N = np.arange(num)
            ax2.stem(N, signalSmooth)

            # plt.yticks([-180, -90, -45, 0, 45, 90, 180])

        elif combobox.get() ==  combobox_array[1]: #sharpening
            signal = data[:,1]
            #Before
            # ax.plot(n, signal)

            first, second = sharpening(signal)
            print(signal)
            print(first)
            print(second)
            N = np.arange(len(first))
            ax.stem(N, first)
            N = np.arange(len(second))
            ax2.stem(N, second)
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Magnitude")
            # plt.yticks([-180, -90, -45, 0, 45, 90, 180])

        elif combobox.get() == combobox_array[2]: #delaying/advancing
            signal = data[:,1]
            N = np.arange(n)
            ax.stem(N, signal)
            second_signal = delay_advance_signal(signal, int(number_text.get()))
            ax2.stem(N, second_signal)
            print(signal)
            print(second_signal)

        elif combobox.get() == combobox_array[3]:  # Folding
            signal = data[:, 1]
            N = np.arange(n)
            ax.stem(N, signal)
            second_signal = fold_signal(signal)
            ax2.stem(N, second_signal)
            print(signal)
            print(second_signal)

        elif combobox.get() == combobox_array[4]:  # delaying/advancing & Folding
            signal = data[:,1]
            N = np.arange(n)
            ax.stem(N, signal)
            second_signal = delay_advance_folded_signal(signal, int(number_text.get()) )
            ax2.stem(N, second_signal)
            print(signal)
            print(second_signal)

        elif combobox.get() == combobox_array[5]:  # Removing DC
            signal = data[:,1]
            N = np.arange(n)
            ax.plot(N, signal)
            second_signal = remove_DC(signal)
            avg = sum(signal) / len(signal)
            ax.axhline(avg, color='black', linestyle='-', label='X-axis')
            ax2.plot(N, second_signal)
            ax2.axhline(avg, color='black', linestyle='-', label='X-axis')
            print(signal)
            print(second_signal)


        elif combobox.get() == combobox_array[6]:  # convolution:
            signal = data[:,1]
            print(signal)
            signal2 = data2[:,1]
            print(signal2)
            N = np.arange(n)
            ax.stem(data[:, 0], signal)
            new_signal = convolution(signal, signal2)

            m = min(data[0][0], data2[0][0])
            N = np.arange(m, len(data)  + len(data2) + m - 1)
            ax2.stem(N, new_signal)
            print(new_signal)

        ax.set_title('Before')
        ax2.set_title('After')
        canvas.draw()
        canvas2.draw()

    root.title("Lab6 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y=650 + 40 * 7)
    next_button = tk.Button(text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y=650 + 40 * 7)
    fig, ax = plt.subplots(figsize=(6, 3))
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
    # canvas3.get_tk_widget().pack()
    ax.set_title('Before')
    ax2.set_title('After')
    browse = tk.Button(text="Browse", command=browse_file)
    browse.place(x=330, y=500 + 40 * 3)

    browse2 = tk.Button(text="Browse2", command=browse_file2)
    browse2.place(x=4100, y=500 + 40 * 3)

    combobox_array = ['Smoothing', 'Sharpening', 'Delaying/Advancing', 'Folding', 'Delaying/Advancing(Fold)', 'Remove DC', 'Convolution']
    combobox = ttk.Combobox(values=combobox_array, state="readonly")
    combobox.current(0)
    combobox.place(x = 300, y=500 + 40 * 4)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)

    number_text = tk.Entry()
    number_text.place(x=300, y=500 + 40 * 5)

    number_label = tk.Label(text="Window Size")
    number_label.place(x=220, y=500 + 40 * 5)

    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x=300, y=500 + 40 * 7)

    clear_button = tk.Button(text="Clear", command= clear_button_action)
    clear_button.place(x= 380,  y=500 + 40 * 7)

    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 500 + 40 * 8)

    browse_label = tk.Label()
    browse_label.place(x=450, y= 800)

    browse_label2 = tk.Label()
    browse_label2.place(x=450, y= 830)