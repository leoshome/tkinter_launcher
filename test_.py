import tkinter as tk
from tkinter import ttk

def on_treeview_select(event):
    print("Treeview item selected")

def on_button_press(event):
    print("Button press")

def on_button_motion(event):
    print("Button motion")

def on_button_release(event):
    print("Button release")

root = tk.Tk()

tree = ttk.Treeview(root)
tree.pack()

tree.bind("<<TreeviewSelect>>", on_treeview_select)
tree.bind("<ButtonPress-1>", on_button_press)
tree.bind("<B1-Motion>", on_button_motion)
tree.bind("<ButtonRelease-1>", on_button_release)

# 插入一些項目
tree.insert("", "end", text="Item 1")
tree.insert("", "end", text="Item 2")
tree.insert("", "end", text="Item 3")

root.mainloop()