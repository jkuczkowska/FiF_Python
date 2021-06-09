#import bibliotek
from tkinter import *
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
rightframe=tk.Frame(root,bg="#A9A9FD",relief=SUNKEN,bd=2)
rightframe.pack(side='right',fill=tk.BOTH,expand=True)

# podział lewego okna na dwie części
firstframe = tk.Frame(leftframe, bg='#191970',relief=SOLID,bd=2)
firstframe.pack(side='top', fill=tk.BOTH, expand=True)
secondframe = tk.Frame(leftframe, bg="#4949AD",relief=SOLID,bd=2)
secondframe.pack(side='bottom', fill=tk.BOTH, expand=True)


## wczytanie danych
frame=pd.read_csv('.\Dane\Pogoda1.csv')#,usecols=['Data','Temperatura powietrza',
                                        #        'Zachmurzenie ogólne [oktanty]','Prędkość wiatru  [m/s]',
                                         #       'Wilgotność względna [%]','Ciśnienie na pozimie stacji [hPa]',
                                          #      'Ciśnienie na pozimie morza [hPa]','Opad za 6 godzin [mm]'])
frame['Data']=pd.to_datetime(frame['Data'])
del frame['Unnamed: 0']

frame_s=pd.read_csv('.\Dane\Sunspot.csv')
frame_s['Data']=pd.to_datetime(frame_s['Data'])
del frame_s['Unnamed: 0']

#frame_a=pd.read_csv('.\Dane\AirQ.csv')
#frame_a['Data']=pd.to_datetime(frame_a['Data'])
#-----------------------------------------------------------------------------------------------------

figure=plt.Figure(figsize=(3,3),dpi=100)
ax=figure.add_subplot(111)
#canvas = FigureCanvasTkAgg(figure, rightframe)

