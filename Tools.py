import json
import mss
import mss.tools
import cv2

def capture_screen(output_file):
    """获取当前屏幕截图"""
    with mss.mss() as sct:
        # 获取第一个显示器的信息
        monitor = sct.monitors[1]
        # 捕获屏幕
        sct_img = sct.grab(monitor)
        # 将捕获的图像保存为文件
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)

class ImageSelector:
    def __init__(self, image_path):
        self.drawing = False  # 是否正在绘制矩形
        self.ix, self.iy = -1, -1  # 矩形起始坐标
        self.fx, self.fy = -1, -1  # 矩形结束坐标
        self.img = cv2.imread(image_path)  # 读取图片
        if self.img is None:
            raise ValueError("图片路径错误或图片无法读取！")
        self.center_x, self.center_y = -1, -1  # 矩形框中心点坐标，初始化为无效值

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下
            self.drawing = True
            self.ix, self.iy = x, y  # 记录起始点

        elif event == cv2.EVENT_MOUSEMOVE:  # 鼠标移动
            if self.drawing:
                img_copy = self.img.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 0), 2)  # 实时绘制矩形
                cv2.imshow("Image", img_copy)

        elif event == cv2.EVENT_LBUTTONUP:  # 鼠标左键释放
            self.drawing = False
            self.fx, self.fy = x, y  # 记录结束点
            cv2.rectangle(self.img, (self.ix, self.iy), (self.fx, self.fy), (0, 255, 0), 2)  # 绘制最终矩形
            cv2.imshow("Image", self.img)

            # 计算矩形框的中心点坐标
            self.center_x = (self.ix + self.fx) // 2
            self.center_y = (self.iy + self.fy) // 2

    def get_center(self):
        # 返回矩形框的中心点坐标
        return self.center_x, self.center_y

    def run(self):
        # 创建窗口并最大化
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # 设置鼠标回调函数
        cv2.setMouseCallback("Image", self.draw_rectangle)

        # 显示图片
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def get_config_param(param_config_path = 'config/config.json'):
    """获取配置参数"""
    with open(param_config_path, 'r') as f:
        config = json.load(f)

    botton_delay = [config[x] for x in config if 'botton_delay' in x and config[x] != 'None']
    botton_location = [config[x] for x in config if 'botton_location' in x and config[x] != 'None']

    return (botton_delay, botton_location,
            config['click_time_randomly_offset_maximum'],
            config['click_location_randomly_offset_maximum'])