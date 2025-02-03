import time
import tkinter as tk
from Tools import *

# 创建主窗口
root = tk.Tk()
# 设置窗口标题
root.title("AUTOMATIC_CLICKER")
# 设置窗口大小
root.geometry("400x300")

def on_button_click():
    print("Button clicked!")
    root.iconify()
    time.sleep(0.2)
    capture_screen(output_file = 'tmp/screenshot.png')
    root.deiconify()


button = tk.Button(root, text="截图", command=on_button_click)
button.pack()



# 进入主事件循环
root.mainloop()