import tkinter as tk
from tkinter import ttk

import Lab
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.geometry("700x1000")
# root.resizable(False, False)
num = 1
Lab.task(root, num)
# task1.task1(root)

#Run loop
root.mainloop()