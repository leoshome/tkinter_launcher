import tkinter as tk
from tkinter import ttk

# 創建主窗口
root = tk.Tk()
root.title("華麗檔案總管")
root.geometry("800x600")
root.resizable(False, False)

# 創建漸變背景 (使用 Canvas)
canvas = tk.Canvas(root, width=800, height=600)
for i in range(600):
    # 確保每個顏色分量在 0-255 之間
    r = min(255, int(50 + i/3))
    g = min(255, int(100 + i/2))
    b = min(255, int(150 + i/1.5))
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 800, i, fill=color)
canvas.pack(fill="both", expand=True)

# 左側樹狀結構 (Treeview)
tree_frame = tk.Frame(root, bg="#2c3e50")
tree_frame.place(x=10, y=10, width=250, height=580)

tree_scroll = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=30)
tree_scroll.config(command=tree.yview)

tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

# 定義樹狀結構資料
tree.heading("#0", text="檔案系統", anchor=tk.W)
root_node = tree.insert("", tk.END, text="exe_lanucher_pyside", open=True)
tree.insert(root_node, tk.END, text="breeze_rag")
tree.insert(root_node, tk.END, text="cef")
tkinter_node = tree.insert(root_node, tk.END, text="tkinter", open=True)
tree.insert(tkinter_node, tk.END, text="main")
tree.insert(tkinter_node, tk.END, text="test_")

# 右側檔案清單 (Treeview)
file_frame = tk.Frame(root, bg="#2c3e50")
file_frame.place(x=270, y=10, width=520, height=580)

file_scroll = tk.Scrollbar(file_frame, orient=tk.VERTICAL)
file_tree = ttk.Treeview(file_frame, yscrollcommand=file_scroll.set, columns=("Date", "Time"), height=30)
file_scroll.config(command=file_tree.yview)

file_tree.heading("#0", text="檔案名稱")
file_tree.heading("Date", text="日期")
file_tree.heading("Time", text="時間")
file_tree.column("#0", width=200)
file_tree.column("Date", width=150)
file_tree.column("Time", width=150)

file_scroll.pack(side=tk.RIGHT, fill=tk.Y)
file_tree.pack(fill=tk.BOTH, expand=True)

# 初始填充右側檔案清單
def update_file_list(event=None):
    selected_item = tree.selection()
    file_tree.delete(*file_tree.get_children())
    if selected_item:
        if tree.item(selected_item)["text"] == "tkinter":
            file_tree.insert("", tk.END, text="main", values=("2025/3/13", "03:33"))
            file_tree.insert("", tk.END, text="test_", values=("2025/3/13", "02:14"))

# 綁定樹狀結構選擇事件
tree.bind("<<TreeviewSelect>>", update_file_list)

# 底部按鈕框架
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.place(x=10, y=560, width=780, height=30)

# 自定義華麗按鈕
def create_fancy_button(parent, text, command, x, y):
    button = tk.Button(parent, text=text, command=command, bg="#27ae60", fg="white",
                       font=("Arial", 10, "bold"), activebackground="#2ecc71", relief=tk.FLAT)
    button.place(x=x, y=y, width=80, height=25)
    # 加入 hover 效果
    def on_enter(e):
        button.config(bg="#2ecc71")
    def on_leave(e):
        button.config(bg="#27ae60")
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button

# 創建開啟和取消按鈕
open_button = create_fancy_button(button_frame, "開啟 (O)", lambda: print("開啟選項"), 10, 2)
cancel_button = create_fancy_button(button_frame, "取消", lambda: root.quit(), 100, 2)

# 啟動更新
update_file_list()

# 運行主循環
root.mainloop()