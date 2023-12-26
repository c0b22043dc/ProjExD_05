import pygame as pg
import random
import pygame
import sys
import random

# 初期化
pygame.init()


WIDTH, HEIGHT = 400, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("車ゲーム")

# 障害物の設定
obstacle_size = 50
obstacle_speed = 5
obstacle_frequency = 25
obstacles = []
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5


# 画面の設定
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("断罪のこうかとんクラッシャー")


# 色の設定
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height -20
player_speed = 5

# スコアの初期化
score = 0
font = pygame.font.Font(None, 36)

def draw_player(x, y):
    pg.draw.rect(screen, white, [x, y, player_width, player_height])
def draw_obstacle(x, y):
    pg.draw.rect(screen, red, [x, y, obstacle_width, obstacle_height])
def game():
    clock = pg.time.Clock()

    obstacles = []
    score = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        keys = pg.key.get_pressed()
        player_x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * player_speed

        player_y = max(0, min(WIDTH - player_width, player_x))

        # スコアの表示
        score_text = font.render("Score: {}".format(score), True, black)
        screen.blit(score_text, [10, 10])

        # スコアの更新
        score += 1

        if random.randint(1, 10) == 1:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = -obstacle_height
            obstacles.append([obstacle_x, obstacle_y])

        for obstacle in obstacles:
            obstacle[1] +- obstacle_speed
            if(
                player_x < obstacle[0] + obstacle_width
                and player_x + player_width > obstacle[0]
                and player_y < obstacle[1] + obstacle_height
                and player_y + player_height > obstacle[1]
            ):
                print(f"Game Over! Score: {score}")
                pg.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        draw_player(player_x, player_y)

        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])

        pg.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    game()