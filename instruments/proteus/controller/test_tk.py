# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:57:20 2020

@author: Crow108
"""

import tkinter as tk

blink_time = 600 #ms
root = tk.Tk()
root.title("Devices")
frame = tk.Frame(root)
frame.pack()

label_00 = tk.Label(
    frame,
    text="●",
    fg="gray",
    bg="white",
    width=2,
    height=2
)
label_01 = tk.Label(
    frame,
    text="Proteus P1284M 1",
    fg="black",
    bg="white",
    anchor='w',
    width=14,
    height=2
)
label_00.pack(side=tk.LEFT)
label_01.pack(side=tk.RIGHT)
frame2 = tk.Frame(root)
frame2.pack()
label_10 = tk.Label(
    frame2,
    text="●",
    fg="green",
    bg="white",
    width=2,
    height=2
)
label_11 = tk.Label(
    frame2,
    text="Proteus P1284M 2",
    fg="black",
    bg="white",
    anchor='w',
    width=14,
    height=2
)
label_10.pack(side=tk.LEFT)
label_11.pack(side=tk.RIGHT)


def change_color():
    label_00.config(fg='green')
    root.after(int(blink_time / 2), change_color2)


def change_color2():
    label_00.config(fg='gray')
    root.after(int(blink_time / 2), change_color)


change_color()
root.mainloop()