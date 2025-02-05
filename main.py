import re
import time
import random
import pyautogui
import keyboard
import tkinter as tk
from PIL import Image, ImageTk
from Tools import *

CLICK_BUTTON_NUMS = 8
CONFIG_PATH = 'config/config.json'
SCREENSHOT_PATH = 'tmp/screenshot.png'

with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)


root = tk.Tk()
root.title("AUTOMATIC_CLICKER -- designed by 孙笑川")
root.geometry("600x600")
# 显示sxc照片
image = Image.open('config/sxc.jpg')
image = image.resize((60, 80))
photo = ImageTk.PhotoImage(image)
label = tk.Label(root, image=photo)
label.image = photo
label.place(relx=0.1, rely=0.05, anchor=tk.CENTER)

def save_changed_click_location_set(event):
    """保存修改的点击位置"""
    # capture_screen
    root.iconify()
    time.sleep(0.2)
    capture_screen(output_file = 'tmp/screenshot.png')
    root.deiconify()
    # draw rect
    selector = ImageSelector(SCREENSHOT_PATH)  # 替换为你的图片路径
    selector.run()
    center_x, center_y = selector.get_center()
    # save changed click location set
    index = int(re.search(r'\d+$', str(event.widget)).group()) if re.search(r'\d+$', str(event.widget)) else 1
    CONFIG[str(index) + '_botton_location'] = [center_x, center_y]

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(CONFIG, file)

def save_changed_click_delay_set(event):
    """保存修改的点击间隔"""
    user_input = event.widget.get("1.0", tk.END).strip()
    # save changed set
    index = int(int(re.search(r'\d+$', str(event.widget)).group())/2)
    CONFIG[str(index) + '_botton_delay'] = int(user_input) if user_input else "None"
    if not user_input: 
        CONFIG[str(index) + '_botton_location'] = "None"

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(CONFIG, file)

def save_changed_click_time_randomly_offset_maximum(event):
    """修改点击时间随机偏移最大值"""
    user_input = event.widget.get("1.0", tk.END).strip()
    CONFIG['click_time_randomly_offset_maximum'] = int(user_input)

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(CONFIG, file)

def save_changed_click_location_randomly_offset_maximum(event):
    """修改点击位置随机偏移最大值"""
    user_input = event.widget.get("1.0", tk.END).strip()
    CONFIG['click_location_randomly_offset_maximum'] = int(user_input)

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(CONFIG, file)

def mouse_click(param_config_path = 'config/config.json'):
    """模拟鼠标点击"""
    (botton_delay, botton_location, time_offset, location_offset) = get_config_param(param_config_path)
    root.iconify()
    time.sleep(0.2)
    while True:
        pyautogui.PAUSE = 0

        if keyboard.is_pressed('esc'):
            root.deiconify()
            break

        for i in range(min(len(botton_delay) , len(botton_location))):
            click_x = botton_location[i][0] + random.randint(0, int(location_offset))
            click_y = botton_location[i][1] + random.randint(0, int(location_offset))
            click_delay = (botton_delay[i] + random.randint(0, int(time_offset)))/1000
            pyautogui.click(click_x, click_y)
            time.sleep(click_delay)

# 参数设置控件
tk.Label(root, text='按键坐标', bg='#D1EEEE').place(relx=0.35, rely=0.05, anchor=tk.CENTER, width=80, height=30)
tk.Label(root, text='按键间隔', bg='#D1EEEE').place(relx=0.6, rely=0.05, anchor=tk.CENTER, width=80, height=30)
for i in range(CLICK_BUTTON_NUMS):

    button_set = tk.Button(root, text='按键' + str(i + 1) + '设置', bg='#D1EEEE')
    button_set.place(relx=0.1, rely=0.15 + 0.08 * i, anchor=tk.CENTER, width=80, height=30)
    button_set.bind("<Button-1>", save_changed_click_location_set)

    rect_set = tk.Text(root, width=15, height=1)
    rect_set.place(relx=0.35, rely=0.15 + 0.08 * i, anchor=tk.CENTER)
    rect_set.insert(tk.END, str(CONFIG[str(i + 1) + '_botton_location']))

    delay_set = tk.Text(root, width=10, height=1)
    delay_set.place(relx=0.6, rely=0.15 + 0.08 * i, anchor=tk.CENTER)
    delay_set.insert(tk.END, CONFIG[str(i + 1) + '_botton_delay'])
    delay_set.bind("<FocusOut>", save_changed_click_delay_set)

tk.Label(root, text='点击时间随机偏移', bg='#D1EEEE').place(relx=0.85, rely=0.15, anchor=tk.CENTER, width=150, height=30)
time_offset = tk.Text(root, width=10, height=1)
time_offset.place(relx=0.85, rely=0.23, anchor=tk.CENTER)
time_offset.insert(tk.END, CONFIG['click_time_randomly_offset_maximum'])
time_offset.bind("<FocusOut>", save_changed_click_time_randomly_offset_maximum)

tk.Label(root, text='点击位置随机偏移', bg='#D1EEEE').place(relx=0.85, rely=0.35, anchor=tk.CENTER, width=150, height=30)
time_offset = tk.Text(root, width=10, height=1)
time_offset.place(relx=0.85, rely=0.43, anchor=tk.CENTER)
time_offset.insert(tk.END, CONFIG['click_location_randomly_offset_maximum'])
time_offset.bind("<FocusOut>", save_changed_click_location_randomly_offset_maximum)

# 自动点击部分控件
tk.Button(root, text="自动点击", bg = '#FFFF00', command=mouse_click).place(relx=0.5, rely=0.9, anchor=tk.CENTER, width=100, height=40)


# 进入主事件循环
root.mainloop()