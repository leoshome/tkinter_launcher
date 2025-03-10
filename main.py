# generated by claude 3.7 sonnet
import tkinter as tk
from tkinter import ttk
import os
import sys

class FileSystemTreeView:
    def __init__(self, root):
        self.root = root
        self.root.title("電腦文件結構")
        self.root.geometry("800x600")
        
        # 創建框架來存放 Treeview 和捲動條
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 創建垂直捲動條
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 設置 Treeview
        self.tree = ttk.Treeview(self.frame, yscrollcommand=self.scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 設置捲動條控制 Treeview
        self.scrollbar.config(command=self.tree.yview)
        
        # 設置 Treeview 欄位
        self.tree["columns"] = ("大小", "修改日期")
        self.tree.column("#0", width=300, minwidth=250)
        self.tree.column("大小", width=100, minwidth=80)
        self.tree.column("修改日期", width=150, minwidth=120)
        
        # 設置 Treeview 標題
        self.tree.heading("#0", text="名稱", anchor=tk.W)
        self.tree.heading("大小", text="大小", anchor=tk.W)
        self.tree.heading("修改日期", text="修改日期", anchor=tk.W)
        
        # 在 Treeview 中填充電腦文件結構
        self.populate_tree()
        
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
                        # self.tree.insert(item_node, "end", text="Loading...", values=("", ""))
                        self.populate_root_folder(item_node, item_path)
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
    
    # def load_children(self, parent, path):
    #     try:
    #         items = os.listdir(path)
    #         for item in items[:50]:  # 限制項目數以避免加載過多
    #             item_path = os.path.join(path, item)
    #             try:
    #                 is_directory = os.path.isdir(item_path)
                    
    #                 # 獲取文件大小和修改日期
    #                 size = ""
    #                 date = ""
    #                 try:
    #                     stats = os.stat(item_path)
    #                     if not is_directory:
    #                         size = self.format_size(stats.st_size)
    #                     date = self.format_date(stats.st_mtime)
    #                 except:
    #                     pass
                    
    #                 # 插入項目到 Treeview
    #                 item_node = self.tree.insert(parent, "end", text=item, values=(size, date))
                    
    #                 # 如果是目錄，添加一個臨時子節點，使其可展開
    #                 if is_directory:
    #                     self.tree.insert(item_node, "end", text="Loading...", values=("", ""))
    #             except:
    #                 # 忽略無法訪問的項目
    #                 pass
    #     except:
    #         # 忽略無法訪問的目錄
    #         pass
    
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

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemTreeView(root)
    root.mainloop()
