import pygame
import random

# 初始化常量
BLOCK_SIZE = 30  # 每个方块的大小
GRID_WIDTH = 10  # 游戏区域宽度（以方块数计）
GRID_HEIGHT = 20 # 游戏区域高度
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # 屏幕宽度，额外空间用于显示下一个方块
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT      # 屏幕高度

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
        # 矩阵转置后反转每一行来实现90度旋转
        # 首先转置矩阵
        rotated = [[self.shape[j][i] for j in range(len(self.shape))]
                  for i in range(len(self.shape[0]))]
        # 然后反转每一行
        rotated = [row[::-1] for row in rotated]
        return rotated

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()

        # 添加游戏状态
        self.game_started = False

        # 初始化字体
        try:
            self.font = pygame.font.SysFont('arial', 24)
            self.title_font = pygame.font.SysFont('arial', 48)
        except:
            self.font = None
            self.title_font = None

        self.reset_game()

    def draw_start_screen(self):
        """绘制开始界面"""
        self.screen.fill(BLACK)

        if self.title_font and self.font:
            # 绘制游戏标题
            title = self.title_font.render('TETRIS', True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title, title_rect)

            # 绘制开始按钮
            start_text = self.font.render('Click to Start', True, WHITE)
            self.start_button = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))

            # 绘制按钮边框
            pygame.draw.rect(self.screen, WHITE, self.start_button.inflate(20, 20), 2)
            self.screen.blit(start_text, self.start_button)
        else:
            # 如果字体加载失败，使用简单的矩形显示
            self.start_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT * 2 // 3 - 20,
                                          SCREEN_WIDTH // 2, 40)
            pygame.draw.rect(self.screen, WHITE, self.start_button, 2)

    def handle_start_screen(self):
        """处理开始界面的输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.game_started = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 也可以通过回车键开始
                    self.game_started = True
        return True

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        # 添加新的属性
        self.drop_speed = 30  # 正常下落速度, 指定下落一格的帧率
        self.fast_drop_speed = 3  # 快速下落速度, 指定下落一格的帧率
        self.current_drop_speed = self.drop_speed  # 当前下落速度
        self.drop_time = 0

        # 添加移动控制相关的属性
        self.move_delay = 12  # 开始持续移动前的延迟
        self.move_repeat = 4  # 持续移动的重复率
        self.left_pressed = 0  # 左键按下的时间
        self.right_pressed = 0  # 右键按下的时间

    def new_piece(self):
        # 随机生成新方块
        shape = random.choice(SHAPES)
        return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)

    def valid_move(self, piece, x, y, shape):
        # 检查移动是否有效
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if not (0 <= x + j < GRID_WIDTH and
                           y + i < GRID_HEIGHT and
                           (y + i < 0 or self.grid[y + i][x + j] == 0)):
                        return False
        return True

    def handle_input(self):
        """处理用户输入"""
        keys = pygame.key.get_pressed()

        # 处理水平移动
        if keys[pygame.K_LEFT]:
            self.left_pressed += 1
            if self.left_pressed == 1 or (self.left_pressed > self.move_delay and self.left_pressed % self.move_repeat == 0):
                self.move(-1)
        else:
            self.left_pressed = 0

        if keys[pygame.K_RIGHT]:
            self.right_pressed += 1
            if self.right_pressed == 1 or (self.right_pressed > self.move_delay and self.right_pressed % self.move_repeat == 0):
                self.move(1)
        else:
            self.right_pressed = 0

        # 处理下落速度
        if keys[pygame.K_DOWN]:
            self.current_drop_speed = self.fast_drop_speed
        else:
            self.current_drop_speed = self.drop_speed

        # 处理其他事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.rotate()

        return True

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            if not self.game_started:
                # 显示开始界面
                self.draw_start_screen()
                running = self.handle_start_screen()
            else:
                # 游戏主循环
                if not self.game_over:
                    # 处理输入
                    if not self.handle_input():
                        break

                    # 自动下落
                    self.drop_time += 1
                    if self.drop_time > self.current_drop_speed:
                        self.drop()
                        self.drop_time = 0

                    # 更新显示
                    self.draw()
                else:
                    # 如果游戏结束，返回开始界面
                    self.game_started = False
                    self.reset_game()

            pygame.display.flip()

        pygame.quit()

    def move(self, dx):
        # 水平移动方块
        if self.valid_move(self.current_piece, self.current_piece.x + dx, self.current_piece.y, self.current_piece.shape):
            self.current_piece.move(dx)

    def drop(self):
        # 方块下落
        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1, self.current_piece.shape):
            self.current_piece.move_down()
        else:
            self.freeze_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y, self.current_piece.shape):
                self.game_over = True

    def draw(self):
        # 绘制游戏界面
        self.screen.fill(BLACK)

        # 绘制游戏区域边框
        border_rect = pygame.Rect(0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(self.screen, WHITE, border_rect, 2)  # 2是边框宽度

        # 绘制网格线
        for x in range(GRID_WIDTH):
            pygame.draw.line(self.screen, (40, 40, 40),
                           (x * BLOCK_SIZE, 0),
                           (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        for y in range(GRID_HEIGHT):
            pygame.draw.line(self.screen, (40, 40, 40),
                           (0, y * BLOCK_SIZE),
                           (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))

        # 绘制已固定的方块
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell,
                                   (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1,
                                    BLOCK_SIZE - 2, BLOCK_SIZE - 2))

        # 绘制当前方块
        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       ((self.current_piece.x + j) * BLOCK_SIZE + 1,
                                        (self.current_piece.y + i) * BLOCK_SIZE + 1,
                                        BLOCK_SIZE - 2, BLOCK_SIZE - 2))

        # 绘制分数
        self.draw_score()

        # 绘制下一个方块预览
        self.draw_next_piece()

    def draw_score(self):
        """绘制分数"""
        # 在游戏区域右侧绘制分数
        score_x = (GRID_WIDTH + 1) * BLOCK_SIZE
        score_y = BLOCK_SIZE

        if self.font:
            # 使用字体渲染分数
            score_text = self.font.render(f'Score:', True, WHITE)
            score_value = self.font.render(f'{self.score}', True, WHITE)

            # 绘制分数文本
            self.screen.blit(score_text, (score_x, score_y))
            self.screen.blit(score_value, (score_x, score_y + 30))
        else:
            # 如果字体加载失败，使用简单的矩形显示
            pygame.draw.rect(self.screen, WHITE,
                           (score_x, score_y, BLOCK_SIZE * 4, BLOCK_SIZE), 1)

    def draw_next_piece(self):
        """绘制下一个方块预览"""
        # 预览区域位置（在分数显示下方）
        preview_x = (GRID_WIDTH + 1) * BLOCK_SIZE
        preview_y = BLOCK_SIZE * 4

        if self.font:
            # 绘制预览标题
            next_text = self.font.render('Next:', True, WHITE)
            self.screen.blit(next_text, (preview_x, preview_y - 30))

        # 绘制预览区域边框
        preview_size = BLOCK_SIZE * 4
        preview_rect = pygame.Rect(preview_x, preview_y, preview_size, preview_size)
        pygame.draw.rect(self.screen, WHITE, preview_rect, 2)

        if self.next_piece:
            # 计算居中偏移
            shape_height = len(self.next_piece.shape)
            shape_width = len(self.next_piece.shape[0])
            offset_x = (4 - shape_width) * BLOCK_SIZE // 2
            offset_y = (4 - shape_height) * BLOCK_SIZE // 2

            # 绘制下一个方块
            for i, row in enumerate(self.next_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.next_piece.color,
                                       (preview_x + offset_x + j * BLOCK_SIZE + 1,
                                        preview_y + offset_y + i * BLOCK_SIZE + 1,
                                        BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def freeze_piece(self):
        # 将当前方块固定到网格中
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

    def clear_lines(self):
        # 清除已完成的行并计分
        lines_cleared = 0
        for i in range(GRID_HEIGHT - 1, -1, -1):
            if all(cell != 0 for cell in self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        # 计算分数
        if lines_cleared > 0:
            self.score += (100 * lines_cleared) * lines_cleared

    def rotate(self):
        # 获取旋转后的形状
        rotated_shape = self.current_piece.rotate_shape()
        # 检查旋转后的位置是否有效
        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y, rotated_shape):
            self.current_piece.shape = rotated_shape
            self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
        else:
            # 尝试墙踢（wall kick）：如果旋转后撞墙，尝试左右移动一格
            # 向左尝试
            if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y, rotated_shape):
                self.current_piece.x -= 1
                self.current_piece.shape = rotated_shape
                self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
            # 向右尝试
            elif self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y, rotated_shape):
                self.current_piece.x += 1
                self.current_piece.shape = rotated_shape
                self.current_piece.rotation = (self.current_piece.rotation + 1) % 4

def main():
    game = TetrisGame()
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
