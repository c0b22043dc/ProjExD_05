import pygame as pg
import random
import sys

pg.init()

WIDTH, HEIGHT = 400, 600  # ゲームウィンドウの幅,高さ
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("車ゲーム")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_width, player_height = 50, 50
#player_x = WIDTH // 2 - player_width // 2
#player_y = HEIGHT - player_height -20
player_speed = 5

obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5


#def draw_player(x, y):
    #pg.draw.rect(screen, WHITE, [x, y, player_width, player_height])
    #rect = self.image.get_rect()
def draw_obstacle(x, y):
    pg.draw.rect(screen, RED, [x, y, obstacle_width, obstacle_height])


class Car:
    """
    プレイヤー（車）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0)
    }

    def __init__(self, player_x, player_y):
        """
        車の画像surfaceを生成する
        """
        self.image = pg.image.load("ex05/fig/car.png")  # 車画像ロード
        self.rct = self.image.get_rect()
        self.rct.center = player_x, player_y

    def update(self, key_lst: list[bool]):
        """
        押下キーに応じてプレイヤー（車）を左右に移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]


def game():
    clock = pg.time.Clock()
    car = Car(WIDTH/2, HEIGHT/2)
    global player_x

    obstacles = []
    score = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        keys = pg.key.get_pressed()
        #player_x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * player_speed

        #player_x = max(0, min(WIDTH - player_width, player_x))

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

        #draw_player(player_x, player_y)
        car.update()


        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])

        score += 1

        pg.display.flip()

        clock.tick(30)

if __name__ == "__main__":
    game()
        
