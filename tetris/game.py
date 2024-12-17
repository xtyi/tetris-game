import pygame
import pygame_gui
import random
from tetris.constants import *
from tetris.tetromino import Tetromino


class TetrisGame:
    def __init__(self):
        pygame.init()
        # screen 是一个 main Surface
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        
        # 初始化 UI Manager 并加载主题
        self.ui_manager = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            'tetris/data/theme.json'
        )
        
        # 创建开始界面的UI元素
        self.create_start_screen_elements()
        # 创建游戏界面的UI元素
        self.create_game_elements()
        
        self.init_music()
        self.init_font()
        
        self.game_started = False
        self.reset_game()

    def create_start_screen_elements(self):
        """创建开始界面的UI元素"""
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT*2//3), (200, 50)),
            text='START GAME',
            manager=self.ui_manager,
            object_id="#start_button"
        )

    def create_game_elements(self):
        """创建游戏界面的UI元素"""
        # 创建分数面板背景
        self.score_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((GRID_WIDTH * BLOCK_SIZE + 10, BLOCK_SIZE - 10), (170, 50)),
            manager=self.ui_manager,
            starting_height=1
        )
        
        # 在面板上创建分数标签
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, 5), (160, 40)),
            text='Score: 0',
            manager=self.ui_manager,
            container=self.score_panel,
            object_id="#score_label"
        )
        
        # 初始时隐藏游戏界面元素
        self.score_panel.hide()

    def init_music(self):
        """初始化音乐系统"""
        pygame.mixer.init()
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.set_volume(0.5)  # 设置音量

    def start_music(self):
        """开始播放背景音乐"""
        pygame.mixer.music.play(-1, fade_ms=5000)  # -1表示循环播放

    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.fadeout(2000)

    def init_font(self):
        self.font = pygame.font.SysFont("arial", 24)
        self.title_font = pygame.font.SysFont("arial", 48)


    def draw_start_screen(self):
        """绘制开始界面"""
        self.screen.fill(BLACK)
        
        # 绘制游戏标题
        title = self.title_font.render("TETRIS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        # UI Manager会自动绘制按钮
        self.ui_manager.draw_ui(self.screen)

    def handle_start_screen(self):
        """处理开始界面的输入"""
        time_delta = self.clock.tick(60)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.game_started = True
                    self.start_button.hide()  # 隐藏开始按钮
                    self.score_panel.show()   # 显示分数面板
                    self.start_music()        # 开始播放音乐
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_started = True
                    self.start_button.hide()  # 隐藏开始按钮
                    self.score_panel.show()   # 显示分数面板
                    self.start_music()        # 开始播放音乐
                
            self.ui_manager.process_events(event)
        
        self.ui_manager.update(time_delta)
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

        # 重置UI元素状态
        self.start_button.show()
        self.score_panel.hide()
        
        # 停止音乐
        self.stop_music()

    def new_piece(self):
        # 随机生成新方块
        shape = random.choice(SHAPES)
        return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)

    def valid_move(self, piece, x, y, shape):
        # 检查移动是否有效
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if not (
                        0 <= x + j < GRID_WIDTH
                        and y + i < GRID_HEIGHT
                        and (y + i < 0 or self.grid[y + i][x + j] == 0)
                    ):
                        return False
        return True

    def handle_input(self):
        """处理用户输入"""
        keys = pygame.key.get_pressed()

        # 处理水平移动
        if keys[pygame.K_LEFT]:
            self.left_pressed += 1
            if self.left_pressed == 1 or (
                self.left_pressed > self.move_delay
                and self.left_pressed % self.move_repeat == 0
            ):
                self.move(-1)
        else:
            self.left_pressed = 0

        if keys[pygame.K_RIGHT]:
            self.right_pressed += 1
            if self.right_pressed == 1 or (
                self.right_pressed > self.move_delay
                and self.right_pressed % self.move_repeat == 0
            ):
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
            time_delta = self.clock.tick(60)/1000.0

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
                    # 更新 UI Manager
                    self.ui_manager.update(time_delta)
                    self.ui_manager.draw_ui(self.screen)
                else:
                    # 如果游戏结束，返回开始界面
                    self.game_started = False
                    self.reset_game()

            pygame.display.flip()

    def move(self, dx):
        # 水平移动方块
        if self.valid_move(
            self.current_piece,
            self.current_piece.x + dx,
            self.current_piece.y,
            self.current_piece.shape,
        ):
            self.current_piece.move(dx)

    def drop(self):
        # 方块下落
        if self.valid_move(
            self.current_piece,
            self.current_piece.x,
            self.current_piece.y + 1,
            self.current_piece.shape,
        ):
            self.current_piece.move_down()
        else:
            self.freeze_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_move(
                self.current_piece,
                self.current_piece.x,
                self.current_piece.y,
                self.current_piece.shape,
            ):
                self.game_over = True

    def draw(self):
        # 绘制游戏界面
        self.screen.fill(BLACK)

        # 绘制游戏区域边框
        border_rect = pygame.Rect(
            0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, WHITE, border_rect, 2)  # 2是边框宽度

        # 绘制网格线
        for x in range(GRID_WIDTH):
            pygame.draw.line(
                self.screen,
                (40, 40, 40),
                (x * BLOCK_SIZE, 0),
                (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE),
            )
        for y in range(GRID_HEIGHT):
            pygame.draw.line(
                self.screen,
                (40, 40, 40),
                (0, y * BLOCK_SIZE),
                (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE),
            )

        # 绘制已固定的方块
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        cell,
                        (
                            x * BLOCK_SIZE + 1,
                            y * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2,
                        ),
                    )

        # 绘制当前方块
        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            self.screen,
                            self.current_piece.color,
                            (
                                (self.current_piece.x + j) * BLOCK_SIZE + 1,
                                (self.current_piece.y + i) * BLOCK_SIZE + 1,
                                BLOCK_SIZE - 2,
                                BLOCK_SIZE - 2,
                            ),
                        )

        # 绘制下一个方块预览
        self.draw_next_piece()


    def draw_next_piece(self):
        """绘制下一个方块预览"""
        # 预览区域位置（在分数显示下方）
        preview_x = (GRID_WIDTH + 1) * BLOCK_SIZE
        preview_y = BLOCK_SIZE * 4

        if self.font:
            # 绘制预览标题
            next_text = self.font.render("Next:", True, WHITE)
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
                        pygame.draw.rect(
                            self.screen,
                            self.next_piece.color,
                            (
                                preview_x + offset_x + j * BLOCK_SIZE + 1,
                                preview_y + offset_y + i * BLOCK_SIZE + 1,
                                BLOCK_SIZE - 2,
                                BLOCK_SIZE - 2,
                            ),
                        )

    def freeze_piece(self):
        # 将当前方块固定到网格中
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + i][
                        self.current_piece.x + j
                    ] = self.current_piece.color

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
            # 更新分数显示
            self.score_label.set_text(f'Score: {self.score}')

    def rotate(self):
        # 获取旋转后的形状
        rotated_shape = self.current_piece.rotate_shape()
        # 检查旋转后的位置是否有效
        if self.valid_move(
            self.current_piece,
            self.current_piece.x,
            self.current_piece.y,
            rotated_shape,
        ):
            self.current_piece.shape = rotated_shape
            self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
        else:
            # 尝试墙踢（wall kick）：如果旋转后撞墙，尝试左右移动一格
            # 向左尝试
            if self.valid_move(
                self.current_piece,
                self.current_piece.x - 1,
                self.current_piece.y,
                rotated_shape,
            ):
                self.current_piece.x -= 1
                self.current_piece.shape = rotated_shape
                self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
            # 向右尝试
            elif self.valid_move(
                self.current_piece,
                self.current_piece.x + 1,
                self.current_piece.y,
                rotated_shape,
            ):
                self.current_piece.x += 1
                self.current_piece.shape = rotated_shape
                self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
