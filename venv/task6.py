import math
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import task5
import task6
import task7
import cmath
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools.msvc import winreg
from tkinter import filedialog


def task6(root):
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

    def time_delay_analysis(signal1, signal2, Ts):
        norm_corr = correlation(signal1, signal2)
        print(norm_corr)
        max_corr_index = 0.0
        j = 0
        for i, value in enumerate(norm_corr):
            if (abs(value) > max_corr_index):
                max_corr_index = abs(value)
                j = i
        time_delay = j * Ts
        return time_delay

    def template_matching(class_folders, test_folder):
        # Load templates from class folders
        templates = load_templates_from_folders(class_folders)

        # Iterate through signals in the test folder
        for file_name in os.listdir(test_folder):
            test_signal = np.loadtxt(os.path.join(test_folder, file_name))

            # Perform template matching for each class
            similarities = [np.max(correlation(test_signal, template)) for template in templates] #class 1 and class 2

            # Assign the label of the class with the highest similarity
            max_corr_index = 0.0
            j = 0
            for i, value in enumerate(similarities):
                print(value)
                if (abs(value) > max_corr_index):
                    max_corr_index = abs(value)
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

    def combobox_selected(event):
        clear_button_action()
        if combobox.get() == combobox_array[2]:
            browse3.place(x=480, y=500 + 40 * 3)

    def prev_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        # num = 2
        task5.task5(root)

    def next_button_action():
        for widget in root.winfo_children():
            widget.destroy()
        task7.task7(root)

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
        if combobox.get() == combobox_array[2]:
            folder_path = filedialog.askdirectory()

            if not folder_path:
                # User canceled the dialog or selected a file
                browse_label.config(text="No folder selected!", fg='red')
            else:
                # User selected a valid folder
                browse_label.config(text="Folder successfully read with NumPy!", fg='green')
                global class1
                class1 = folder_path

        else:
            try:
                # Check if the file path ends with .txt extension'
                file_path = tk.filedialog.askopenfilename()
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
        if combobox.get() == combobox_array[2]:
            folder_path = filedialog.askdirectory()

            if not folder_path:
                # User canceled the dialog or selected a file
                browse_label2.config(text="No folder selected!", fg='red')
            else:
                # User selected a valid folder
                browse_label2.config(text="Folder successfully read with NumPy!", fg='green')
                global class2
                class2 = folder_path

        else:
            try:
                # Check if the file path ends with .txt extension
                file_path = tk.filedialog.askopenfilename()
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

    def browse_file3():

        # Get the file path from the file dialog
        if combobox.get() == combobox_array[2]:
            folder_path = filedialog.askdirectory()

            if not folder_path:
                # User canceled the dialog or selected a file
                browse_label3.config(text="No folder selected!", fg='red')
            else:
                # User selected a valid folder
                browse_label3.config(text="Folder successfully read with NumPy!", fg='green')
                global ttest
                ttest = folder_path

        else:
            browse_label3.config(text="Error reading the folder:", fg='red')


    def clear_button_action():
        wrong_label.config(text="")
        answer_label.config(text="")
        answer_label2.config(text="")
        browse_label.config(text="", fg="red")
        browse_label2.config(text="", fg="red")
        browse_label3.config(text="", fg="red")
        browse3.place(x=4800, y=500 + 40 * 3)

    def generate_button_check():
        if browse_label.cget("foreground") != 'green':
            return False
        if browse_label2.cget("foreground") != 'green':
            return False
        if combobox.get() == combobox_array[2]:
            if browse_label2.cget("foreground") != 'green':
                return False
        return True


    def generate_button_action():

        if (generate_button_check() == False):
            wrong_label.config(text="Invalid input")
            return
        wrong_label.config(text="")
        print("==================================================================================================================")
        if combobox.get() == combobox_array[0]: #Correlation
            answer_label.place(x=40, y=500 + 40 * 6)
            answer_label.config(text=f"Correlations : {correlation(data[:,1], data2[:,1])}")
        elif combobox.get() == combobox_array[1]: #Time Analysis
            answer_label.place(x=350, y=500 + 40 * 6)
            answer = time_delay_analysis(data[:,1], data2[:,1], 1/100)
            answer_label.config(text=f"Time Delay = {answer}")
        elif combobox.get() == combobox_array[2]: #Template Matching
            class1_folder = class1
            class2_folder = class2
            test_folder = ttest

            template_matching([class1_folder, class2_folder], test_folder)

    root.title("Lab7 Task")
    prev_button = tk.Button(text="Previous", font=("Arial", 10), command=prev_button_action)
    prev_button.place(x=10, y=650 + 40 * 7)
    # fig, ax = plt.subplots(figsize=(6, 3))
    # fig2, ax2 = plt.subplots(figsize=(6, 3))
    # fig3, ax3 = plt.subplots(figsize=(6, 3))
    # canvas = FigureCanvasTkAgg(fig, master=root)
    # canvas2 = FigureCanvasTkAgg(fig2, master=root)
    # canvas3 = FigureCanvasTkAgg(fig3, master=root)
    # canvas.get_tk_widget().pack()
    # canvas2.get_tk_widget().pack()
    # # canvas3.get_tk_widget().pack()
    # ax.set_title('Before')
    # ax2.set_title('After')
    browse = tk.Button(text="Browse1", command=browse_file)
    browse.place(x=300, y=500 + 40 * 3)

    browse2 = tk.Button(text="Browse2", command=browse_file2)
    browse2.place(x=390, y=500 + 40 * 3)


    browse3 = tk.Button(text="Test", command=browse_file3)
    # browse3.place(x=480, y=500 + 40 * 3)

    combobox_array = ['Correlation', 'Time Analysis', 'Template Matching']
    combobox = ttk.Combobox(values=combobox_array, state="readonly")
    combobox.current(0)
    combobox.place(x = 300, y=500 + 40 * 4)
    combobox.bind("<<ComboboxSelected>>", combobox_selected)
    # number_text = tk.Entry()
    # number_text.place(x=300, y=500 + 40 * 5)
    #
    # number_label = tk.Label(text="Window Size")
    # number_label.place(x=220, y=500 + 40 * 5)

    generate_button = tk.Button(text="Generate", command=generate_button_action)
    generate_button.place(x=340, y=500 + 40 * 5)

    # clear_button = tk.Button(text="Clear", command= clear_button_action)
    # clear_button.place(x= 380,  y=500 + 40 * 7)

    wrong_label = tk.Label(fg='red')
    wrong_label.place(x = 300 , y = 500 + 40 * 8)

    answer_label = tk.Label()
    answer_label.place(x = 100 , y = 500 + 40 * 6)

    answer_label2 = tk.Label()
    answer_label2.place(x = 100 , y = 500 + 40 * 7)

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