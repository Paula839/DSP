
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import practical
import task1
import task2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def task1(root):
    # file path browser
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

    # text fields empty or NAN
    def generate_button_check():
        for text in text_fields:
            try:
                if (text.get() != ""):
                    float(text.get())
                else:
                    return False
            except ValueError:
                return False

        if (float(text_fields[2].get()) <= 0):
            return False
        return True

    # generate the graph with sin and cos
    def generate_button_action():
        ax.clear()
        ax2[0].clear()
        ax2[1].clear()
        sig_type = combobox.get()  # type(sin / cos)
        if browse_label.cget("foreground") == 'green':
            t = np.arange(0, n, 1)
            canvas.get_tk_widget().pack_forget()
            canvas2.get_tk_widget().pack()

            if signal_type == 0:
                x = data[:, 1]
            elif signal_type == 1:
                frequency = data[:, 0]
                amplitude = data[:, 1]
                phase_shift = data[:, 2]
                if (sig_type == 'sin'):
                    x = amplitude * np.sin(2 * np.pi * frequency * t + phase_shift)
                elif sig_type == 'cos':
                    x = amplitude * np.cos(2 * np.pi * frequency * t + phase_shift)

            else:
                raise ValueError("Invalid signal type")

            ax2[0].plot(t, x)
            ax2[1].stem(t, x)
            # ax2[0].set_xlim(0, 25)
            # ax2[0].set_ylim(0, 25)
            # ax2[1].set_xlim(0, 25)
            # ax2[1].set_ylim(0, 25)
            canvas2.draw()
            wrong_label.config(text="")
            return

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return
        else:
            wrong_label.config(text="")

        A = float(text_fields[0].get())  # Amplitude
        F = float(text_fields[1].get())  # Analog Frequency
        Fs = float(text_fields[2].get())  # Sampling Frequency
        θ = float(text_fields[3].get())  # Phase Shift

        t = np.arange(-10, 10, 1 / Fs)
        f = F / Fs;
        if sig_type == "sin":
            signal1 = A * np.sin(2 * np.pi * f * t + θ)
            signal2 = A * np.cos(2 * np.pi * f * t + θ)
        else:
            signal1 = A * np.cos(2 * np.pi * f * t + θ)
            signal2 = A * np.sin(2 * np.pi * f * t + θ)

        if Fs < 2 * F:
            warning_label.config(text='Warning! Acording to the Sampling theorem, Fs should be > 2Fmax')
            warning_label.place(x=170, y=540)

        elif Fs == 2 * F:
            warning_label.config(text='Warning! Nyquist rate')
            warning_label.place(x=280, y=540)


        else:
            warning_label.config(text='')

        canvas2.get_tk_widget().pack_forget()
        canvas.get_tk_widget().pack()
        browse_label.config(text="")
        ax.plot(t, signal1)
        ax.stem(t, signal1)
        if sig_type == "both":
            ax.plot(t, signal2)
            ax.stem(t, signal2)
        # ax.set_xlim([-0.2, max(t)])
        ax.axhline(0, color='black', linestyle='-')
        ax.axvline(0, color='black', linestyle='-')
        ax.set_xlim(0, 10)
        ax.set_ylim(-5, 5)
        canvas.draw()

    def clear_button_action():
        for i in text_fields:
            i.delete(0, "end")
        ax.clear()
        ax2[0].clear()
        ax2[1].clear()
        warning_label.config(text="")
        wrong_label.config(text="")
        browse_label.config(text="", fg="red")
        canvas2.get_tk_widget().pack_forget()
        canvas.get_tk_widget().pack()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Lab1 Task')
        canvas.draw()


    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
        practical.practical(root)
    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
        task2.task2(root)

    # def next_button_action():
    root.title("Lab1 Task")

    fig, ax = plt.subplots()  # task2
    fig2, ax2 = plt.subplots(1, 2)  # task1

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Lab1 Task')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    ax2[0].set_xlabel("Continuous Signal")
    ax2[0].set_ylabel("Continuous Signal")
    ax2[0].set_title("Continuous Signal")
    ax2[1].set_xlabel("Discrete Signal")
    ax2[1].set_ylabel("Discrete Signal")
    ax2[1].set_title("Discrete Signal")

    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    # Create a frame for the text fields
    text_fields_frame = tk.Frame(root)
    text_fields_frame.pack(side=tk.BOTTOM, pady=20)

    # Create labels and corresponding text fields
    browse = tk.Button(text="Browse", command=browse_file)
    browse.place(x=330, y=500)

    or_label = tk.Label(text='Or', font=('Arial', 15))
    or_label.place(x=340, y=570)

    browse_label = tk.Label()
    browse_label.place(x=270, y=530)

    warning_label = tk.Label(fg='orange', font=('Bold', 11))

    labels = ["Amplitude", "Analog Frequency", "Sampling Frequency", "Phase Shift"]
    text_fields = []

    # Positions
    for i in range(4):
        label = tk.Label(text=labels[i])
        label.place(x=220,y= 650 + 40*i)
        text_field = tk.Entry()
        text_field.place(x=350,y=650 + 40*i)
        text_fields.append(text_field)

    type_label = tk.Label(text="Type: ")
    type_label.place(x = 220, y=650 + 40 * 4)
    combobox = ttk.Combobox(values=["sin", "cos", "both"], state="readonly")
    combobox.current(0)
    combobox.place(x = 350, y=650 + 40 * 4)

    # Create the "Generate" button
    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x = 300 , y = 650 + 43 * 5)

    clear_button = tk.Button(text="Clear", command=clear_button_action)
    clear_button.place(x= 390,  y = 650 + 43 * 5)

    next_button = tk.Button( text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y = 650 + 40 * 7)
    # Create the error label
    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 650 + 40 * 7)