## tworzenie wykresu
def make_fig():
    global figure
    global ax
    #global canvas
    figure.clf()
    ax.cla()
    figure=plt.Figure(figsize=(3,3),dpi=100)
    ax=figure.add_subplot(111)
    #zczytanie danych X i Y
    if x_file.get()=='Pogoda': x=frame[x_clicked.get()]
    elif x_file.get()=='Aktywność słoneczna': x=frame_s[x_clicked.get()]
    #else: x=frame_a[x_clicked.get()]

    if y_file.get()=='Pogoda': y=frame[y_clicked.get()]
    elif y_file.get()=='Aktywność słoneczna': y=frame_s[y_clicked.get()]
    #else: y=frame_a[y_clicked.get()]
    
    #znalezienie zakresu odpowiadającego podanym datom
    id_s = list(frame.Data).index(pd.to_datetime(date_s.get()))
    id_f = list(frame.Data).index(pd.to_datetime(date_f.get()))
    x=x[id_s:id_f]
    y=y[id_s:id_f]
    ax.plot(x,y,'r.',lw=1)

    #opis osi
    ax_x=x_clicked.get()
    ax_y=y_clicked.get()
    ax.set_xlabel(ax_x)
    ax.set_ylabel(ax_y)
    
    canvas = FigureCanvasTkAgg(figure, rightframe)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, rightframe)
    toolbar.update()
    toolbar.place(x=0,y=0)
    canvas._tkcanvas.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)
    #aktualizacja statów
    update_stat(x,y)

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
def update_stat(x,y):
    global max_label
    global min_label
    global mean_label
    global med_label
    global std_label
    global corr_label
    
    if x_clicked.get()=='Data' and y_clicked.get()=='Data':
        max_label = tk.Label(secondframe,text='Wartość maksymalna: -',bg='#CAC').grid(column=0,row=1,sticky="W")
        min_label = tk.Label(secondframe,text='Wartość minimalna: -',bg='#CAC').grid(column=0,row=2,sticky="W")
        mean_label = tk.Label(secondframe,text='Wartość średnia: -',bg='#CAC').grid(column=0,row=3,sticky="W")
        med_label = tk.Label(secondframe,text='Mediana: -',bg='#CAC').grid(column=0,row=4,sticky="W")
        std_label = tk.Label(secondframe,text='Rozrzut (std): -',bg='#CAC').grid(column=0,row=5,sticky="W")
    elif x_clicked.get()=='Data':
        max_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość maksymalna: {:.3f} dla {}'.format(max(y),str(list(x)[list(y).index(max(y))]).split()[0])).grid(
                                 column=0,row=1,sticky="W") 
        min_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość minimalna: {:.3f} dla {}'.format(min(y),str(list(x)[list(y).index(min(y))]).split()[0])).grid(
                                 column=0,row=2,sticky="W")
        mean_label = tk.Label(secondframe,bg='#CAC',text='Wartość średnia: {:.3f}'.format(y.mean(),)).grid(column=0,row=3,sticky="W")
        med_label = tk.Label(secondframe,bg='#CAC',text='Mediana: {:.3f}'.format(y.median())).grid(column=0,row=4,sticky="W")
        std_label = tk.Label(secondframe,bg='#CAC',text='Rozrzut (std): {:.3f}'.format(y.std())).grid(column=0,row=5,sticky="W")
    elif y_clicked.get()=='Data':
        max_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość maksymalna: {:.3f} dla {}'.format(max(x),str(list(y)[list(x).index(max(x))]).split()[0])).grid(
                                 column=0,row=1,sticky="W") 
        min_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość minimalna: {:.3f} dla {}'.format(min(x),str(list(y)[list(x).index(min(x))]).split()[0])).grid(
                                 column=0,row=2,sticky="W")
        mean_label = tk.Label(secondframe,bg='#CAC',text='Wartość średnia: {:.3f}'.format(x.mean(),)).grid(column=0,row=3,sticky="W")
        med_label = tk.Label(secondframe,bg='#CAC',text='Mediana: {:.3f}'.format(x.median())).grid(column=0,row=4,sticky="W")
        std_label = tk.Label(secondframe,bg='#CAC',text='Rozrzut (std): {:.3f}'.format(x.std())).grid(column=0,row=5,sticky="W")
    else:
        max_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość maksymalna: {:.3f} dla {:.3f}'.format(max(y),x[y.idxmax()])).grid(
                                 column=0,row=1,sticky="W") 
        min_label = tk.Label(secondframe,bg='#CAC',
                             text='Wartość minimalna: {:.3f} dla {:.3f}'.format(min(y),x[y.idxmax()])).grid(
                                 column=0,row=2,sticky="W")
        mean_label = tk.Label(secondframe,bg='#CAC',text='Wartość średnia: {:.3f}'.format(y.mean(),)).grid(column=0,row=3,sticky="W")
        med_label = tk.Label(secondframe,bg='#CAC',text='Mediana: {:.3f}'.format(y.median())).grid(column=0,row=4,sticky="W")
        std_label = tk.Label(secondframe,bg='#CAC',text='Rozrzut (std): {:.3f}'.format(y.std())).grid(column=0,row=5,sticky="W")
    try:
        corr_label = tk.Label(secondframe,bg='#CAC',text='Korelacja: {:.3f}'.format(y.corr(x))).grid(column=0,row=6,sticky="W")
    except TypeError:
        corr_label = tk.Label(secondframe,bg='#CAC',text='Korelacja: -').grid(column=0,row=6,sticky="W")
#-----------------------------------------------------------------
#-----------------------------------------------------------------
    
axes_names_x=frame.columns
axes_names_y=frame.columns
def set_x(x):
    global axes_names_x
    if x=='Pogoda': axes_names_x = frame.columns
    elif x=='Aktywność słoneczna':axes_names_x = frame_s.columns
    #else: axes_names_x = frame_a.columns
    x_drop = tk.OptionMenu(firstframe, x_clicked, *axes_names_x)#, command=x_show)
    x_drop.grid(column=0, row=1,columnspan=3,sticky="W")


