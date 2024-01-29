import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task1

import cmath
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools.msvc import winreg
from tkinter import filedialog


def practical(root):
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

        return hd * w

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

        return hd * w

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
        return hd * w

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
            if n == 0:
                hd[n] = 1 - 2 * (F2 - F1)
            else:
                wc1 = 2 * np.pi * F1
                wc2 = 2 * np.pi * F2
                hd[n] = 2 * F1 * np.sin(n * wc1) / (n * wc1) - 2 * F2 * np.sin(n * wc2) / (n * wc2)
        return hd * w

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

        # ["FilterType", "FS", "StopBandAttenuation", "FC", "TransitionBand"]
        if FilterType.lower() == 'band pass':
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
            return hd * w

        if FilterType.lower() == 'low pass':
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
            return hd * w

        if FilterType.lower() == 'high pass':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = high_pass(FC1, float(text_fields[tr - 1].get()),
                          getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                               loat(text_fields[fs - 1].get()))), float(text_fields[fs - 1].get(),
                                                                        float(text_fields[sa - 1].get()))

        if FilterType.lower() == 'band stop':
            tr = labels.index("TransitionBand")
            fs = labels.index('FS')
            sa = labels.index('StopBandAttenuation')
            h = band_stop(FC1, FC2, float(text_fields[tr - 1].get()),
                          getN(float(text_fields[sa - 1].get()), float(text_fields[tr - 1].get()),
                               loat(text_fields[fs - 1].get()))), float(text_fields[fs - 1].get(),
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

    def dct(signal):
        N = len(signal)
        dct_result = [0] * N

        for k in range(N):
            dct_result[k] = np.sqrt(2 / N) *sum(signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1)) for n in range(N))
        return dct_result

    def dc(signal):
        N = len(signal)
        dct_result = [0] * N
        removed_DC = [0] * N
        values = signal
        global avg
        avg = sum(values) / len(values)

        for i in range(len(values)):
            removed_DC[i] = values[i] - avg
        return removed_DC, avg

    def correlation(signal1, signal2):
        c = len(signal1)
        if len(signal2) < c:
            signal2 = signal2 + [0] * (c - len(signal2))
        elif len(signal2) > c:
            signal2 = signal2[:c]

        sum1 = sum(x ** 2 for x in signal1)
        sum2 = sum(x ** 2 for x in signal2)
        norm = (sum1 * sum2) ** 0.5

        norm_corr = []

        for i in range(c):
            temp = 0

            for j in range(c):
                temp += signal1[j] * signal2[(j + i) % c]

            norm_corr.append(temp / norm)

        return norm_corr

    def preserve_autocorrelation_coefficients(autocorr, num_coefficients):
        # Preserve only the needed coefficients of autocorrelation
        return autocorr[:num_coefficients]

    def normalize_signal(signal):

        min_value = min(signal)
        max_value = max(signal)
        normalized_signal = [((x - min_value) / (max_value - min_value)) * 2 - 1 for x in signal]
        return normalized_signal

    def template_matching(class_signal, test_folder):

        templates = load_templates_from_folders(test_folder)
            # Perform template matching for each class
        similarities = [np.max(correlation(class_signal, template)) for template in templates] #class 1 and class 2

            # Assign the label of the class with the highest similarity
        max_corr_val = 0.0
        j = 0
        for i, value in enumerate(similarities):
            print(value)
            if (abs(value) > max_corr_val):
                max_corr_val = abs(value)
                j = i

        if answer_label.cget("text") == "":
            answer_label.place(x=100, y=500 + 40 * 6)
            if j + 1 == 1:
                answer_label.config(text=f"{file_name}: Class {j + 1}: down movement of EOG signal")
            else:
                answer_label.config(text=f"{file_name}: Class {j + 1}: up movement of EOG signal")
        else:
            if j + 1 == 1:
                answer_label2.config(text=f"{file_name}: Class {j + 1}: down movement of EOG signal")
            else:
                answer_label2.config(text=f"{file_name}: Class {j + 1}: up movement of EOG signal")
    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task1.task1(root)

    def load_templates_from_folders(class_folders):
        # Load templates from class folders
        templates = []
        for folder in class_folders:
            folder_templates = []
            files = os.listdir(folder)
            for file in files:
                template = np.loadtxt(os.path.join(folder, file))
                folder_templates.append(template)
            # Concatenate all templates from the current folder into one template
            concatenated_template = np.concatenate(folder_templates)

            templates.append(concatenated_template)
        print(templates)
        return templates

    def browse_file():

        # Get the file path from the file dialog

        try:
            folder_path = filedialog.askdirectory()

            if not folder_path:
                # User canceled the dialog or selected a file
                browse_label.config(text="No folder selected!", fg='red')
            else:
                # User selected a valid folder
                browse_label.config(text="Folder successfully read with NumPy!", fg='green')
                global class1
                class1 = folder_path

        except Exception as e:
            browse_label.config(text="Error reading the folder:", fg='red')


    def browse_file2():
        folder_path = filedialog.askdirectory()

        if not folder_path:
            # User canceled the dialog or selected a file
            browse_label.config(text="No folder selected!", fg='red')
        else:
            # User selected a valid folder
            browse_label.config(text="Folder successfully read with NumPy!", fg='green')
            global class2
            class2 = folder_path

    def browse_file3():

        # Get the file path from the file dialog

            folder_path = filedialog.askdirectory()

            if not folder_path:
                # User canceled the dialog or selected a file
                browse_label.config(text="No folder selected!", fg='red')
            else:
                # User selected a valid folder
                browse_label.config(text="Folder successfully read with NumPy!", fg='green')
                global ttest
                ttest  = folder_path



    def clear_button_action():
        wrong_label.config(text="")
        answer_label.config(text="")
        answer_label2.config(text="")
        browse_label.config(text="", fg="red")
        browse_label2.config(text="", fg="red")
        browse_label3.config(text="", fg="red")
        browse3.place(x=4800, y=500 + 40 * 3)

    # def generate_button_check():
    #     if browse_label.cget("foreground") != 'green':
    #         return False
    #     if browse_label2.cget("foreground") != 'green':
    #         return False
    #     if combobox.get() == combobox_array[2]:
    #         if browse_label2.cget("foreground") != 'green':
    #             return False
    #     return True





    def generate_button_action():

        # if (generate_button_check() == False):
        #     wrong_label.config(text="Invalid input")
        #     return
        wrong_label.config(text="")
        print("==================================================================================================================")

        ax.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()

        '''
        This function takes paths for two ECG folders of two subjects A & B and a test ECG folder., its sampling frequency ‘Fs’, 
        the minimum ‘miniF’& maximum frequency ‘maxF’ of the signal and new sampling frequency ‘newFs’ as an input and then do the following:
        '''
        class1_folder = class1
        class2_folder = class2
        test_folder = ttest
        templates = load_templates_from_folders([class1_folder, class2_folder])



        # 1-Filter the signal using FIR filter with band [miniF, maxF].
        signal = filtering("band pass", float(fs.get()), 50,float(minf.get()), float(maxf.get()), 500)
        # 2-Resample the signal to newFs only if newFs doesn’t destroy the signal, else show a message to the user “ newFs is not valid”
        # -and continue executing the next instructions.
        if float(newf.get()) < 2*float(maxf.get()):
            print("WRONG")
        else:
            signal = filtering("band pass", float(newf.get()), 50, float(minf.get()), float(maxf.get()), 500)



        # 3-Remove the DC component.
        dc_signal = dc(signal)
        # 4-Normalize the signal to be from -1 to 1.
        # norm_signal = normalize_signal(dc_signal)
        # 5-Compute Auto correlation for each ECG segment.
        cor_signal = correlation(templates[0], templates[1])
        # 6-Preserve only the needed coefficients for the computed auto correlation.
        coe_signal = preserve_autocorrelation_coefficients(cor_signal, 5)
        # 7-Compute DCT.
        dct_signal = dct(cor_signal)
        # 8-Use template matching to compare the non-zero values of the computed DCT and label each ECG segment in the test folder as subject A or B.
        template_matching(dct_signal, test_folder)
        # 9-Display original signal, after autocorrelation, after preserving the needed coefficients of autocorrelation, DCT and the label of each test case.

        ax.set_title('original signal')
        ax2.set_title('after autocorrelation')
        ax3.set_title('after preserving the needed coefficients of autocorrelation')
        ax4.set_title('DCT')
        ax5.set_title('After')
        canvas.draw()
        canvas2.draw()
        canvas3.draw()
        canvas4.draw()
        canvas5.draw()

    root.title("Practical task 2")
    # prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    # prev_button.place(x=10, y=650 + 40 * 7)
    vary = 1.8
    fig, ax = plt.subplots(figsize=(6, vary))
    fig2, ax2 = plt.subplots(figsize=(6, vary))
    fig3, ax3 = plt.subplots(figsize=(6, vary))
    fig4, ax4 = plt.subplots(figsize=(6, vary))
    fig5, ax5 = plt.subplots(figsize=(6, vary))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    canvas4 = FigureCanvasTkAgg(fig4, master=root)
    canvas5 = FigureCanvasTkAgg(fig5, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
    canvas3.get_tk_widget().pack()
    canvas4.get_tk_widget().pack()
    canvas5.get_tk_widget().pack()
    #after autocorrelation, after preserving the needed coefficients of autocorrelation, DCT and the label of each test case.

    ax.set_title('original signal')
    ax2.set_title('after autocorrelation')
    ax3.set_title('after preserving the needed coefficients of autocorrelation')
    ax4.set_title('DCT')
    ax5.set_title('After')

    browse = tk.Button(text="Browse1", command=browse_file)
    browse.place(x=300, y=500 + 42 * 10)

    browse2 = tk.Button(text="Browse2", command=browse_file2)
    browse2.place(x=390, y=500 + 42 * 10)


    browse3 = tk.Button(text="Test", command=browse_file3)
    browse3.place(x=480, y=500 + 42 * 10)

    # combobox_array = ['Correlation', 'Time Analysis', 'Template Matching']
    # combobox = ttk.Combobox(values=combobox_array, state="readonly")
    # combobox.current(0)
    # combobox.place(x = 300, y=500 + 40 * 4)
    # combobox.bind("<<ComboboxSelected>>", combobox_selected)
    # number_text = tk.Entry()
    # number_text.place(x=300, y=500 + 40 * 5)
    #
    # number_label = tk.Label(text="Window Size")
    # number_label.place(x=220, y=500 + 40 * 5)

    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x=340, y=500 + 42 * 11)

    # clear_button = tk.Button(text="Clear", command= clear_button_action)
    # clear_button.place(x= 380,  y=500 + 40 * 7)

    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 500 + 40 * 10)

    answer_label = tk.Label()
    answer_label.place(x = 100 , y = 500 + 40 * 10)

    answer_label2 = tk.Label()
    answer_label2.place(x = 100 , y = 500 + 40 * 10)

    answer_label.config(text="")
    answer_label2.config(text="")

    browse_label = tk.Label()
    browse_label.place(x=450, y= 800)

    browse_label2 = tk.Label()
    browse_label2.place(x=450, y= 830)

    browse_label3 = tk.Label()
    browse_label3.place(x=450, y= 860)

    next_button = tk.Button(text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y=650 + 40 * 7)



    fs = tk.Entry()
    fs.place(x=80, y=500 + 41 * 10)

    minf = tk.Entry()
    minf.place(x=80, y=500 + 43 * 10)

    maxf = tk.Entry()
    maxf.place(x=80, y=500 + 45 * 10)

    newf = tk.Entry()
    newf.place(x=80, y=500 + 47 * 10)