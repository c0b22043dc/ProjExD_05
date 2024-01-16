import pygame as pg
import os
import time
import random
import sys
import threading

pg.init()

WIDTH, HEIGHT = 400, 600
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("車ゲーム")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 背景の設定
background = pg.image.load(f"{MAIN_DIR}/fig/way.png").convert_alpha()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
scroll_speed = 5
scroll_y = 0

player_width, player_height = 100, 100
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5
#ガソリンの初期設定
gasoline_width ,gasoline_height = 60, 60
gasoline_speed = 3
gasoline_interval = 10 * 30
#ガソリン画像の読み込み
gasoline_img = pg.image.load(f"{MAIN_DIR}/fig/oil.png").convert_alpha()
gasoline_img = [pg.transform.scale(gasoline_img, (gasoline_width, gasoline_height)) for i in range(1, 11)]

# Player画像の読み込み
player_image = pg.image.load(f"{MAIN_DIR}/fig/car.png").convert_alpha()
player_image = pg.transform.scale(player_image, (player_width, player_height))
#障害物の初期設定
obstacle_width, obstacle_height = 100, 100
obstacle_speed = 5
obstacle_interval = 5 * 30  # 5秒毎に障害物を生成


# 障害物画像の読み込み
obstacle_image = pg.image.load(f"{MAIN_DIR}/fig/3.png").convert_alpha()
obstacle_images = [pg.transform.scale(obstacle_image, (obstacle_width, obstacle_height)) for i in range(1, 11)]

def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_obstacle(x, y, obstacle_img):
    screen.blit(obstacle_img, (x, y))

def draw_gasoline(x, y, gasoline_img):
    screen.blit(gasoline_img,(x,y))

def measure_time(seconds):
    start_time = time.time()
    global obstacle_speed ,obstacle_interval, gasoline_speed, gasoline_interval
    while True:
        elapsed_time = time.time() - start_time
        if (elapsed_time >= seconds):
            obstacle_speed += 0.1
            obstacle_interval -= 0.05*30
            gasoline_speed -= 0.02
            gasoline_interval += 0.02 *30
            
        time.sleep(1)
def display_text(text, position, color=(255, 255, 255)):
    font = pg.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)
def main():
    global player_x, scroll_y,player_speed
    clock = pg.time.Clock()
    gasoline_capacity = []
    obstacles = []
    score = 0
    obstacle_timer = 0
    collisions = 0  # 衝突階数
    gasoline = 100
    threading.Thread(target=measure_time, args=(10,)).start()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        player_x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * player_speed
        player_x = max(0, min(WIDTH - player_width, player_x))

        # 障害物の生成
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = -obstacle_height
            obstacle_image = random.choice(obstacle_images)
            obstacles.append([obstacle_x, obstacle_y, obstacle_image])
            obstacle_timer = 0
        
        if keys[pg.K_RETURN]:
            gasoline -= 1
            player_speed += 0.05
            

            if gasoline == 0:
                print(f"Game Over! Score:{score}")
                display_text(f"Game Over! Score: {score}", [60,200], (0, 0, 255))
                pg.display.flip()
                time.sleep(3)
                pg.quit()
                sys.exit()
        
        # 背景のスクロール
        screen.blit(background, (0, scroll_y))
        screen.blit(background, (0, scroll_y - HEIGHT))
        scroll_y = (scroll_y + scroll_speed) % HEIGHT
        # measure_time(10)

        # 障害物のスクロール
        obstacles = [[obstacle[0], obstacle[1] + obstacle_speed, obstacle[2]] for obstacle in obstacles]
        # gasolines = [[gasoline_capacity[0], gasoline_capacity[1] + gasoline_speed, gasoline_capacity[2]] for gasoline_capacity in gasolines]
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1], obstacle[2])
            if (
                    player_x < obstacle[0] + obstacle_width
                    and player_x + player_width > obstacle[0]
                    and player_y < obstacle[1] + obstacle_height
                    and player_y + player_height > obstacle[1]
            ):
                print(f"Score: {score}")
                collisions += 1
                if collisions >= 3:  # ３回衝突したら
                    print("Game Over!")
                    display_text("Game Over!", [100, 200], (255,0,0))
                    pg.display.flip()
                    time.sleep(3)
                    pg.quit()
                    sys.exit()
        # for gasoline_capacity in gasoline_capacity:
        #     draw_gasoline(gasoline_capacity[0], gasoline_capacity[1],gasoline_capacity[2])
        #     if(
        #         player_x <gasoline_capacity[0] + gasoline_width
        #         and player_x + gasoline_width > gasoline_capacity[0]
        #         and player_y < gasoline_capacity[1] + gasoline_height
        #         and player_y + gasoline_height > gasoline_capacity[1]
        #     ):
        #         gasoline += 10
        #         gasoline_capacity.remove(gasoline_capacity)
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] <= HEIGHT]
        draw_player(player_x, player_y)
        score += 1

        display_text(f"Gasoline Capacity: {gasoline}", [10, 10])
        display_text(f"Score: {score}", [10, 50])
        pg.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    main() #