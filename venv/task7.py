import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task6
import task8
import cmath
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools.msvc import winreg
from PIL import Image, ImageTk

def task7(root):
    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
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

    def fast_convolution(signal1, signal2):
        N = len(signal1) + len(signal2) - 1

        '''
        Yn = Xn * Hn -> o(n^2)
        Yk = Xk * Hk -> o(n)
        Xk = dft(Xn), Hk = dft(Xn)
        Yn = idft(Yk)
        '''
        for i in range(N-len(signal1)):
          signal1 = np.append(signal1, 0)
        for i in range(N-len(signal2)):

         signal2 = np.append(signal2, 0)

        #  Yk = Xk * Hk -> o(n)
        X = dft(signal1)
        H = dft(signal2)
        Yk = [X[k] * H[k] for k in range(N)]
        ###########################################

        #Yn = idft(Yk)
        Yn = idft(Yk)

        result_rounded = [round(x.real) for x in Yn]
        return result_rounded


    def fast_correlation(signal1, signal2):
            f_signal1 = dft(signal1)
            f_signal2 = dft(signal2)

            f_signal1_conj = [val.conjugate() for val in f_signal1]

            correlation_result_freq = [f_signal1_conj[k] * f_signal2[k] for k in range(len(f_signal1))]

            correlation_result = idft(correlation_result_freq)

            normalized_result = [val / len(signal1) for val in correlation_result]
            normalized_result = [round(val.real, 8) for val in normalized_result]  # Round real parts for comparison
            return normalized_result


    def clear_button_action():
        wrong_label.config(text="")
        browse_label.config(text="", fg="red")
        browse_label2.config(text="", fg="red")
        ax.clear()
        ax2.clear()
        ax3.clear()
        ax.set_title('Before')
        ax3.set_title('After')
        canvas.draw()
        canvas2.draw()
        canvas3.draw()

    def combobox_selected(event):
        clear_button_action()

    def generate_button_check():
        if browse_label.cget("foreground") != 'green':
            return False
        if browse_label2.cget("foreground") != 'green':
            return False
        return True

    def generate_button_action():

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return

        wrong_label.config(text="")
        print("==================================================================================================================")
        ax.clear()
        ax2.clear()
        ax3.clear()
        if combobox.get() ==  combobox_array[0]: # Fast Convolution
            signal1 = data[:,1]
            signal2 = data2[:,1]
            N = np.arange(n)
            # Before
            ax.stem(N, signal1)
            print("Signal 1 = ", signal1)
            N = np.arange(n2)
            ax2.stem(N, signal2)
            print("Signal 2 = ", signal2)
            # After
            m = min(data[0][0], data2[0][0])
            N = np.arange(m, len(data)  + len(data2) + m - 1)
            signalConvolution = fast_convolution(signal1, signal2)
            ax3.stem(N, signalConvolution)
            print("Fast Convolution = ", N)
            print("Fast Convolution = ", signalConvolution)
            # plt.yticks([-180, -90, -45, 0, 45, 90, 180])

        elif combobox.get() ==  combobox_array[1]: # Fast Correlation
            signal1 = data[:,1]
            signal2 = data2[:,1]
            N = np.arange(n)
            # Before
            ax.stem(N, signal1)
            print("Signal 1 = ", signal1)
            N = np.arange(n2)
            ax2.stem(N, signal2)
            print("Signal 2 = ", signal2)
            # After
            signalCorrelation = fast_correlation(signal1, signal2)
            ax3.stem(N, signalCorrelation)
            print("Fast Correlation = ", np.array(N))
            print("Fast Correlation = ", signalCorrelation)
            label.pack(pady=20)
            start_button.pack()



        ax.set_title('Before')
        ax3.set_title('After')
        canvas.draw()
        canvas2.draw()
        canvas3.draw()




    def update_text(index=0):
        current_text = original_text[:index]
        label.config(text=current_text)

        if index < len(original_text):
            index += 1
            root.after(50, update_text, index)  # Update every 100 milliseconds
        else:
            root.after(1500, display_photo())

    def start_animation():
        start_button.config(state=tk.DISABLED, disabledforeground='blue') # Disable the button to prevent multiple clicks
        update_text()

    def display_photo():
        image_path = "D:\dsp\SECRET\dr.Omar.jpg"  # Replace with the actual path to your image
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo  # Keep a reference to the image to prevent garbage collection

    root.title("Lab6 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y=650 + 40 * 7)
    fig, ax = plt.subplots(figsize=(6, 2))
    fig2, ax2 = plt.subplots(figsize=(6, 2))
    fig3, ax3 = plt.subplots(figsize=(6, 2))

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    photo_label = tk.Label(root)
    photo_label.pack()
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
    canvas3.get_tk_widget().pack()

    ax.set_title('Before')
    ax3.set_title('After')
    browse = tk.Button(text="Browse1", command=browse_file)
    browse.place(x=300, y=500 + 40 * 3)

    browse2 = tk.Button(text="Browse2", command=browse_file2)
    browse2.place(x=390, y=500 + 40 * 3)


    combobox_array = ['Fast Convolution', 'Fast Correlation']
    combobox = ttk.Combobox(values=combobox_array, state="readonly")
    combobox.current(0)
    combobox.place(x = 300, y=500 + 40 * 6)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)

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
    original_text = "Finallyyyyy! The last task :D\nThanks for everything dr. Omar <3 <3\nWe hope to see you again <33"
    secret_label = tk.Label()

    secret_label.place(x=210, y=690)
    # secret_label.config(text="Finallyyyyy! The last task :D\nThanks for everything dr. Omar <3 <3\nWe hope see you again <3", font=("Arial", 15))
    label = tk.Label(root, text="What do you think of our efforts??", font=("Arial", 18))
    start_button = tk.Button(root, text="LIKE", command=start_animation,  font=("Arial", 12))


