import pygame
import sys
import random

# 初期化
pygame.init()

# 画面の設定
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("断罪のこうかとんクラッシャー")

# 色の設定
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# プレイヤーの設定
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - player_size - 10

# 障害物の設定
obstacle_size = 50
obstacle_speed = 5
obstacle_frequency = 25
obstacles = []

# スコアの初期化
score = 0
font = pygame.font.Font(None, 36)

# ゲームループ
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # プレイヤーの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += 5

    # 障害物の生成
    if random.randrange(obstacle_frequency) == 0:
        obstacle_x = random.randrange(width - obstacle_size)
        obstacle_y = -obstacle_size
        obstacles.append([obstacle_x, obstacle_y])

    # 障害物の移動と衝突判定
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
        if (
            player_x < obstacle[0] < player_x + player_size
            and player_y < obstacle[1] < player_y + player_size
        ):
            pygame.quit()
            sys.exit()

    # 画面の更新
    screen.fill(white)
    pygame.draw.rect(screen, black, [player_x, player_y, player_size, player_size])

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, [obstacle[0], obstacle[1], obstacle_size, obstacle_size])

    # スコアの表示
    score_text = font.render("Score: {}".format(score), True, black)
    screen.blit(score_text, [10, 10])

    # スコアの更新
    score += 1

    # 画面の描画
    pygame.display.flip()

    # フレームレートの制御
    clock.tick(30)