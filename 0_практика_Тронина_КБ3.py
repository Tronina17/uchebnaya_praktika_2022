# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 23:20:06 2022

@author: User
"""

import tkinter as tk
import random
from tkinter import messagebox as mb

"""ВЫБОР ОСНОВНОГО СЛОВА"""
def vibor_slovo():
    lines = open('slovo.txt').read().splitlines()
    myline = random.choice(lines)
    return myline   
 
slovo=vibor_slovo()
nazvan=slovo+'.txt'
l_slovo=list(slovo)

strok=0 #пометка для счета строк введенных слов
c_strok=0 #пометка для подсчета строк введенных слов компьютером
rasmer=100 #размер поля, для введенных слов

"""КОЛИЧЕСТВО ВОЗМОЖНЫХ СЛОВ ДЛЯ СОСТАВЛЕНИЯ"""
def count_lines(filename):
    with open(filename) as file:
        count = sum(1 for line in file if line.rstrip('\n'))
    return count

eraser=0 #пометка для удаления всего набронного слова
inscription=0 #пометка, что мы записали новое слово


"""СОЗДАНИЕ КЛАССА КНОПОК"""
class Letters(object):
    def __init__(self, fr, x):
        #States: 0=неиспользованный, 1=использованный
        self.state = 0
        self.core = tk.Button(fr, height=2, width=4,
            bg="#ffc0cb", activebackground="#d996a1", text=l_slovo[x],
            command=lambda:[self.cycle(), self.out_text(l_slovo[x])])
        self.core.grid(row=1, column=x)     
        
        self.record = tk.Button(fr, text='Записать', bg='#3CB371', command=self.com_zap)
        self.record.grid(row=0,column=len(l_slovo))
        
        self.ochistka=tk.Button(fr, text='Очистить', command=self.och)
        self.ochistka.grid(row=1,column=len(l_slovo)) 
        
    """меняет состояние"""
    def cycle(self):
        global eraser,  inscription
        if (self.state == 1 and eraser==1 and inscription==0 and self.core['text'] not in new_w['text']) or (self.state == 1 and eraser==0 and inscription==1 and self.core['text'] not in new_w['text']): 
            self.state=0
            
    """запись букв"""
    def out_text(self, z):
        n_slovo=new_w['text']
        if (self.state == 0 and eraser==0 and  inscription==0) or (self.state == 0 and eraser==1 and inscription==0) or (self.state == 0 and eraser==0 and inscription==1):
            new_w.config(text=n_slovo+z)
            self.state=1
        elif (eraser==0 and self.state==1) or (eraser==1 and inscription==0 and self.state==1 and self.core['text'] in new_w['text']) or (eraser==0 and inscription==1 and self.state==1 and self.core['text'] in new_w['text']): 
            new_w.config(text=n_slovo) 
            self.core.config(text=z)
            n_slovo=n_slovo.replace(z, '', 1) 
            new_w.config(text=n_slovo)
            self.state=0
    
    """запись новых слов + подсчет баллов"""
    def com_zap(self):
        global eraser, inscription, nazvan, strok, c_strok
        new_text=new_w['text']
        all_text=label1['text']
        prob=all_text.count(' ')
        summa=len(all_text)-prob
        all_words=open(nazvan).read()
        inscription=0
        lines = open(nazvan).read().splitlines()
        
        """случай, когда слово уже было введено раньше"""
        if ((' ' + new_text + ' ') in all_words) and (((' ' + new_text + ' ') in all_text) or ((' ' + new_text + ' ') in label2['text'])):
            old=mb.showinfo('Слово уже существует', 'Данное слово уже было введено')
            
        elif ((' ' + new_text + ' ') in all_words) and ((' ' + new_text + ' ') not in all_text) and ((' ' + new_text + ' ') not in label2['text']):
            if len(label1['text'].split('\n')[strok] + ' ' + new_text)>rasmer: 
                all_text=all_text + '\n  ' + new_text + ' '
                strok+=1
            else: all_text=all_text+ ' ' + new_text + ' '
            label1.config(text=all_text)
            len_sl=len(new_text)
            summa+=len_sl
            label3.configure(text='Игрок:\n' + str(summa) + ' б.')
            print(new_text)
            new_w.config(text='')
            eraser=0
            inscription=1
        
        """ход копьютера + подсчет его баллов"""
        if eraser==0 and inscription==1:
            c_all_text=label2['text']
            c_prob=c_all_text.count(' ')
            c_summa=len(c_all_text)-c_prob
            while True:
                c_slovo = random.choice(lines).replace(" ", "")
                if ((' ' + c_slovo) not in label1['text']) and ((' ' + c_slovo) not in label2['text']):
                    if len(label2['text'].split('\n')[c_strok] +c_slovo)>rasmer:
                        novoe=label2['text']+'\n'+ c_slovo+' '
                        c_strok+=1
                    else: novoe=label2['text']+c_slovo+' '
                    label2.config(text=novoe)
                    c_len_sl=len(c_slovo)
                    c_summa=c_summa+c_len_sl
                    label4.configure(text='Компьютер:\n' + str(c_summa) + ' б.')
                    break

        """конец игры, если были введены все возможные слова"""
        if len(label1['text'].split() + label2['text'].split()) == count_lines(nazvan):
            end = mb.showinfo('Конец игры', 'Были введены все возможные слова')

    """очистка всего набранного слова"""        
    def och(self):
        global eraser, inscription
        new_w.config(text='')
        eraser=1
        inscription=0
        
        
"""ОСНОВНОЕ ОКНО"""            
window = tk.Tk()
window.title("Слова из слова") 
n=len(l_slovo)

"""МЕСТО ДЛЯ НОВЫХ СЛОВ И КОЛИЧЕСТВА БАЛЛОВ"""
d=tk.Canvas(window, width=300, height=250)
d.grid(row=0,column=0)

"""МЕСТО ДЛЯ КНОПОК"""
frame=tk.Frame(bg='#DCDCDC')
frame.grid(row=1,column=0)

"""МЕСТО ДЛЯ ВВОДА НОВЫХ СЛОВ"""
new_w=tk.Label(d, text='')
new_w.grid(row=2,column=0)

"""ВСЕ ВВЕДЕННЫЕ СЛОВА ИГРОКА"""
label1=tk.Label(d, width=rasmer, height=10, text=' ', fg='#8b00ff')
label1.grid(row=0,column=0)

"""ВВЕДЕННЫЕ СЛОВА КОМПЬЮТЕРА"""
label2=tk.Label(d, text=' ', height=10, fg='#000080')
label2.grid(row=1, column=0)

"""КОЛИЧЕСТВО БАЛЛОВ ИГРОКА"""
label3=tk.Label(d, width=10, height=5, text= 'Игрок:\n 0 б.', fg='#8b00ff')
label3.grid(row=0,column=1)

"""КОЛЛИЧЕСТВО БАЛЛОВ КОМПЬЮТЕРА"""
label4=tk.Label(d, width=10, height=5, text= 'Компьютер:\n 0 б.', fg='#000080')
label4.grid(row=1,column=1)

"""ФОРМИРОВАНИЕ КНОПОК ИЗ БУКВ ОСНОВНОГО СЛОВА"""
board = [] 
for y in range(n):
    row = [Letters(frame, x) for x in range(n)]
    board.append(row)

"""функция для показа набранных баллов после завершения игры"""
def clicked():  
    summa=[int(summa) for summa in str.split(label3['text']) if summa.isdigit()]
    c_summa=[int(c_summa) for c_summa in str.split(label4['text']) if c_summa.isdigit()]
    if summa[0]>c_summa[0]: mb.showinfo('Поздравляем', 'Вы выиграли, набрав '+ label3['text'].replace('Игрок:', '')) 
    elif summa[0]==c_summa[0]: mb.showinfo('Ничья', 'Попробуйте выиграть в следующий раз')
    else: mb.showinfo('Компьютер набрал больше', 'К сожалению, Вы проиграли, набрав '+ label3['text'].replace('Игрок:', ''))

"""функция для закрытия основного окна после завершения игры"""
def close_window():
    window.destroy()

"""КНОПКА ДЛЯ ЗАВЕРШЕНИЯ ИГРЫ"""
btn = tk.Button(frame, text='Закончить игру', width=13, bg='red', command=lambda:[clicked(), close_window()])   
btn.grid(row=3, column=len(l_slovo)) 

window.mainloop()