
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task7
import practical
import CompareSignal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def task8(root):
    # file path browser
    def clear_button_action():
        for i in text_fields:
            i.delete(0, "end")

        M_text.delete(0, "end")
        L_text.delete(0, "end")

        wrong_label.config(text="")
        browse_label.config(text="", fg="red")
        browse_label2.config(text="", fg="red")
        ax.clear()
        ax2.clear()
        ax.set_title('Before')
        ax2.set_title('After')
        canvas.draw()
        canvas2.draw()

    def browse_file():

        # Get the file path from the file dialog

        file_path = tk.filedialog.askopenfilename()

        # try:
        parameters = {}
        # Check if the file path ends with .txt extension
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                for line in file:

                    key, value = line.strip().split(' = ')
                    parameters[key.strip()] = value.strip()

                ok = 0
                for combo_value in combobox_array:

                    for key in parameters.keys():
                        if(labels[0] == key):

                            if combo_value.lower() == parameters[key].lower():
                                clear_button_action()
                                combobox.set(combo_value)
                                ok = 1
                                try:
                                    index = labels.index("F2")
                                    if combobox.get() == combobox_array[0] or combobox.get() == combobox_array[1]:

                                        for i in range(len(text_fields)):
                                            text_fields[i].destroy()

                                        text_fields.clear()

                                        labels.pop(index)
                                        index = labels.index("F1")
                                        labels[index] = "FC"
                                        L_text.place(x=350, y=650 + 40 * 6)
                                        M_text.place(x=350, y=650 + 40 * 5)
                                        L_checkbox.place(x=220, y=650 + 40 * 6)
                                        M_checkbox.place(x=220, y=650 + 40 * 5)

                                        for i in range(len(labels)):
                                            labels_array[i].config(text=labels[i])
                                            labels_array[i].place(x=220, y=650 + 40 * i)
                                            if i != 0:
                                                text_field = tk.Entry()
                                                text_field.place(x=350, y=650 + 40 * i)
                                                text_fields.append(text_field)
                                except:
                                    if combobox.get() == combobox_array[2] or combobox.get() == combobox_array[3]:
                                        index = labels.index("FC")

                                        for i in range(len(text_fields)):
                                            text_fields[i].destroy()
                                        text_fields.clear()
                                        labels.insert(index + 1, 'F2')
                                        labels.index('FC')
                                        labels[index] = 'F1'
                                        L_text.place(x=350, y=650 + 40 * 7)
                                        M_text.place(x=350, y=650 + 40 * 6)
                                        L_checkbox.place(x=220, y=650 + 40 * 7)
                                        M_checkbox.place(x=220, y=650 + 40 * 6)

                                        for i in range(len(labels)):
                                            labels_array[i].config(text=labels[i])
                                            labels_array[i].place(x=220, y=650 + 40 * i)
                                            if i != 0:
                                                text_field = tk.Entry()
                                                text_field.place(x=350, y=650 + 40 * i)
                                                text_fields.append(text_field)
                                break
                if ok == 0:
                    browse_label.config(text="Selected file is not a .txt file.", fr='red')
                    return
                for i in  range(1, len(labels)):
                    ok = 0
                    for key in parameters.keys():
                        if(labels[i] == key):

                            text_fields[i-1].insert(0, int(parameters[key]))
                            ok = 1
                            break
                    if ok == 0:
                        browse_label.config(text="Selected file is not a .txt file.", fr='red')
                        return
            browse_label.config(text="File successfully read with NumPy!", fg='green')


        else:
            browse_label.config(text="Selected file is not a .txt file.", fr='red')


    # except Exception as e:
        # browse_label.config(text="Error reading the file:", fg='red')

    def Compare_Signals(file_name, Your_indices, Your_samples):
        expected_indices = []
        expected_samples = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                # process line
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                elif len(L.split("  ")) == 2:
                    L = line.split()
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                else:
                    break
        print("Current Output Test file is: ")
        print(file_name)
        print("\n")
        if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
            print("Test case failed, your signal have different length from the expected one")

            return
        for i in range(len(Your_indices)):
            if (Your_indices[i] != expected_indices[i]):
                print("Test case failed, your signal have different indicies from the expected one")
                return
        for i in range(len(expected_samples)):
            if abs(Your_samples[i] - expected_samples[i]) < 0.1:
                continue
            else:
                print("Test case failed, your signal have different values from the expected one")
                return
        print("Test case passed successfully")

    def browse_file2():

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
                browse_label2.config(text="File successfully read with NumPy!", fg='green')
                # You can perform further processing with the data here


            else:
                browse_label2.config(text="Selected file is not a .txt file.", fr='red')


        except Exception as e:
            browse_label2.config(text="Error reading the file:", fg='red')
    def save_file():

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

    def combobox_selected(event):
        try:
            index = labels.index("F2")
            if combobox.get() == combobox_array[0] or combobox.get() == combobox_array[1]:

                for i in range(len(text_fields)):
                    text_fields[i].destroy()

                text_fields.clear()

                labels.pop(index)
                index = labels.index("F1")
                labels[index] = "FC"
                L_text.place(x=350, y=650 + 40 * 6)
                M_text.place(x=350, y=650 + 40 * 5)
                L_checkbox.place(x=220, y=650 + 40 * 6)
                M_checkbox.place(x=220, y=650 + 40 * 5)

                for i in range(len(labels)):
                    labels_array[i].config(text=labels[i])
                    labels_array[i].place(x=220, y=650 + 40 * i)
                    if i != 0:
                        text_field = tk.Entry()
                        text_field.place(x=350, y=650 + 40 * i)
                        text_fields.append(text_field)
        except:
            if combobox.get() == combobox_array[2] or combobox.get() == combobox_array[3]:
                index = labels.index("FC")

                for i in range(len(text_fields)):
                        text_fields[i].destroy()
                text_fields.clear()
                labels.insert(index + 1, 'F2')
                labels.index('FC')
                labels[index] = 'F1'
                L_text.place(x=350, y=650 + 40 * 7)
                M_text.place(x=350, y=650 + 40 * 6)
                L_checkbox.place(x=220, y=650 + 40 * 7)
                M_checkbox.place(x=220, y=650 + 40 * 6)

                for i in range(len(labels)):
                    labels_array[i].config(text=labels[i])
                    labels_array[i].place(x=220, y=650 + 40 * i)
                    if i != 0:
                        text_field = tk.Entry()
                        text_field.place(x=350, y=650 + 40 * i)
                        text_fields.append(text_field)

    def generate_button_check():

        for text in text_fields:
            try:
                if (text.get() != ""):

                    float(text.get())
                    if(float(text.get()) < 0):
                        return False
                else:
                    return False
                if M_var.get() == 1:
                    if(M_text.get() != ""):
                        float(M_text.get())
                        if(float(M_text.get()) < 0):
                            return False

                    else:
                        return False

                if L_var.get() == 1:
                    if(L_text.get() != ""):
                        float(L_text.get())
                        if(float(L_text.get()) < 0):
                            return False
                    else:
                        return False

            except ValueError:
                print("EX")
                return False

        if (float(text_fields[2].get()) <= 0):
            return False
        return True

    def convolution(signal1, signal2):
        length = len(signal1) + len(signal2) - 1
        new_signal = []
        for k in range(length):
            sum = 0
            for x in range(k, -1, -1):
                if (len(signal1) <= len(signal2)):
                    if x >= len(signal1): continue
                    if k - x >= len(signal2): continue
                    sum += signal1[x] * signal2[k - x]
                else:
                    if x >= len(signal2): continue
                    if k - x >= len(signal1): continue
                    sum += signal2[x] * signal1[k - x]

            new_signal.append(sum)

        return new_signal
    def low_pass(FC1, TransitionBand, N, FS, StopBandAttenuation):
        hd = np.zeros(int(N / 2) + 1)
        w = np.zeros(int(N / 2) + 1)
        F1 = FC1 + TransitionBand / 2
        F1 = F1 / FS
        print(F1)
        for n in range(int(N / 2) + 1):
            if StopBandAttenuation < 21:
                w[n] = 1
            elif StopBandAttenuation < 44:
                w[n] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            elif StopBandAttenuation < 53:
                w[n] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            else:
                w[n] = 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
        for n in range(int(N / 2) + 1):
            if n == 0:
                hd[n] = 2 * F1
            else:
                wc1 = 2 * np.pi * F1
                hd[n] = 2 * F1 * np.sin(n * wc1) / (n * wc1)

        return hd*w

    def high_pass(FC1, TransitionBand, N, FS, StopBandAttenuation):
        w = np.zeros(int(N / 2) + 1)
        for n in range(int(N / 2) + 1):
            if StopBandAttenuation < 21:
                w[n] = 1
            elif StopBandAttenuation < 44:
                w[n] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            elif StopBandAttenuation < 53:
                w[n] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            else:
                w[n] = 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
        hd = np.zeros(int(N / 2) + 1)
        F1 = FC1 - TransitionBand / 2
        F1 = F1 / FS
        for n in range(int(N / 2) + 1):
            if n == 0:
                hd[n] = 1 - 2 * F1
            else:
                wc1 = 2 * np.pi * F1
                hd[n] = -2 * F1 * np.sin(n * wc1) / (n * wc1)

        return hd*w
    def band_pass(FC1, FC2, TransitionBand, N, FS, StopBandAttenuation):
        w = np.zeros(int(N / 2) + 1)
        for n in range(int(N / 2) + 1):
            if StopBandAttenuation < 21:
                w[n] = 1
            elif StopBandAttenuation < 44:
                w[n] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            elif StopBandAttenuation < 53:
                w[n] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            else:
                w[n] = 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
        hd = np.zeros(int(N / 2) + 1)
        F1 = FC1 - TransitionBand / 2
        F2 = FC2 + TransitionBand / 2
        F1 = F1 / FS
        F2 = F2 / FS
        for n in range(int(N / 2) + 1):
            if n == 0:
                hd[n] = 2 * (F2 - F1)
            else:
                wc1 = 2 * np.pi * F1
                wc2 = 2 * np.pi * F2
                hd[n] = 2 * F2 * np.sin(n * wc2) / (n * wc2) - 2 * F1 * np.sin(n * wc1) / (n * wc1)
        return hd*w
    def band_stop(FC1, FC2, TransitionBand, N, FS, StopBandAttenuation):
        w = np.zeros(int(N / 2) + 1)
        for n in range(int(N / 2) + 1):
            if StopBandAttenuation < 21:
                w[n] = 1
            elif StopBandAttenuation < 44:
                w[n] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            elif StopBandAttenuation < 53:
                w[n] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            else:
                w[n] = 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
        hd = np.zeros(int(N / 2) + 1)
        F1 = FC1 + TransitionBand / 2
        F2 = FC2 - TransitionBand / 2
        F1 = F1 / FS
        F2 = F2 / FS
        for n in range(int(N / 2) + 1):
            if n == 0 :
                hd[n] = 1 - 2 * (F2 - F1)
            else:
                wc1 = 2 * np.pi * F1
                wc2 = 2 * np.pi * F2
                hd[n] = 2 * F1 * np.sin(n * wc1) / (n * wc1) - 2 * F2 * np.sin(n * wc2) / (n * wc2)
        return hd*w
    def getN(StopBandAttenuation, TransitionBand, FS):
        if StopBandAttenuation < 21:
            print("Rectangular")
            N = 0.9 * FS / TransitionBand
        elif StopBandAttenuation < 44:
            print("Hanning")
            N = 3.1 * FS / TransitionBand
        elif StopBandAttenuation < 53:
            print("Hamming")
            N = 3.3 * FS / TransitionBand
        else:
            print("Blackman")
            N = 5.5 * FS / TransitionBand
        return N
    def filtering(FilterType, FS, StopBandAttenuation, FC1, FC2, TransitionBand):

        print(StopBandAttenuation)
        if StopBandAttenuation < 21:
            print("Rectangular")
            N = 0.9 * FS / TransitionBand
        elif StopBandAttenuation < 44:
            print("Hanning")
            N = 3.1 * FS / TransitionBand
        elif StopBandAttenuation < 53:
            print("Hamming")
            N = 3.3 * FS / TransitionBand
        else:
            print("Blackman")
            N = 5.5 * FS / TransitionBand

        print(N)
        if int(N) % 2 == 0:
            N = int(N) + 1
        elif int(N) < N:
            N = int(N) + 2


        hd = np.zeros(int(N / 2) + 1)



                #["FilterType", "FS", "StopBandAttenuation", "FC", "TransitionBand"]
        if FilterType.lower() == 'low pass':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = low_pass(FC1, float(text_fields[tr-1].get()),getN(float(text_fields[sa-1].get()), float(text_fields[tr-1].get()), float(text_fields[fs-1].get())),  float(text_fields[fs-1].get()),
                          float(text_fields[sa-1].get()))
        if FilterType.lower() == 'high pass':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = high_pass(FC1, float(text_fields[tr - 1].get()),
                         getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                              float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),
                         float(text_fields[sa - 1].get()))


        if FilterType.lower() == 'band pass':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = band_pass(FC1, FC2,  float(text_fields[tr - 1].get()),
                         getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                              float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),
                         float(text_fields[sa - 1].get()))


        if FilterType.lower() == 'band stop':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = band_stop(FC1, FC2, float(text_fields[tr - 1].get()),
                         getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                              float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),
                         float(text_fields[sa - 1].get()))

        h_symmetric = np.zeros(2 * len(h) - 1)
        for i in range(len(h)):
            h_symmetric[i] = h[len(h) - 1 - i]
            h_symmetric[len(h) + i - 1] = h[i]

        return h_symmetric

    def downsample(signal, factor):
        new_signal = []
        for i in range(len(signal)):
            if i % factor == 0:
                new_signal.append(signal[i])
        return new_signal

    def upsample(signal, factor):
        new_signal = []
        for i in range(len(signal)):
            new_signal.append(signal[i])
            new_signal += [0] * (factor - 1)
        return new_signal

    def generate_button_action():

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return

        wrong_label.config(text="")
        print("==================================================================================================================")
        ax.clear()
        ax2.clear()
        #["FilterType", "FS", "StopBandAttenuation", "F1", "F2", "TransitionBand"]
        print(len(text_fields))

        try:
            signal = filtering(combobox.get(), float(text_fields[0].get()), float(text_fields[1].get()), float(text_fields[2].get())
                               , float(text_fields[3].get()), float(text_fields[4].get()))
        except:
            signal = filtering(combobox.get(), float(text_fields[0].get()), float(text_fields[1].get()), float(text_fields[2].get()), 0, float(text_fields[3].get()))
        tr = labels.index("TransitionBand")
        fs = labels.index('FS')
        sa = labels.index('StopBandAttenuation')
        try:
            fc = labels.index('FC')
        except:
            fc = labels.index("F1")
        if(L_var.get() == 1 and L_text.get() != 0 and (M_var.get() == 0 or M_text.get() == 0)):
            upsample_signal = upsample(signal, int(L_text.get()))
            upsample_signal = low_pass(float(text_fields[fc-1].get()), float(text_fields[tr - 1].get()),
                     getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                          float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),float(text_fields[sa-1].get()))


        elif(M_var.get() == 1 and M_text.get() != 0 and (L_var.get() == 0 or L_text.get() == 0)):
            signal = low_pass(float(text_fields[fc-1].get()), float(text_fields[tr - 1].get()),
                     getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                          float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),float(text_fields[sa-1].get()))
            downsample_signal = downsample(signal, int(M_text.get()))

        elif (M_var.get() == 1 and M_text.get() != 0 and L_var.get() == 1 and L_text.get() != 0):
            new_signal = upsample(signal, int(L_text.get()))
            new_signal =  low_pass(float(text_fields[fc-1].get()), float(text_fields[tr - 1].get()),
                     getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                          float(text_fields[fs - 1].get())), float(text_fields[fs - 1].get()),float(text_fields[sa-1].get()))
            new_signal = downsample(new_signal, int(M_text.get()))

        elif(M_var.get() == 1 and L_var.get() == 1):
            if(M_text.get() == 0 and L_text.get() == 0):
                wrong_label.config(text="Invalid input")
                ax.clear()
                ax2.clear()

        # output = convolution(data[:, 1], signal)
        if browse_label2.cget("foreground") == 'green':
            if M_var.get() == 1 and L_var.get() == 1:
                output = convolution(data[:, 1], new_signal)
                n_values = np.arange(-len(signal) // 2 + 1, len(output) - len(signal) // 2)
                print(output)
                print(n_values)
                ax2.stem(n_values, output, basefmt='b')

                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 1\LPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 3\HPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 5\BPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 7\BSFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", n_values, output)

            elif M_var.get() == 1:
                output = convolution(data[:, 1], downsample_signal)
                n_values = np.arange(-len(signal) // 2 + 1, len(output) - len(signal) // 2)
                print(output)
                print(n_values)
                ax2.stem(n_values, output, basefmt='b')
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 1\LPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 3\HPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 5\BPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 7\BSFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", n_values, output)
            elif L_var.get() == 1:
                output = convolution(data[:, 1], upsample_signal)
                n_values = np.arange(-len(signal) // 2 + 1, len(output) - len(signal) // 2)
                print(output)
                print(n_values)
                ax2.stem(n_values, output, basefmt='b')
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 1\LPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 3\HPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 5\BPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 7\BSFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", n_values, output)
            else:
                output = convolution(data[:, 1], signal)
                n_values = np.arange(-len(signal) // 2 + 1, len(output) - len(signal) // 2)
                print(output)
                print(n_values)
                ax2.stem(n_values, output, basefmt='b')
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 1\LPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 3\HPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 5\BPFCoefficients.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", n_values, output)
                # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 7\BSFCoefficients.txt", n_values, output)
                Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", n_values, output)
        else:
            n_values = np.arange(-len(signal) // 2 + 1,  len(signal) // 2 + 1)
            print(signal)
            print(n_values)
            ax2.stem(n_values, signal, basefmt='b')
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 1\LPFCoefficients.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 3\HPFCoefficients.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 5\BPFCoefficients.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", n_values, signal)
            # Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 7\BSFCoefficients.txt", n_values, signal)
            Compare_Signals("D:\dsp\Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", n_values, signal)
            # plt.show()
        ax.set_title('Before')
        ax2.set_title('After')
        canvas.draw()
        canvas2.draw()








    fig, ax = plt.subplots(figsize=(6, 2.7))
    fig2, ax2 = plt.subplots(figsize=(6, 2.7))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()

    ax.set_title('Before')
    ax2.set_title('After')

    text_fields_frame = tk.Frame(root)
    text_fields_frame.pack(side=tk.BOTTOM, pady=20)

    # Create labels and corresponding text fields
    browse = tk.Button(text="Browse", command=browse_file)
    browse.place(x=330, y=550)
    browse_signal = tk.Button(text="Browse_signal", command=browse_file2)
    browse_signal.place(x=500, y=500 + 40 * 10)

    or_label = tk.Label(text='Or', font=('Arial', 15))
    or_label.place(x=340, y=595)

    browse_label = tk.Label()
    browse_label.place(x=270, y=530)

    browse_label2 = tk.Label()
    browse_label2.place(x=500, y=930)


    warning_label = tk.Label(fg='orange', font=('Bold', 11))

    labels = ["FilterType", "FS", "StopBandAttenuation", "FC", "TransitionBand"]
    text_fields = []
    labels_array = []

    for i in range(len(labels)):
        label = tk.Label(text=labels[i])
        label.place(x=220,y= 650 + 40*i)
        labels_array.append(label)
        if i != 0:
            text_field = tk.Entry()
            text_field.place(x=350,y=650 + 40*i)
            text_fields.append(text_field)

    label = tk.Label(text="")
    labels_array.append(label)

    combobox_array = ['Low Pass', 'High Pass', 'Band Pass', 'Band Stop']

    combobox = ttk.Combobox(values=combobox_array, state="readonly")
    combobox.current(0)
    combobox.place(x=350, y=650)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)
    M_var = tk.IntVar()
    M_checkbox = tk.Checkbutton(root, text="M", variable=M_var)
    M_checkbox.place(x = 220 , y = 650 + 40 * 5)

    M_text = tk.Entry()
    M_text.place(x=350, y=650 + 40 * 5)

    L_var = tk.IntVar()
    L_checkbox = tk.Checkbutton(root, text="L", variable=L_var)
    L_checkbox.place(x = 220 , y = 650 + 40 * 6)

    L_text = tk.Entry()
    L_text.place(x=350, y=650 + 40 * 6)


    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x = 300 , y = 650 + 43 * 7)

    clear_button = tk.Button(text="Clear", command=clear_button_action)
    clear_button.place(x= 390,  y = 650 + 43 * 7)


    wrong_label = tk.Label(fg='red')
    wrong_label.place(x=500, y=550)

    browse_label = tk.Label()
    browse_label.place(x=500, y=550)

    save_button = tk.Button(text="Save", font=("Arial", 11), command=save_file)
    save_button.place(x=630, y=500 + 40 * 3)




