import pygame as pg
import os
import time
import random
import sys

pg.init()

WIDTH, HEIGHT = 400, 600
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("車ゲーム")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

#背景の設定
background = pg.image.load(f"{MAIN_DIR}/fig/way.png").convert_alpha()
background = (pg.transform.scale(background, (WIDTH, HEIGHT)))
#background_rect = background.get_rect()
scroll_speed = 5
scroll_y = 0

player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height -20
player_speed = 5

obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5
obstacle_interval = 5 * 30 #５秒毎に障害物を生成

#障害物画像の読み込み
obstacle_image = pg.image.load(f"{MAIN_DIR}/fig/pin.png").convert_alpha()
obstacle_images = [pg.transform.scale(obstacle_image, (obstacle_width, obstacle_height)) for i in range(1, 11)]
#obstacle_rect = obstacle_image.get_rect()

def draw_player(x, y):
    pg.draw.rect(screen, WHITE, [x, y, player_width, player_height])
def draw_obstacle(x, y):
    pg.draw.rect(screen, RED, [x, y, obstacle_width, obstacle_height])

def main():
    global player_x,scroll_y
    clock = pg.time.Clock()

    obstacles = []
    score = 0
    obstacle_timer = 0
    collisions = 0 #衝突階数

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        keys = pg.key.get_pressed()
        player_x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * player_speed

        player_x = max(0, min(WIDTH - player_width, player_x))

        

        #障害物の生成
        obstacle_timer += 1

        # if obstacle_timer >= obstacle_interval:
            # obstacle_x = random.randint(0, WIDTH - obstacle_image.get_width())
            # obstacle_y = -obstacle_image.get_height()
            # obstacles.append([obstacle_x, obstacle_y])
            # obstacle_timer = 0
         
        #背景のスクロール
        screen.blit(background, (0, scroll_y))
        screen.blit(background, (0, scroll_y - HEIGHT))
        scroll_y = (scroll_y + scroll_speed) % HEIGHT
        #障害物のスクロール
        # screen.blit(obstacle_image,(0, scroll_y))
        # screen.blit(obstacle_image, (0,scroll_y - HEIGHT))
        if obstacle_timer >= obstacle_interval:
            obstacle_x = random.randint(0, WIDTH - obstacle_image.get_width())
            obstacle_y = -obstacle_image.get_height()
            obstacle_image = random.choice(obstacle_images)
            obstacles.append([obstacle_x, obstacle_y])
            obstacle_timer = 0

        # if random.randint(1, 10) == 1:
        #     obstacle_x = random.randint(0, WIDTH - obstacle_width)
        #     obstacle_y = -obstacle_height
        #     obstacles.append([obstacle_x, obstacle_y])

        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if(
                player_x < obstacle[0] + obstacle_width
                and player_x + player_width > obstacle[0]
                and player_y < obstacle[1] + obstacle_height
                and player_y + player_height > obstacle[1]
            ):
                print(f"Score: {score}")
                collisions += 1
                if collisions >= 3: #３回衝突したら
                    print("Game Over!")
                    pg.quit()
                    sys.exit()

        #screen.fill((0, 0, 0))
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] <= HEIGHT]

        draw_player(player_x, player_y)

        # for obstacle in obstacles:
        #     screen.blit(obstacle_image,obstacle_x,obstacle_y)

        score += 1

        pg.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    main()
        
