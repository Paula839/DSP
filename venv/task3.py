import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task2
import task3
import task4
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def task3(root):
    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task2.task2(root)

    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task4.task4(root)

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

    def quantization_check():
        if browse_label.cget("foreground") != 'green':
            return False
        try:
             if levels_bits_entry.get() != "":
                 int(levels_bits_entry.get())
             else:
                 return False
        except ValueError:
            return False
        return True

    def quantization():
        if(quantization_check() == False) :
            wrong_label.config(text="Invalid input")
            return
        else:
            wrong_label.config(text="")

        ax.clear()
        ax2.clear()


        if choice_var.get() == 2:
            levels = 2 ** int(levels_bits_entry.get())
        else:
            levels = int(levels_bits_entry.get())
        minimum = min(data[:, 1])
        maximum = max(data[:, 1])

        delta = (max(data[:, 1]) - min(data[:, 1])) / levels

        def make_ranges(minimum, delta):
            var = minimum
            ranges = []
            for i in range(0, levels):
                x = var + delta
                r = (var, x)
                ranges.append(r)
                var = x
            return ranges

        ranges = make_ranges(minimum, delta)
        midpoints = []
        upper_bounds = []
        lower_bounds = []
        for tuple_item in ranges:
            first_element = tuple_item[0]
            second_element = tuple_item[1]
            upper_bounds.append(second_element)
            lower_bounds.append(first_element)
            midpoint = (first_element + second_element) / 2
            midpoints.append(midpoint)
        Quantized_y = []
        interval_indices = []
        encoded = []
        error_val = []
        for x in data[:, 1]:
            for i in range(0, len(upper_bounds)):
                if (x > lower_bounds[i] and x < upper_bounds[i]):
                    interval_indices.append(i + 1)
                    encoded.append(bin(i)[2:].zfill(int(math.log(int(levels), 2))))
                    break
                elif (x <= lower_bounds[0]):
                    interval_indices.append(i + 1)
                    encoded.append(bin(i)[2:].zfill(int(math.log(int(levels), 2))))
                    break
                elif (x >= upper_bounds[len(upper_bounds) - 1]):
                    interval_indices.append(len(upper_bounds))
                    encoded.append(bin(len(upper_bounds) - 1)[2:].zfill(int(math.log(int(levels), 2))))

                    break
        for i in interval_indices:
            Quantized_y.append(midpoints[i - 1])

        for i in range(0, len(data[:, 1])):
            error_val.append(Quantized_y[i] - data[i][1])

        print(Quantized_y)
        print(data[:, 1])
        # return Quantized_y, interval_indices
        if choice_var.get() == 2:
         result_label.config(text=f"Interval Indices: {encoded}\nQuantized Signal: {Quantized_y}")
        else:
            result_label.config(text=f"Interval Indices: {interval_indices}\nEncoded: {encoded}\nQuantized Signal: {Quantized_y}\n Error: {error_val}")

        ax.plot(data[:, 0], data[:, 1])
        ax2.stem(data[:, 0], Quantized_y)
        # ax.set_xlabel("Frequency (Hz)")
        # ax.set_ylabel("Magnitude")
        canvas.draw()
        canvas2.draw()


    root.title("Lab3 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y=650 + 40 * 7)
    next_button = tk.Button(text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y=650 + 40 * 7)

    fig, ax = plt.subplots(figsize=(6, 2))
    fig2, ax2 = plt.subplots(figsize=(6, 2))
    ax.set_title('Lab3 Task')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()

    choice_var = tk.IntVar()
    choice_var.set(1)

    label = tk.Label(root, text="Upload a signal file and choose quantization method:")
    label.place()

    upload_button = tk.Button(root, text="Browse Signal", command=browse_file)
    upload_button.pack()

    levels_bits_label = tk.Label(root, text="Enter number of levels or bits:")
    levels_bits_label.pack()

    levels_bits_entry = tk.Entry(root)
    levels_bits_entry.pack()

    level_button = tk.Radiobutton(root, text="Levels", variable=choice_var, value=1)
    level_button.pack()

    bits_button = tk.Radiobutton(root, text="Bits", variable=choice_var, value=2)
    bits_button.pack()

    quantize_button = tk.Button(root, text="Quantize", command=quantization)
    quantize_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 500 + 40 * 8)

    browse_label = tk.Label()
    browse_label.place(x=300, y= 630)
