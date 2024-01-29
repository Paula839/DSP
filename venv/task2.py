import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task1
import task2
import task3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def task2(root):
    def on_entry_click(event):
        if text_field.get() == placeholder_text:
            text_field.delete(0, tk.END)
            text_field.config(fg='black')

    def on_entry_leave(event):
        if text_field.get() == '':
            text_field.insert(0, placeholder_text)
            text_field.config(fg='gray')

    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 1
        task1.task1(root)

    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 4
        task3.task3(root)

    def combobox_selected(event):
        browse1_label.config(text="")
        browse2_label.config(text="")

        if combobox.get() == list[0] or combobox.get() == list[1]:
            browse2.place(x=475, y=643 + 40 * 3)
            range_combobox.place(x=5000, y=645 + 40 * 3)
            text_field.place(x=5000, y=645 + 40 * 3)
            text_field.config(text="")
        elif combobox.get() == list[5]:
            range_combobox.place(x=475, y=645 + 40 * 3)
            browse2.place(x=5000, y=643 + 40 * 3)
            text_field.place(x=5000, y=645 + 40 * 3)
            text_field.config(text="")
        elif combobox.get() == list[3] or  combobox.get() == list[6]:
            browse2.place(x=5000, y=643 + 40 * 3)
            range_combobox.place(x=5000, y=645 + 40 * 3)
            text_field.place(x=5000, y=645 + 40 * 3)
            text_field.config(text="")
        else:
            text_field.place(x=475, y=645 + 40 * 3)
            browse2.place(x=5000, y=643 + 40 * 3)
            range_combobox.place(x=5000, y=645 + 40 * 3)


    def browse1_file():

        # Get the file path from the file dialog
        file_path = tk.filedialog.askopenfilename()
        try:
            # Check if the file path ends with .txt extension
            if file_path.endswith('.txt'):
                global data1
                data1 = np.loadtxt(file_path, max_rows=3)
                signal_type = int(data1[0])
                is_periodic = int(data1[1])
                global n
                n = int(data1[2])
                data1 = np.loadtxt(file_path, skiprows=3)
                browse1_label.config(text="Signal1 successfully read with NumPy!", fg='green')
                # You can perform further processing with the data here


            else:
                browse1_label.config(text="Selected Signal1 is not a .txt file.", fr='red')


        except Exception as e:
            browse1_label.config(text="Error reading Signal1:", fg='red')

    def browse2_file():

        # Get the file path from the file dialog
        file_path = tk.filedialog.askopenfilename()
        try:
            # Check if the file path ends with .txt extension
            if file_path.endswith('.txt'):
                global data2
                data2 = np.loadtxt(file_path, max_rows=3)
                signal_type = int(data2[0])
                is_periodic = int(data2[1])
                global n
                n = int(data2[2])
                data2 = np.loadtxt(file_path, skiprows=3)
                browse2_label.config(text="Signal2 successfully read with NumPy!", fg='green')
                # You can perform further processing with the data here


            else:
                browse2_label.config(text="Selected Signal2 is not a .txt file.", fr='red')


        except Exception as e:
            browse2_label.config(text="Error reading Signal2:", fg='red')

    def generate_button_check():
        try:
            if (combobox.get() == list[2] or combobox.get() == list[4]):
                if browse1_label.cget("foreground") == 'green' and text_field.get() != "":
                    float(text_field.get())
                    return True
                return False
            elif combobox.get() == list[5] or combobox.get() == list[3] or combobox.get() == list[6]:
                if  browse1_label.cget("foreground") == 'green' :
                    return True
                return False
            else:
               if browse1_label.cget("foreground") == 'green' and browse2_label.cget("foreground") == 'green':
                return True
            return False
        except ValueError:
            return False

    #  list = ["Addition", "Subtraction", "Multiplication", "Squaring", "Shifting", "Normalization", "Accumulation "]
    def generate_button_action():

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return
        else:
            wrong_label.config(text="")
        print("==================================================================================================================")
        ax.clear()
        ax2.clear()
        ax3.clear()
        x = np.arange(0, n, 1)
        ax.plot(x, data1[:, 1])

        if combobox.get() == list[0]: #data1 and data2
            canvas3.get_tk_widget().pack()
            ADD = data1[:,1]+data2[:,1]
            ax2.plot(x, data2[:, 1])
            ax3.plot(x,ADD)
            print(data1[:, 1])
            print(data2[:, 1])
            print(ADD)

        elif combobox.get() == list[1]: # data 1 and data2
            canvas3.get_tk_widget().pack()
            SUB = data1[:,1] - data2[:,1]
            ax2.plot(x, data2[:, 1])
            ax3.plot(x,SUB)
            print(data1[:, 1])
            print(data2[:, 1])
            print(SUB)

        elif combobox.get() == list[2]: # data1 and the constant
            canvas3.get_tk_widget().pack_forget()
            MULTI =  float(text_field.get()) * data1[:, 1]
            ax2.plot(x, MULTI)
            print(data1[:, 1])
            print(MULTI)

        elif combobox.get() == list[3]:
            canvas3.get_tk_widget().pack_forget()
            ax2.plot(x, data1[:,1] * data1[:, 1]) #squaring
            print(data1[:, 1])
            print(data1[:, 1] * data1[:, 1])
        elif combobox.get() == list[4]:
            canvas3.get_tk_widget().pack_forget()
            ax2.plot(x+float(text_field.get()), data1[:,1])
            print(data1[:, 1])
            print(x+float(text_field.get()))

        elif combobox.get() == list[5]:
            canvas3.get_tk_widget().pack_forget()
            ax2.plot(x, normalize_signal(data1[:,1], range_combobox.get()))
            print(data1[:, 1])
            print(normalize_signal(data1[:,1], range_combobox.get()))

        elif combobox.get() == list[6]:
            canvas3.get_tk_widget().pack_forget()
            Acc = np.cumsum(data1[:, 1])
            ax2.plot(x, Acc)
            print(data1[:, 1])
            print(Acc)



        canvas.draw()
        canvas2.draw()
        if combobox.get() == list[0] or combobox.get() == list[1]:
            canvas3.draw()

    def clear_button_action():
        text_field.delete(0, "end")
        ax.clear()
        ax2.clear()
        ax3.clear()
        wrong_label.config(text="")
        browse1_label.config(text="", fg="red")
        browse2_label.config(text="", fg="red")
        canvas.draw()
        canvas2.draw()
        canvas3.get_tk_widget().pack_forget()

    def normalize_signal(signal, range_option):
        if range_option == range_list[1]:
            min_value = min(signal)
            max_value = max(signal)
            normalized_signal = [(x - min_value) / (max_value - min_value) for x in signal]
        else:
            min_value = min(signal)
            max_value = max(signal)
            normalized_signal = [((x - min_value) / (max_value - min_value)) * 2 - 1 for x in signal]
        return normalized_signal

    root.title("Lab2 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y = 650 + 40 * 7)
    next_button = tk.Button(text="Next", font=("Arial", 10), command=next_button_action)
    next_button.place(x=650, y=650 + 40 * 7)
    fig, ax = plt.subplots(figsize=(6,2))
    fig2, ax2 = plt.subplots(figsize=(6,2))
    fig3, ax3 = plt.subplots(figsize=(6,2))
    ax.set_title('Lab2 Task')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    canvas.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
    # canvas3.get_tk_widget().pack()
    list = ["Addition", "Subtraction", "Multiplication", "Squaring", "Shifting", "Normalization", "Accumulation "]
    combobox = ttk.Combobox(values=list, state="readonly")
    combobox.current(0)
    combobox.place(x = 200, y=650 + 40 * 3)
    browse1_label = tk.Label()
    browse2_label = tk.Label()
    browse1 = tk.Button( text="Signal1 Browse", font=("Arial", 10), command=browse1_file)
    browse1.place(x=360, y = 643 + 40 * 3)
    browse2 = tk.Button( text="Signal2 Browse", font=("Arial", 10),command=browse2_file)
    browse2.place(x=475, y = 643 + 40 * 3)
    placeholder_text = "Enter Constant Value!"
    text_field = tk.Entry(root, fg='gray')
    text_field.insert(0, placeholder_text)
    text_field.bind('<FocusIn>', on_entry_click)
    text_field.bind('<FocusOut>', on_entry_leave)
    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x = 325 , y = 650 + 43 * 4)
    browse1_label.place(x=450, y= 650 + 40 * 4)
    browse2_label.place(x=450, y= 670 + 40 * 4)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)
    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 650 + 40 * 7)
    clear_button = tk.Button(text="Clear", command=clear_button_action)
    clear_button.place(x= 420,  y = 650 + 43 * 4)
    range_list = ['-1 to 1', '0 to 1']
    range_combobox = ttk.Combobox(values=range_list, state="readonly")
    range_combobox.current(0)

    # text_field.place(x=475, y = 643 + 40 * 3)
