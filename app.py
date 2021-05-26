#import bubliotek
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import pandas as pd

root = tk.Tk()
root.title('Projekcik z Pythona')
root.geometry("950x500")
root.config(bg='#2c2f33')

#podział okna na dwie części
leftframe=tk.Frame(bg='#191970')
leftframe.pack(side='left',fill=tk.BOTH,expand=True)
rightframe=tk.Frame()
rightframe.pack(side='right',fill=tk.BOTH,expand=True)


#wczytanie danych
frame=pd.read_csv('test.csv')

#tworzenie wykresu
figure=plt.Figure(figsize=(3,3),dpi=100)
ax=figure.add_subplot(111)
ax.plot(frame['colB'])

canvas = FigureCanvasTkAgg(figure, rightframe)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, rightframe)
toolbar.update()
toolbar.place(x=0,y=0)
canvas._tkcanvas.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)

#przycisk do zamykania programu
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
button = tk.Button(master=leftframe, text="Quit", command=_quit,bg='#778899')
button.place(x=0,y=0)
button.pack()

root.mainloop()
