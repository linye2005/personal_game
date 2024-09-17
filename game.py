import pygame
import sys
import random
from pygame import *
from time import time

# 初始化Pygame
pygame.init()
pygame.font.init() 
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 定义常量
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
tile_size = 100  # 定义图片方块的大小


add_time_icon = pygame.image.load("./pictures/add time icon.png")  # 加载加时间道具图片
add_time_icon = pygame.transform.scale(add_time_icon, (50, 50))  # 缩放道具图片

# 定义游戏变量
clock = pygame.time.Clock()
total_time = 30  # 倒计时30秒
start_time = time()
game_over = False
game_win = False
layer_count = 3  # 图案分层数
can_add_time = True  # 可以加时间的标志

# 加载动物图片
img1 = pygame.image.load("./pictures/1.png")  
img2 = pygame.image.load("./pictures/2.png")  
img3 = pygame.image.load("./pictures/3.png")  
img6 = pygame.image.load("./pictures/6.png")  
img4 = pygame.image.load("./pictures/4.png")
img5 = pygame.image.load("./pictures/5.png")
img7 = pygame.image.load("./pictures/7.png")
img8 = pygame.image.load("./pictures/8.png")
img9 = pygame.image.load("./pictures/9.png")

# 缩放图片
img1 = pygame.transform.scale(img1, (tile_size, tile_size))
img2 = pygame.transform.scale(img2, (tile_size, tile_size))
img3 = pygame.transform.scale(img3, (tile_size, tile_size))
img4 = pygame.transform.scale(img4, (tile_size, tile_size))
img5 = pygame.transform.scale(img5, (tile_size, tile_size))
img6 = pygame.transform.scale(img6, (tile_size, tile_size))
img7 = pygame.transform.scale(img7, (tile_size, tile_size))
img8 = pygame.transform.scale(img8, (tile_size, tile_size))
img9 = pygame.transform.scale(img9, (tile_size, tile_size))


