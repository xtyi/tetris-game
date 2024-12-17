from tetris.constants import COLORS, SHAPES

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def move(self, dx):
        """移动方块"""
        self.x += dx

    def move_down(self):
        """向下移动方块"""
        self.y += 1

    def rotate_shape(self):
        """旋转方块形状"""
        # 矩阵转置后反转每一行来实现90度旋转
        rotated = [[self.shape[j][i] for j in range(len(self.shape))]
                  for i in range(len(self.shape[0]))]
        # 然后反转每一行
        rotated = [row[::-1] for row in rotated]
        return rotated 