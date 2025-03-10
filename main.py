import tkinter as tk
from tkinter import ttk
import os
import sys

class FileSystemTreeView:
    def __init__(self, root):
        self.root = root
        self.root.title("電腦文件結構")
        self.selected_files = []
        #self.root.geometry("600x600")
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("", 16))
        style.configure("TLabel", font=("", 16))
        style.configure("TFrame", font=("", 16))
        style.configure("Treeview", font=("", 16))

        # Main frame
        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Left frame for Treeview and scrollbar
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Right frame for button and listbox
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        # Treeview frame
        self.tree_frame = ttk.Frame(self.left_frame)
        self.tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        
        # 設置捲動條控制 Treeview
        self.scrollbar.config(command=self.tree.yview)
        
        # 設置 Treeview 欄位
        self.tree["columns"] = ("大小", "修改日期")
        self.tree.column("#0", width=200, minwidth=50)
        self.tree.column("大小", width=50, minwidth=50)
        self.tree.column("修改日期", width=150, minwidth=100)
        
        # 設置 Treeview 標題
        self.tree.heading("#0", text="名稱", anchor=tk.W)
        self.tree.heading("大小", text="大小", anchor=tk.W)
        self.tree.heading("修改日期", text="修改日期", anchor=tk.W)
        
        # 在 Treeview 中填充電腦文件結構
        self.populate_tree()

        # Add button to right frame
        self.add_button = ttk.Button(self.right_frame, text="加入指令檔案列表>>", command=self.add_selected_file)
        self.add_button.grid(row=0, column=0, pady=10)

        # Add label for first listbox
        self.file_listbox_label = ttk.Label(self.right_frame, text="指令檔案列表：")
        self.file_listbox_label.grid(row=1, column=0, sticky=tk.W, padx=5)

        # Add listbox to right frame
        self.file_listbox_frame = ttk.Frame(self.right_frame)
        self.file_listbox_frame.grid(row=2, column=0, pady=5, sticky=tk.NSEW)

        self.file_listbox_yscrollbar = ttk.Scrollbar(self.file_listbox_frame)
        self.file_listbox_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox_xscrollbar = ttk.Scrollbar(self.file_listbox_frame, orient=tk.HORIZONTAL)
        self.file_listbox_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.file_listbox = tk.Listbox(self.file_listbox_frame, width=30, height=12,
                                        yscrollcommand=self.file_listbox_yscrollbar.set,
                                        xscrollcommand=self.file_listbox_xscrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_listbox_yscrollbar.config(command=self.file_listbox.yview)
        self.file_listbox_xscrollbar.config(command=self.file_listbox.xview)

        # Add "貼指令" button
        self.paste_button = ttk.Button(self.right_frame, text="貼指令", command=self.move_files)
        self.paste_button.grid(row=3, column=0, pady=10)

        # Add label for second listbox
        self.command_listbox_label = ttk.Label(self.right_frame, text="已執行的指令檔案：")
        self.command_listbox_label.grid(row=4, column=0, sticky=tk.W, padx=5)

        # Add new file_listbox
        self.command_listbox_frame = ttk.Frame(self.right_frame)
        self.command_listbox_frame.grid(row=5, column=0, pady=5, sticky=tk.NSEW)

        self.command_listbox_yscrollbar = ttk.Scrollbar(self.command_listbox_frame)
        self.command_listbox_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.command_listbox_xscrollbar = ttk.Scrollbar(self.command_listbox_frame, orient=tk.HORIZONTAL)
        self.command_listbox_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.command_listbox = tk.Listbox(self.command_listbox_frame, width=30, height=12,
                                           yscrollcommand=self.command_listbox_yscrollbar.set,
                                           xscrollcommand=self.command_listbox_xscrollbar.set)
        self.command_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.command_listbox_yscrollbar.config(command=self.command_listbox.yview)
        self.command_listbox_xscrollbar.config(command=self.command_listbox.xview)

        # 綁定雙擊事件來展開/收縮節點
        self.tree.bind("<Double-1>", self.on_double_click)

    def populate_tree(self):
        # 獲取根目錄
        if sys.platform == "win32":
            # Windows
            drives = self.get_windows_drives()
            # 添加每個驅動器
            for drive in drives:
                drive_node = self.tree.insert("", "end", text=drive, open=False)
                self.populate_root_folder(drive_node, f"{drive}\\")
        else:
            # Unix/Linux/Mac
            root_node = self.tree.insert("", "end", text="/", open=False)
            self.populate_root_folder(root_node, "/")
    
    def get_windows_drives(self):
        # 獲取 Windows 上的所有驅動器
        import string
        from ctypes import windll
        
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:")
            bitmask >>= 1
            
        return drives
    def populate_root_folder(self, parent, path):
        try:
            # 只嘗試列出根目錄的第一級項目
            items = os.listdir(path)
            for item in items[:20]:  # 限制項目數以避免加載過多
                item_path = os.path.join(path, item)
                try:
                    is_directory = os.path.isdir(item_path)

                    # 獲取文件大小和修改日期
                    size = ""
                    date = ""
                    try:
                        stats = os.stat(item_path)
                        if not is_directory:
                            size = self.format_size(stats.st_size)
                        date = self.format_date(stats.st_mtime)
                    except:
                        pass

                    # 插入項目到 Treeview
                    item_node = self.tree.insert(parent, "end", text=item, values=(size, date))

                    # 如果是目錄，添加一個臨時子節點，使其可展開
                    if is_directory:
                        self.tree.insert(item_node, "end", text="Loading...", values=("", ""))
                except:
                    # 忽略無法訪問的項目
                    pass
        except:
            # 忽略無法訪問的目錄
            pass
    
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        
        # 檢查該項目是否已被展開
        if self.tree.item(item, "open"):
            # 如果已展開，則收縮
            self.tree.item(item, open=False)
        else:
            # 如果未展開，則展開並加載子項目
            self.tree.item(item, open=True)
    
    def get_full_path(self, item):
        # 獲取項目的完整路徑
        path_parts = []
        while item:
            path_parts.insert(0, self.tree.item(item, "text"))
            item = self.tree.parent(item)
        
        if sys.platform == "win32":
            # Windows 路徑
            return "\\".join(path_parts)
        else:
            # Unix/Linux/Mac 路徑
            return "/" + "/".join(path_parts[1:])  # 跳過第一個元素（根節點）

    def add_selected_file(self):
       for item in self.tree.selection():
           file_path = self.get_full_path(item)
           if os.path.isfile(file_path):
               if file_path not in self.selected_files:
                   self.selected_files.append(file_path)
                   self.file_listbox.insert(tk.END, file_path)
    
    def format_size(self, size_bytes):
        # 格式化文件大小
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"
    def format_date(self, timestamp):
        # 格式化日期
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def move_files(self):
        # Get all items in the file_listbox
        all_items = self.file_listbox.get(0, tk.END)
        # Insert all items into the command_listbox
        for item in all_items:
            self.command_listbox.insert(tk.END, item)
        # Delete all items from the original listbox
        self.file_listbox.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemTreeView(root)
    root.mainloop()