import time
import ctypes
from ctypes import wintypes
import random

class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]

user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

# 每次移动距离（随机范围）
MIN_STEP = 10
MAX_STEP = 50
# 间隔时间（随机范围，避免规律）
MIN_INTERVAL = 3
MAX_INTERVAL = 8

def get_mouse_position():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def set_mouse_position(x, y):
    user32.SetCursorPos(x, y)

def simulate_key_press():
    # 模拟按一下Shift键，重置系统空闲状态
    VK_SHIFT = 0x10
    user32.keybd_event(VK_SHIFT, 0, 0, 0)
    user32.keybd_event(VK_SHIFT, 0, 0x0002, 0)

def calculate_safe_position(x, y):
    # 随机选择移动方向和距离
    step = random.randint(MIN_STEP, MAX_STEP)
    direction = random.choice(["right", "left", "up", "down"])
    
    if direction == "right" and x + step < SCREEN_WIDTH:
        return x + step, y
    elif direction == "left" and x - step >= 0:
        return x - step, y
    elif direction == "up" and y - step >= 0:
        return x, y - step
    elif direction == "down" and y + step < SCREEN_HEIGHT:
        return x, y + step
    else:
        # 方向不可行时，换一个方向
        return calculate_safe_position(x, y)

def main():
    print("Mouse mover started. Press Ctrl + C to stop.")
    print(f"Move every {MIN_INTERVAL}-{MAX_INTERVAL} seconds, step = {MIN_STEP}-{MAX_STEP}px")
    try:
        while True:
            original_x, original_y = get_mouse_position()
            new_x, new_y = calculate_safe_position(original_x, original_y)
            
            # 移动鼠标
            set_mouse_position(new_x, new_y)
            time.sleep(0.1)
            # 移回原位
            set_mouse_position(original_x, original_y)
            
            # 模拟按键，重置系统空闲
            simulate_key_press()
            
            # 随机间隔，避免规律
            interval = random.randint(MIN_INTERVAL, MAX_INTERVAL)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMouse mover stopped.")

if __name__ == "__main__":
    main()
