import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task3
import task4
import task5
import cmath
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def task4(root):

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

    def dct(signal):
        N = len(signal)
        dct_result = [0] * N

        for k in range(N):
            dct_result[k] = np.sqrt(2/N)*sum(signal[n] * np.cos((np.pi/(4*N))*(2*n-1)*(2*k-1)) for n in range(N))
        return dct_result

    def dc(signal):
        N = len(signal)
        dct_result = [0] * N
        removed_DC = [0] * N
        values = data[:, 1]
        global avg
        avg = sum(values) / len(values)

        for i in range(len(values)):
            removed_DC[i] = values[i] - avg
        return removed_DC, avg


    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task5.task5(root)

    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
        task3.task3(root)

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
    def save_file():
        # Specify the file path
        if combobox.get() == 'DFT':
            if browse_label.cget("foreground") != 'green':
                browse_label.config(text="Error! empty data:", fg='red')
                return
            file_path = "output.txt"
            saved_data = list(zip(np.fft.fft(data[:, 1]), [np.arctan(c.imag / c.real) for c in np.fft.fft(data[:, 1])]))
            # listed = [0, 1, len(saved_data)]
            # saved_data = [(col1,) + pair for col1, pair in zip(listed, saved_data)]
            # Open the file in write mode and write the list elements to it

            with open(file_path, "w") as file:
                file.write('0\n1\n' + str(n) + '\n')
                for item in saved_data:
                    file.write(str(item) + "\n")
        else:
            saved_data, avg = dc(data[:, 1])
            n = len(saved_data)
            try:
                if firstM_text.get() != "":
                    int(firstM_text.get())
                else:
                    wrong_label.config(text="Invalid input")
                    return
                if int(firstM_text.get()) > n:
                    print("ANA?")
                    wrong_label.config(text="Invalid input")
                    return
                wrong_label.config(text="")
                file_path = "done job.txt"
                num = int(firstM_text.get())
                if os.path.exists(file_path):
                    os.remove(file_path)
                with open(file_path, "w") as file:
                    for i in range(num):
                        file.write(str(saved_data[i]) + "\n")
            except ValueError:
                wrong_label.config(text="Invalid input")






    def clear_button_action():
        frequency_text.delete(0, "end")
        index_text.delete(0, "end")
        amplitiude_text.delete(0, "end")
        phase_text.delete(0, "end")
        wrong_label.config(text="")
        browse_label.config(text="", fg="red")
        ax.clear()
        ax2.clear()
        ax.set_title('Before')
        ax2.set_title('After')
        canvas.draw()
        canvas2.draw()

    def checkbox_changed():
        index_text.delete(0, "end")
        amplitiude_text.delete(0, "end")
        phase_text.delete(0, "end")
        if checkbox_var.get() == 1:
            index_label.config(text="Index")
            amplitiude_label.config(text="Amplitiude")
            phase_label.config(text="Phase")

            index_text.place(x=300, y=500 + 40 * 7)
            index_label.place(x=230, y=500 + 40 * 7)
            amplitiude_text.place(x=300, y=500 + 40 * 8)
            amplitiude_label.place(x=230, y=500 + 40 * 8)
            phase_text.place(x=300, y=500 + 40 * 9)
            phase_label.place(x=230, y=500 + 40 * 9)
            generate_button.place(x=300, y=620 + 40 * 7)
            clear_button.place(x=380, y=620 + 40 * 7)
            wrong_label.place(x=300, y=500 + 40 * 11)

        else:
            index_label.config(text="")
            amplitiude_label.config(text="")
            phase_label.config(text="")
            index_text.place(x=5000, y=500 + 40 * 4)
            index_label.place(x=5000, y=500 + 40 * 4)
            amplitiude_text.place(x=5000, y=500 + 40 * 5)
            amplitiude_label.place(x=5000, y=500 + 40 * 5)
            phase_text.place(x=5000, y=500 + 40 * 6)
            phase_label.place(x=5000, y=500 + 40 * 6)
            generate_button.place(x=300, y=500 + 40 * 7)
            clear_button.place(x=380, y=500 + 40 * 7)
            wrong_label.place(x=300, y=500 + 40 * 8)

    def combobox_selected(event):
        if combobox.get() == 'DFT':
            clear_button_action()
            frequency_label.config(text="Frequency")
            frequency_text.place(x=300, y=500 + 40 * 5)
            frequency_label.place(x=230, y=500 + 40 * 5)
            checkbox.place(x=230, y=500 + 40 * 6)
            save_button.place(x=630, y=500 + 40 * 3)
            firstM_text.place(x=55555, y=500 + 40 * 5)
            firstM_label.place(x=5555, y=500 + 40 * 5)
            checkbox_changed()

        elif combobox.get() == 'DCT':
            clear_button_action()
            checkbox_var.set(0)
            frequency_text.place(x=5000, y=420 + 40 * 4)
            frequency_label.place(x=5000, y=417 + 40 * 4)
            checkbox.place(x=5000, y = 500 + 40)
            checkbox_changed()
            save_button.place(x=590, y=557 + 40 * 3)
            firstM_text.place(x=580, y=527 + 40 * 3)
            firstM_label.place(x=550, y=500 + 40 * 3)

        elif combobox.get() == 'DC':
            clear_button_action()
            checkbox_var.set(0)
            frequency_text.place(x=5000, y=420 + 40 * 4)
            frequency_label.place(x=5000, y=417 + 40 * 4)
            checkbox.place(x=5000, y = 500 + 40)
            checkbox_changed()
            save_button.place(x=55555, y=557 + 40 * 3)
            firstM_text.place(x=55555, y=527 + 40 * 3)
            firstM_label.place(x=5555, y=500 + 40 * 3)
            save_button.place(x=55555, y=500 + 40 * 3)
            firstM_text.place(x=55555, y=500 + 40 * 5)
            firstM_label.place(x=55555, y=500 + 40 * 5)

        else:
            clear_button_action()
            checkbox_var.set(0)
            frequency_text.place(x=5000, y=420 + 40 * 4)
            frequency_label.place(x=5000, y=417 + 40 * 4)
            checkbox.place(x=5000, y = 500 + 40)
            checkbox_changed()
            save_button.place(x=55555, y=500 + 40 * 3)
            firstM_text.place(x=55555, y=500 + 40 * 5)
            firstM_label.place(x=55555, y=500 + 40 * 5)
    def generate_button_check():
        if browse_label.cget("foreground") != 'green':
            return False
        if combobox.get() == 'DFT':
            try:
                if frequency_text.get() != "":
                    float(frequency_text.get())
                else:
                    return False
            except ValueError:
                return False
            if checkbox_var.get() == 1:
                try:
                    if amplitiude_text.get() != "":
                        float(amplitiude_text.get())
                    else:
                        return False
                    if phase_text.get() != "":
                        float(phase_text.get())
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
        if combobox.get() == 'DFT':
            # signal = np.fft.fft(data[:,1])
            signal = dft(data[:,1])
            freq = 2 * np.pi*float(frequency_text.get())/n
            ffreq = np.arange(freq, (n + 1) * freq, freq)

            # amplitude_array = abs(signal)
            amplitude_array = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in signal]
            if checkbox_var.get() == 1:
                idx = int(index_text.get())
                amp = float(amplitiude_text.get())
                amplitude_array[idx] = amp


            ax.stem(ffreq, amplitude_array)
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")

            phase_array = [np.arctan(c.imag / c.real) for c in signal]
            phase_degrees = [np.degrees(phase) for phase in phase_array]
            if checkbox_var.get() == 1:
                idx = int(index_text.get())
                pha = float(phase_text.get())
                phase_degrees[idx] = pha
            ax2.stem(ffreq, phase_degrees)
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Phase")
            ax2.set_yticks([-180, -90, -45, 0, 45, 90, 180])

        elif combobox.get() == 'DCT':
            t = data[:,0]
            signal = data[:,1]
            N = np.arange(n)
            #Before
            ax.plot(t, signal)
            signalDCT = dct(signal)
            print(signalDCT)
            ax2.stem(N, signalDCT)
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Magnitude")
            # plt.yticks([-180, -90, -45, 0, 45, 90, 180])

        elif combobox.get() == 'DC':
            t = data[:,0]
            signal = data[:,1]
            N = np.arange(n)
            signalDC, avg = dc(signal)
            print(signalDC)
            ax.plot(t, signal)
            ax.axhline(avg, color='black', linestyle='-', label='X-axis')
            ax2.plot(N, signalDC)
            ax2.axhline(avg, color='black', linestyle='-', label='X-axis')

        else:

            A = data[:,0]
            PH = data[:,1]
            N = np.arange(n)
            ax.stem(N, A)
            complex_numbers = [amp * np.exp(1j * phase) for amp, phase in zip(A, PH)]

            # ans = np.fft.ifft(complex_numbers)
            ans = idft(complex_numbers)
            print(ans)
            N = len(ans)
            t = np.arange(N)

            ax2.plot(t, ans)
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Magnitude")
            # plt.yticks([-180, -90, -45, 0, 45, 90, 180])
        canvas.draw()
        canvas2.draw()

    root.title("Lab4 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y=650 + 40 * 7)
    next_button = tk.Button(text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y=650 + 40 * 7)
    fig, ax = plt.subplots(figsize=(6, 3))
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax.set_title('Before')
    ax2.set_title('After')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()


    browse = tk.Button(text="Browse", command=browse_file)
    browse.place(x=330, y=500 + 40 * 3)

    combobox = ttk.Combobox(values=['DFT', 'IDFT', 'DCT', 'DC'], state="readonly")
    combobox.current(0)
    combobox.place(x = 300, y=500 + 40 * 4)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)

    frequency_text = tk.Entry()
    frequency_text.place(x=300, y=500 + 40 * 5)

    frequency_label = tk.Label(text="Frequency")
    frequency_label.place(x=230, y=500 + 40 * 5)

    firstM_text = tk.Entry(width=10)
    firstM_label = tk.Label(text="Number of coefficients ")


    index_text = tk.Entry()

    index_label = tk.Label()

    amplitiude_text = tk.Entry()

    amplitiude_label = tk.Label()

    phase_text = tk.Entry()

    phase_label = tk.Label()

    save_button = tk.Button(text="Save", font=("Arial", 11), command=save_file)
    save_button.place(x=630, y=500 + 40 * 3)

    checkbox_var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text="Modification", variable=checkbox_var, command = checkbox_changed)
    checkbox.place(x=230, y=500 + 40 * 6)


    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x=300, y=500 + 40 * 7)

    clear_button = tk.Button(text="Clear", command= clear_button_action)
    clear_button.place(x= 380,  y=500 + 40 * 7)

    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 500 + 40 * 8)

    browse_label = tk.Label()
    browse_label.place(x=450, y= 800)