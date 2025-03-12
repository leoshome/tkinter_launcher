import tkinter as tk
from tkinter import ttk
import os
import sys
import datetime

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

        # 設置root的grid配置
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Main frame
        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Left frame for Treeview and scrollbar
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)

        # Right frame for button and listbox
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        # Treeview frame
        self.tree_frame = ttk.Frame(self.left_frame)
        self.tree_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Treeview
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set, selectmode="extended")
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
        
        # Add button to right frame
        self.add_button = ttk.Button(self.right_frame, text="加入到指令檔案列表>>>", command=self.add_selected_file)
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

        # 將file_listbox改為多選模式
        self.file_listbox = tk.Listbox(self.file_listbox_frame, width=30, height=12, font=("", 16),
                                      yscrollcommand=self.file_listbox_yscrollbar.set,
                                      xscrollcommand=self.file_listbox_xscrollbar.set,
                                      selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_listbox_yscrollbar.config(command=self.file_listbox.yview)
        self.file_listbox_xscrollbar.config(command=self.file_listbox.xview)

        # 添加刪除按鈕
        self.delete_button = ttk.Button(self.right_frame, text="刪除選定的檔案", command=self.delete_selected_items)
        self.delete_button.grid(row=3, column=0, pady=5)

        # Add "貼指令" button
        self.paste_button = ttk.Button(self.right_frame, text="貼指令", command=self.move_files)
        self.paste_button.grid(row=4, column=0, pady=10)

        # Add label for second listbox
        self.command_listbox_label = ttk.Label(self.right_frame, text="已執行的指令檔案：")
        self.command_listbox_label.grid(row=5, column=0, sticky=tk.W, padx=5)

        # Add new file_listbox
        self.command_listbox_frame = ttk.Frame(self.right_frame)
        self.command_listbox_frame.grid(row=6, column=0, pady=5, sticky=tk.NSEW)

        self.command_listbox_yscrollbar = ttk.Scrollbar(self.command_listbox_frame)
        self.command_listbox_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.command_listbox_xscrollbar = ttk.Scrollbar(self.command_listbox_frame, orient=tk.HORIZONTAL)
        self.command_listbox_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.command_listbox = tk.Listbox(self.command_listbox_frame, width=30, height=12, font=("", 16),
                                          yscrollcommand=self.command_listbox_yscrollbar.set,
                                          xscrollcommand=self.command_listbox_xscrollbar.set)
        self.command_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.command_listbox_yscrollbar.config(command=self.command_listbox.yview)
        self.command_listbox_xscrollbar.config(command=self.command_listbox.xview)
        
        # 在 Treeview 中填充電腦文件結構
        self.populate_tree()
        
        # 滑鼠拖拉多選相關變數
        self.is_dragging = False
        self.drag_start_item = None
        
        # 綁定事件
        self.tree.bind("<ButtonPress-1>", self.on_button_press)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_button_release)
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        
        # 綁定節點展開事件
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_open)

    def populate_tree(self):
        # 獲取根目錄
        if sys.platform == "win32":
            # Windows
            drives = self.get_windows_drives()
            # 添加每個驅動器
            for drive in drives:
                drive_node = self.tree.insert("", "end", text=drive, open=False)
                # 為每個驅動器創建一個臨時節點
                self.tree.insert(drive_node, "end", text="", values=("", ""))
        else:
            # Unix/Linux/Mac
            root_node = self.tree.insert("", "end", text="/", open=False)
            # 為根節點創建一個臨時節點
            self.tree.insert(root_node, "end", text="", values=("", ""))
    
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
    
    def populate_folder(self, parent, path):
        # 先刪除所有現有的子項目（包括臨時節點）
        for item in self.tree.get_children(parent):
            self.tree.delete(item)
            
        try:
            # 列出目錄中的所有項目
            items = os.listdir(path)
            
            # 分開處理檔案和資料夾
            folders = []
            files = []
            
            for item in items:
                item_path = os.path.join(path, item)
                try:
                    if os.path.isdir(item_path):
                        folders.append(item)
                    else:
                        files.append(item)
                except:
                    pass
            
            # 先添加資料夾
            for folder in sorted(folders):
                folder_path = os.path.join(path, folder)
                try:
                    # 獲取修改日期
                    date = ""
                    try:
                        stats = os.stat(folder_path)
                        date = self.format_date(stats.st_mtime)
                    except:
                        pass
                    
                    # 插入資料夾到 Treeview
                    folder_node = self.tree.insert(parent, "end", text=folder, values=("", date))
                    
                    # 檢查資料夾是否有內容
                    try:
                        has_content = len(os.listdir(folder_path)) > 0
                    except:
                        has_content = False
                    
                    # 如果資料夾有內容，添加一個臨時節點
                    if has_content:
                        self.tree.insert(folder_node, "end", text="", values=("", ""))
                except:
                    # 忽略無法訪問的項目
                    pass
            
            # 再添加檔案
            for file in sorted(files):
                file_path = os.path.join(path, file)
                try:
                    # 獲取文件大小和修改日期
                    size = ""
                    date = ""
                    try:
                        stats = os.stat(file_path)
                        size = self.format_size(stats.st_size)
                        date = self.format_date(stats.st_mtime)
                    except:
                        pass
                    
                    # 插入檔案到 Treeview
                    self.tree.insert(parent, "end", text=file, values=(size, date))
                except:
                    # 忽略無法訪問的項目
                    pass
        except Exception as e:
            print(f"Error populating folder {path}: {e}")  # 用於調試
            pass
    
    def on_button_press(self, event):
        # 获取点击位置的项目
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        # 检查是否点击在展开/收缩按钮上
        region = self.tree.identify_region(event.x, event.y)
        
        # 记录拖动开始的项目
        self.is_dragging = False
        self.drag_start_item = item
        
        # 处理选择和展开/收缩逻辑
        if region == "tree":  # 点击在展开/收缩图标上
            # 切换展开/收缩状态
            path = self.get_full_path(item)
            if os.path.isdir(path):
                if self.tree.item(item, "open"):
                    self.tree.item(item, open=False)
                else:
                    self.tree.item(item, open=True)
                    self.populate_folder(item, path)
        else:  # 点击在项目上（非展开/收缩图标）
            # 如果按下Ctrl键，保留当前选择，否则清除当前选择并只选择当前项目
            if not (event.state & 0x0004):  # 0x0004是Ctrl键的状态
                self.tree.selection_set(item)
    
    def on_drag_motion(self, event):
        if not self.drag_start_item:
            return
            
        # 标记为正在拖动
        self.is_dragging = True
        
        # 获取当前鼠标位置的项目
        current_item = self.tree.identify_row(event.y)
        if not current_item:
            return
            
        # 获取所有可见的项目
        visible_items = []
        
        # 获取可见项目（简化版，只获取当前显示的顶层项目及其可见子项目）
        def get_visible_children(parent):
            children = self.tree.get_children(parent)
            for child in children:
                visible_items.append(child)
                if self.tree.item(child, "open"):
                    get_visible_children(child)
        
        # 从根节点开始获取所有可见项目
        for top_item in self.tree.get_children():
            visible_items.append(top_item)
            if self.tree.item(top_item, "open"):
                get_visible_children(top_item)
        
        # 找出起始项目和当前项目的索引
        try:
            start_idx = visible_items.index(self.drag_start_item)
            current_idx = visible_items.index(current_item)
            
            # 获取范围内的所有项目
            if start_idx <= current_idx:
                selection_range = visible_items[start_idx:current_idx+1]
            else:
                selection_range = visible_items[current_idx:start_idx+1]
            
            # 设置选择
            self.tree.selection_set(selection_range)
        except ValueError:
            # 如果项目不在可见列表中（可能在已折叠的节点内）
            pass
    
    def on_button_release(self, event):
        # 释放时，只需重置拖动状态
        self.drag_start_item = None
        self.is_dragging = False
    
    def on_double_click(self, event):
        # 双击事件处理 - 这里主要用于展开/收缩文件夹
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        # 检查该项目是否是文件夹
        path = self.get_full_path(item)
        if os.path.isdir(path):
            if self.tree.item(item, "open"):
                self.tree.item(item, open=False)
            else:
                self.tree.item(item, open=True)
                self.populate_folder(item, path)
    
    def on_tree_open(self, event):
        # 获取当前打开的项目
        item = self.tree.focus()
        
        # 获取完整路径
        path = self.get_full_path(item)
        
        # 检查这是否是一个目录
        if os.path.isdir(path):
            self.populate_folder(item, path)
    
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
        # Clear the selected_files list
        self.selected_files = []
    
    # 新增的刪除選定項目的函數
    def delete_selected_items(self):
        # 獲取選中的項目索引（從後往前，避免刪除時索引變化）
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return
            
        # 將索引轉換為列表並從大到小排序
        indices_list = sorted(list(selected_indices), reverse=True)
        
        # 從後往前刪除選中的項目
        for index in indices_list:
            item = self.file_listbox.get(index)
            # 從self.selected_files中移除
            if item in self.selected_files:
                self.selected_files.remove(item)
            # 從listbox中刪除
            self.file_listbox.delete(index)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemTreeView(root)
    root.mainloop()