import os
from pathlib import Path

# 游戏区域常量
BLOCK_SIZE = 30  # 每个方块的大小
GRID_WIDTH = 10  # 游戏区域宽度（以方块数计）
GRID_HEIGHT = 20  # 游戏区域高度
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # 屏幕宽度，额外空间用于显示下一个方块
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT      # 屏幕高度

# 资源路径
PROJECT_ROOT = Path(__file__).parent.parent
print("PROJECT_ROOT: ", PROJECT_ROOT)
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# 音乐文件路径
BACKGROUND_MUSIC_PATH = os.path.join(SOUNDS_DIR, 'background.mp3')

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),   # 青色 - I
    (255, 255, 0),   # 黄色 - O
    (128, 0, 128),   # 紫色 - T
    (0, 255, 0),     # 绿色 - S
    (255, 0, 0),     # 红色 - Z
    (0, 0, 255),     # 蓝色 - J
    (255, 127, 0)    # 橙色 - L
]

# 俄罗斯方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[1, 1, 0],
     [0, 1, 1]],     # Z
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]]      # L
]

