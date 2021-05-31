# import bibliotek
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import pandas as pd
from tkinter import filedialog
import os


root = tk.Tk()
root.title('Projekcik z Pythona')
root.geometry("950x500")
root.config(bg='#2c2f33')

# podział okna na dwie części
leftframe = tk.Frame(root, bg='#191970')
leftframe.pack(side='left', fill=tk.BOTH, expand=True)
rightframe = tk.Frame(root)
rightframe.pack(side='right', fill=tk.BOTH, expand=True)

# podział lewego okna na dwie części
firstframe = tk.Frame(leftframe, bg='#191970')
firstframe.pack(side='top', fill=tk.BOTH, expand=True)
secondframe = tk.Frame(leftframe, bg="#4949AD")
secondframe.pack(side='bottom', fill=tk.BOTH, expand=True)

# wczytanie danych
frame = pd.read_csv('test.csv')

def file_open():
    global chosen_file
    chosen_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wybierz plik",
                                               filetypes=(("pliki csv", "*.csv"), ("wszystkie pliki", "*.*")))      # directory to change

file_button = tk.Button(master=firstframe, text="Wybierz plik", command=file_open).grid(column=0, row=0, columnspan=2)

# tworzenie wykresu
figure = plt.Figure(figsize=(3, 3), dpi=100)
ax = figure.add_subplot(111)
ax.plot(frame['colB'])

canvas = FigureCanvasTkAgg(figure, rightframe)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, rightframe)
toolbar.update()
toolbar.place(x=0, y=0)
canvas._tkcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# nazwy osi\kolumn
axes_names = frame.columns

# przycisk do wyboru osi x
x_mode = axes_names[0]

def x_show(choice):
    x_mode = x_clicked.get()
    x_label = tk.Label(firstframe, text=x_clicked.get()).grid(column=0, row=1)

x_clicked = tk.StringVar()
x_clicked.set(axes_names[0])

x_drop = tk.OptionMenu(firstframe, x_clicked, *axes_names, command=x_show)
x_drop.grid(column=0, row=1)

# przycisk do wyboru osi y
y_mode = axes_names[0]

def y_modefun(choice):
    y_mode = y_clicked.get()
    y_label = tk.Label(firstframe, text=y_clicked.get()).grid(column=1, row=1)

y_clicked = tk.StringVar()
y_clicked.set(axes_names[0])

y_drop = tk.OptionMenu(firstframe, y_clicked, *axes_names, command=y_modefun)
y_drop.grid(column=1, row=1)

# przycisk do zatwierdzenia wyborów
def _accept():
    tk.Label(secondframe, text=x_mode).grid(column=0, row=4)    # to delete
    tk.Label(secondframe, text=x_mode).grid(column=1, row=4)    # to delete

accept_button = tk.Button(master=secondframe, text="Zatwierdź", command=_accept).grid(column=0, row=0)


# przycisk do zamykania programu
def _quit():
    root.quit()  # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

quit_button = tk.Button(master=secondframe, text="Wyjdź", command=_quit, bg='#778899')
quit_button.place(x=0, y=0)
quit_button.grid(column=1, row=0)

root.mainloop()