# 随机生成成对的动物图片
def generate_tiles(layer_count):
    tiles = []
    images = [img1,img2,img3,img4,img5,img6,img7,img8,img9]  # 动物图片列表
    tile_pairs = []

    # 创建成对的图片
    for img in images:
        for _ in range(layer_count * 2):  # 每个动物生成两对
            tile_pairs.append({"image": img, "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - tile_size), random.randint(0, SCREEN_HEIGHT - tile_size), tile_size, tile_size), "layer": 0})

    # 随机打乱这些方块的位置
    random.shuffle(tile_pairs)

    return tile_pairs

# 绘制图案
def draw_tiles(tiles, screen):
    for tile in tiles:
        screen.blit(tile["image"], tile["rect"])
        selected_tiles = []
        if tile in selected_tiles:
            pygame.draw.rect(screen, (255, 255, 0), tile["rect"], 2)  # 绘制选中框

# 主游戏循环
def game_loop(screen, font):
    global game_over, game_win
    tiles = generate_tiles(layer_count)
    selected_tiles = []
    
    while not game_over:
        screen.fill(WHITE)
        elapsed_time = time() - start_time
        remaining_time = total_time - elapsed_time
        
        if remaining_time <= 0:
            game_over = True
            break
        
        # 绘制倒计时
        timer_text = font.render(f"剩余时间: {int(remaining_time)}", True, BLACK)
        screen.blit(timer_text, (10, 10))
        
        # 绘制图案
        draw_tiles(tiles, screen)
        
        # 检测事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for tile in tiles:
                    if tile["rect"].collidepoint(pos):
                        if tile in selected_tiles:
                            selected_tiles.remove(tile)
                        else:
                            selected_tiles.append(tile)
                        break
        
        # 匹配逻辑：如果有两个选择的图案相同则消除
        if len(selected_tiles) == 2:
            if selected_tiles[0]["image"] == selected_tiles[1]["image"]:
                tiles.remove(selected_tiles[0])
                tiles.remove(selected_tiles[1])
            selected_tiles = []

        # 检测胜利条件
        if not tiles:
            game_win = True
            game_over = True

        pygame.display.update()
        clock.tick(30)

# 定义常量
GRID_SIZE = 10
ICON_SIZE = 50
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
ICON_COUNT = 9
SLOT_COUNT = 7

# 加载图片和音乐
bg_image = pygame.image.load('./pictures/bg.png')
music = pygame.mixer.music.load('./music/Daocao.mp3')
pygame.mixer.music.play(-1)

class Start:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('耶了个耶')
        self.big_font = pygame.font.Font('./font/msyh.ttf', 48)
        self.font = pygame.font.Font('./font/msyh.ttf', 24)
        self.small_font = pygame.font.Font('./font/msyh.ttf', 18)
        self.start_button_easy = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50)
        self.start_button_hard = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    def start(self):
        running = True
        current_difficulty = 'easy'  # 假设默认难度是简单，你可以根据需要调整
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if self.start_button_easy.collidepoint(event.pos):
                        game = Game(difficulty='easy')
                        game.run()
                        running = False
                    elif self.start_button_hard.collidepoint(event.pos):
                        game = Game(difficulty='hard')
                        game.run()
                        running = False
                    elif self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            # 保存当前难度设置
            self.current_difficulty = current_difficulty
            self.draw_main_menu()

    def draw_main_menu(self):
        bg_image = pygame.transform.scale(pygame.image.load('./pictures/bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg_image, (0, 0))

        title_text = self.big_font.render('耶了个耶', True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        start_easy_text = self.font.render('简单模式', True, BLACK)
        self.screen.blit(start_easy_text, (self.start_button_easy.x + 50, self.start_button_easy.y + 10))

        start_hard_text = self.font.render('困难模式', True, BLACK)
        self.screen.blit(start_hard_text, (self.start_button_hard.x + 50, self.start_button_hard.y + 10))

        exit_text = self.font.render('退出游戏', True, BLACK)
        self.screen.blit(exit_text, (self.exit_button.x + 50, self.exit_button.y + 10))

           # 分行显示游戏规则
        rules_lines = [
            "游戏规则：",
            "1. 简单模式：两个相同图案消除得1分。",
            "2. 困难模式：三个相同图案消除得1分。",
            "3. 加时道具只能使用一次加五秒钟。"
        ]
        rules_height = 650  # 规则文本起始的 Y 坐标，位于屏幕垂直方向300像素的位置
        for line in rules_lines:
            rules_text = self.small_font.render(line, True, BLACK)
            rules_rect = rules_text.get_rect(center=(SCREEN_WIDTH // 2, rules_height))
            self.screen.blit(rules_text, rules_rect)
            rules_height += 40  # 更新 Y 坐标以换行


        pygame.display.flip()

class End:
    def __init__(self, screen, result, game):
        self.screen = screen
        self.result = result
        self.game = game
        self.font = pygame.font.Font('./font/msyh.ttf', 36)
        self.button_font = pygame.font.Font('./font/msyh.ttf', 24)
        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        self.menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 180, 200, 50)
        self.background = pygame.image.load(f"./pictures/{result}.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        result_text = self.font.render("成功啦！" if self.result == "win" else "时间到了！", True, BLACK)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2+5, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(result_text, result_rect)

        score_text = self.font.render(f"得分: {self.game.score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        start_text = self.button_font.render("重新开始", True, BLACK)
        self.screen.blit(start_text, (self.start_button.x + 50, self.start_button.y + 10))
        menu_text = self.button_font.render("返回主菜单", True, BLACK)
        self.screen.blit(menu_text, (self.menu_button.x + 40, self.menu_button.y + 10))

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.restart_game()
                elif self.menu_button.collidepoint(event.pos):
                    self.return_to_menu()

    def restart_game(self):
        self.game.reset_game(self.game.difficulty)
        self.game.run()

    def return_to_menu(self):
        self.game.game_over = False
        start = Start()
        start.start()


class Game:
    def __init__(self, difficulty='easy'):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('耶了个耶')
        self.font = pygame.font.Font('./font/msyh.ttf', 24)
        self.clock = pygame.time.Clock()
        self.total_time = 30
        self.start_time = time()
        self.game_over = False
        self.game_win = False
        self.layer_count = 3
        self.tiles = self.generate_tiles(self.layer_count)
        self.selected_tiles = []
        self.add_time_button = pygame.Rect(SCREEN_WIDTH - 60, 10, 50, 50)
        self.can_add_time = True
        self.score = 0
        self.difficulty = difficulty

    def generate_tiles(self, layer_count):
        tiles = []
        images = [img1,img2,img3,img4,img5,img6,img7,img8,img9] 
        for img in images:
            for _ in range(layer_count * 2):
                tile = {"image": img, "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - tile_size),
                                                          random.randint(0, SCREEN_HEIGHT - tile_size),
                                                          tile_size, tile_size), "layer": layer_count}
                tiles.append(tile)
        return tiles

    def run(self):
        result = "running"
        while result == "running":
            self.screen.fill(WHITE)
            self.handle_events()
            self.update_game()
            self.draw_game()
            pygame.display.update()
            self.clock.tick(30)
            result = self.check_game_over()

        if result in ["win", "lose"]:
            end_screen = End(self.screen, result, self)
            end_screen.draw()
            while True:
                end_screen.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.add_time_button.collidepoint(pos) and self.can_add_time:
                    self.total_time += 5
                    self.start_time += 5
                    self.can_add_time = False
                top_tile = None
                for tile in reversed(self.tiles):
                    if tile["rect"].collidepoint(pos):
                        top_tile = tile
                        break
                if top_tile and top_tile not in self.selected_tiles:
                    self.selected_tiles.append(top_tile)
                    if self.difficulty == 'easy' and len(self.selected_tiles) == 2:
                        if self.selected_tiles[0]["image"] == self.selected_tiles[1]["image"]:
                            for tile in self.selected_tiles:
                                if tile in self.tiles:
                                    self.tiles.remove(tile)
                            self.score += 1
                        self.selected_tiles = []
                    elif self.difficulty == 'hard' and len(self.selected_tiles) == 3:
                        if (self.selected_tiles[0]["image"] == self.selected_tiles[1]["image"] ==
                                self.selected_tiles[2]["image"]):
                            for tile in self.selected_tiles:
                                if tile in self.tiles:
                                    self.tiles.remove(tile)
                            self.score += 1
                        self.selected_tiles = []

    def update_game(self):
        elapsed_time = time() - self.start_time
        self.total_time = 30 - elapsed_time
        if self.total_time <= 0:
            self.game_over = True

    def draw_game(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_add_time_button()
        timer_text = self.font.render(f"剩余时间: {int(self.total_time)}", True, BLACK)
        self.screen.blit(timer_text, (10, 10))

    def draw_add_time_button(self):
        self.screen.blit(add_time_icon, self.add_time_button)  # 绘制加时间按钮

    def draw_background(self):
        bg_image = pygame.transform.scale(pygame.image.load("./pictures/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg_image, (0, 0))  # 绘制背景图

    def draw_tiles(self):
        for tile in self.tiles:
            self.screen.blit(tile["image"], tile["rect"])
            if tile in self.selected_tiles:
                pygame.draw.rect(self.screen, (255, 255, 0), tile["rect"], 2)  # 绘制选中框

    def check_game_over(self):
        if not self.tiles:
            self.game_win = True
            self.game_over = True
            return "win"
        elif self.total_time <= 0:
            self.game_over = True
            return "lose"
        return "running"

    def reset_game(self, difficulty):
        self.__init__(difficulty)  # 重置游戏状态并保留难度设置

if __name__ == '__main__':
    start = Start()
    start.start()