def set_y(y):
    global axes_names_y
    if y=='Pogoda': axes_names_y = frame.columns
    elif y=='Aktywność słoneczna':axes_names_y = frame_s.columns
   # else: axes_names_y = frame_a.columns
    y_drop = tk.OptionMenu(firstframe, y_clicked, *axes_names_y)#, command=y_modefun)
    y_drop.grid(column=3, row=1,columnspan=3,sticky="W")
    
#wybór pliku na X
global x_file
file_option=['Pogoda','Aktywność słoneczna']#,'Zanieczyszczenie powietrza']
x_file=tk.StringVar()
x_file.set('Pogoda')
x_file_label=tk.OptionMenu(firstframe,x_file,*file_option,
                           command=set_x)
x_file_label.grid(column=0,row=0,columnspan=3,sticky="W")
#wybór pliku na Y
global y_file
y_file=tk.StringVar()
y_file.set('Pogoda')
y_file_label=tk.OptionMenu(firstframe,y_file,*file_option,
                           command=set_y)
y_file_label.grid(column=3,row=0,columnspan=3,sticky="W")


# przyciski do wyboru osi x i y

x_clicked = tk.StringVar()
x_clicked.set(axes_names_x[0])

y_clicked = tk.StringVar()
y_clicked.set(axes_names_y[1])

# wybór dat
date_label = tk.Label(master=firstframe, bg='#4949AD', padx=10,pady=10,
                      text='Wybierz zakres dat w formacie rrrr-mm-dd\nMożliwy zakres od {} do {}'.format(
                          str(frame.Data.min()).split()[0],
                          str(frame.Data.max()).split()[0])).grid(
                          column=0,row=2,columnspan=6,sticky="W")
date_s_label = tk.Label(master=firstframe,bg='#4949AD', padx=10,pady=10,
                        text='Data początkowa').grid(column=0,row=3,columnspan=3,sticky="W")
date_f_label = tk.Label(master=firstframe,bg='#4949AD', padx=10,pady=10,
                        text='Data końcowa').grid(column=3,row=3,columnspan=3,sticky="W")
global date_s
global date_f
date_s=tk.StringVar()
date_s.set('2010-01-01')
date_f=tk.StringVar()
date_f.set('2021-04-30')
date_s_e = tk.Entry(master=firstframe,textvariable=date_s).grid(column=0,row=4,columnspan=3,sticky="W")
date_f_e = tk.Entry(master=firstframe,textvariable=date_f).grid(column=3,row=4,columnspan=3,sticky="W")

# przycisk do zatwierdzenia wyborów
def _accept():
    tk.Label(secondframe, text=x_mode).grid(column=0, row=4)    
    tk.Label(secondframe, text=x_mode).grid(column=1, row=4)    

accept_button = tk.Button(master=firstframe, text="Zatwierdź", command=make_fig,
                          padx=10,pady=10,bg='#CAC').grid(column=0, row=10,sticky="W")
# jakaś statystyka ----------------------------------------------------------------

max_label =  tk.Label(secondframe,width=45,anchor='w',text='Wartość maksymalna:',bg='#CAC').grid(column=0,row=1,sticky="W")
min_label =  tk.Label(secondframe,width=45,anchor='w',text='Wartość minimalna:',bg='#CAC').grid(column=0,row=2,sticky="W")
mean_label = tk.Label(secondframe,width=45,anchor='w',text='Wartość średnia:',bg='#CAC').grid(column=0,row=3,sticky="W")
med_label =  tk.Label(secondframe,width=45,anchor='w',text='Mediana:',bg='#CAC').grid(column=0,row=4,sticky="W")
std_label =  tk.Label(secondframe,width=45,anchor='w',text='Rozrzut (std):',bg='#CAC').grid(column=0,row=5,sticky="W")
corr_label = tk.Label(secondframe,width=45,anchor='w',text='Korelacja:',bg='#CAC').grid(column=0,row=6,sticky="W")

#przycisk do zamykania programu------------------------------------------------------------------------
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    
button = tk.Button(master=secondframe, text="Quit",anchor='w', command=_quit,bg='#FF2266',padx=10,pady=10)
button.grid(column=0,row=10,columnspan=4,sticky="W")

root.mainloop()
