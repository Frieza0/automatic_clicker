import time
import json
import random
import mss
import mss.tools
import pyautogui
import keyboard

def capture_screen(output_file):
    """获取当前屏幕截图"""
    with mss.mss() as sct:
        # 获取第一个显示器的信息
        monitor = sct.monitors[1]
        # 捕获屏幕
        sct_img = sct.grab(monitor)
        # 将捕获的图像保存为文件
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)

def get_config_param(param_config_path = 'config/config.json'):
    """获取配置参数"""
    with open(param_config_path, 'r') as f:
        config = json.load(f)

    botton_delay = [config[x] for x in config if 'botton_delay' in x and config[x] != 'None']
    botton_location = [config[x] for x in config if 'botton_location' in x and config[x] != 'None']

    return (botton_delay, botton_location,
            config['click_time_randomly_offset_maximum'],
            config['click_location_randomly_offset_maximum'])

def mouse_click(param_config_path = 'config/config.json'):
    """模拟鼠标点击"""
    (botton_delay, botton_location, time_offset, location_offset) = get_config_param(param_config_path)

    while True:
        pyautogui.PAUSE = 0

        if keyboard.is_pressed('esc'):
            break

        for i in range(len(botton_delay)):
            click_x = botton_location[i][0] + random.randint(1, int(location_offset))
            click_y = botton_location[i][1] + random.randint(1, int(location_offset))
            click_delay = (botton_delay[i] + random.randint(1, int(time_offset)))/1000
            pyautogui.click(click_x, click_y)
            time.sleep(click_delay)
