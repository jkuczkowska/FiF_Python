#import bubliotek
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

#podział okna na dwie części
leftframe=tk.Frame(bg='#191970')
leftframe.pack(side='left',fill=tk.BOTH,expand=True)
rightframe=tk.Frame()
rightframe.pack(side='right',fill=tk.BOTH,expand=True)

# podział lewego okna na dwie części
firstframe = tk.Frame(leftframe, bg='#191970')
firstframe.pack(side='top', fill=tk.BOTH, expand=True)
secondframe = tk.Frame(leftframe, bg="#4949AD")
secondframe.pack(side='bottom', fill=tk.BOTH, expand=True)


## wczytanie danych
frame=pd.read_csv('.\Dane\Pogoda1.csv',usecols=['Data','Temperatura powietrza',
                                                'Zachmurzenie ogólne [oktanty]','Prędkość wiatru  [m/s]',
                                                'Wilgotność względna [%]','Ciśnienie na pozimie stacji [hPa]',
                                                'Ciśnienie na pozimie morza [hPa]','Opad za 6 godzin [mm]'])
frame['Data']=pd.to_datetime(frame['Data'])

frame_s=pd.read_csv('.\Dane\Sunspot.csv')
frame_s['Data']=pd.to_datetime(frame_s['Data'])

#frame_a=pd.read_csv('.\Dane\air-quality_kraków_ul_złoty_róg.csv')
#-----------------------------------------------------------------------------------------------------

figure=plt.Figure(figsize=(3,3),dpi=100)
ax=figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, rightframe)

## tworzenie wykresu
def make_fig():
    global figure
    global ax
    global canvas
    figure.clear()
   # canvas.delete()
    figure=plt.Figure(figsize=(3,3),dpi=100)
    ax=figure.add_subplot(111)
    if x_file.get()=='Pogoda': x=frame[x_clicked.get()]
    elif x_file.get()=='Aktywność słoneczna': x=frame_s[x_clicked.get()]
    else: x=frame_a[x_clicked.get()]

    if y_file.get()=='Pogoda': y=frame[y_clicked.get()]
    elif y_file.get()=='Aktywność słoneczna': y=frame_s[y_clicked.get()]
    else: y=frame_a[y_clicked.get()]
    #znalezienie zakresu odpowiadającego podanym datom
    id_s = list(frame.Data).index(pd.to_datetime(date_s.get()))
    id_f = list(frame.Data).index(pd.to_datetime(date_f.get()))
    ax.plot(x[id_s:id_f],y[id_s:id_f],'r.',lw=1)

    canvas = FigureCanvasTkAgg(figure, rightframe)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, rightframe)
    toolbar.update()
    toolbar.place(x=0,y=0)
    canvas._tkcanvas.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)
#-----------------------------------------------------------------
    
axes_names_x=frame.columns
axes_names_y=frame.columns
def set_x(x):
    global axes_names_x
    if x=='Pogoda': axes_names_x = frame.columns
    elif x=='Aktywność słoneczna':axes_names_x = frame_s.columns
   # else: axes_names_x = frame_a.columns
    x_drop = tk.OptionMenu(firstframe, x_clicked, *axes_names_x)#, command=x_show)
    x_drop.grid(column=0, row=1,columnspan=3)


def set_y(y):
    global axes_names_y
    if y=='Pogoda': axes_names_y = frame.columns
    elif y=='Aktywność słoneczna':axes_names_y = frame_s.columns
   # else: axes_names_y = frame_a.columns
    y_drop = tk.OptionMenu(firstframe, y_clicked, *axes_names_y)#, command=y_modefun)
    y_drop.grid(column=3, row=1,columnspan=3)
    
#wybór pliku na X
global x_file
file_option=['Pogoda','Aktywność słoneczna','Zanieczyszczenie powietrza']
x_file=tk.StringVar()
x_file.set('Pogoda')
x_file_label=tk.OptionMenu(firstframe,x_file,*file_option,
                           command=set_x)
x_file_label.grid(column=0,row=0,columnspan=3)
#wybór pliku na Y
global y_file
y_file=tk.StringVar()
y_file.set('Pogoda')
y_file_label=tk.OptionMenu(firstframe,y_file,*file_option,
                           command=set_y)
y_file_label.grid(column=3,row=0,columnspan=3)


# przyciski do wyboru osi x i y

x_clicked = tk.StringVar()
x_clicked.set(axes_names_x[0])

y_clicked = tk.StringVar()
y_clicked.set(axes_names_y[0])

# wybór dat
date_label = tk.Label(master=firstframe, bg='#4949AD', padx=10,pady=10,
                      text='Wybierz zakres dat w formacie rrrr-mm-dd\nMożliwy zakres od {} do {}'.format(
                          str(frame.Data.min()).split()[0],
                          str(frame.Data.max()).split()[0])).grid(
                          column=0,row=2,columnspan=6)
date_s_label = tk.Label(master=firstframe,bg='#4949AD', padx=10,pady=10,
                        text='Data początkowa').grid(column=0,row=3,columnspan=3)
date_f_label = tk.Label(master=firstframe,bg='#4949AD', padx=10,pady=10,
                        text='Data końcowa').grid(column=3,row=3,columnspan=3)
global date_s
global date_f
date_s=tk.StringVar()
date_s.set('2000-01-01')
date_f=tk.StringVar()
date_f.set('2020-12-31')
date_s_e = tk.Entry(master=firstframe,textvariable=date_s).grid(column=0,row=4,columnspan=3)
date_f_e = tk.Entry(master=firstframe,textvariable=date_f).grid(column=3,row=4,columnspan=3)

# przycisk do zatwierdzenia wyborów
def _accept():
    tk.Label(secondframe, text=x_mode).grid(column=0, row=4)    # to delete
    tk.Label(secondframe, text=x_mode).grid(column=1, row=4)    # to delete

accept_button = tk.Button(master=firstframe, text="Zatwierdź", command=make_fig,
                          padx=10,pady=10).grid(column=0, row=10)

#przycisk do zamykania programu------------------------------------------------------------------------
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    
button = tk.Button(master=secondframe, text="Quit", command=_quit,bg='#778899',padx=10,pady=10)
button.grid(column=0,row=10)

root.mainloop()
