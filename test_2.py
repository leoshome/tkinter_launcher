import tkinter as tk
from tkinter import ttk
import os

class FileBrowser(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.path = tk.StringVar()
        self.path.set(os.getcwd())  # 初始路徑為當前工作目錄
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # 路徑輸入框
        self.path_entry = ttk.Entry(self, textvariable=self.path)
        self.path_entry.pack(fill=tk.X)

        # Treeview 顯示檔案列表
        self.tree = ttk.Treeview(self, columns=('type', 'size'), show='headings')
        self.tree.heading('type', text='Type')
        self.tree.heading('size', text='Size')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 滾動條
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 綁定 Treeview 點擊事件
        self.tree.bind('<Double-1>', self.on_double_click)

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())  # 清空 Treeview

        try:
            files = os.listdir(self.path.get())
            for file in files:
                full_path = os.path.join(self.path.get(), file)
                file_type = 'Directory' if os.path.isdir(full_path) else 'File'
                file_size = os.path.getsize(full_path) if os.path.isfile(full_path) else ''
                self.tree.insert('', tk.END, values=(file_type, file_size), text=file)
        except FileNotFoundError:
            pass  # 處理路徑錯誤

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        file = self.tree.item(item, 'text')
        full_path = os.path.join(self.path.get(), file)

        if os.path.isdir(full_path):
            self.path.set(full_path)
            self.update_treeview()
        else:
            # 在這裡處理檔案開啟邏輯
            print(f'Opening file: {full_path}')

if __name__ == '__main__':
    root = tk.Tk()
    app = FileBrowser(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()