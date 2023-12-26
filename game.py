import os
import pygame as pg
import time
import random
import pygame
import sys
import random

# 初期化
pygame.init()


WIDTH = 400  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# 背景の設定
background = pg.image.load(f"ex05/fig/way.png").convert_alpha()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
scroll_speed = 5
scroll_y = 0

player_speed = 5


#障害物の初期設定
obstacle_width, obstacle_height = 50, 50
obstacle_speed = 5
obstacle_interval = 5 * 30  # ５秒毎に障害物を生成


# 障害物画像の読み込み
obstacle_image = pg.image.load(f"ex05/fig/3.png").convert_alpha()
obstacle_images = [pg.transform.scale(obstacle_image, (obstacle_width, obstacle_height)) for i in range(1, 11)]
obstacle_rct = obstacle_image.get_rect()



def draw_obstacle(x, y, obstacle_img,screen):
    screen.blit(obstacle_img, (x, y))


def check_bound(obj_rct: pg.Rect):
    """
    オブジェクトが画面内か判定する関数
    引数：なんらかの画像SurfaceのRect（主に車）
    戻り値：横方向のはみ出し判定の結果（画面内：True/画面外：False）
    """
    yoko = True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    return yoko

class Car:
    """
    車（プレイヤー）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_RIGHT:+player_speed,
        pg.K_LEFT:-player_speed
    }

    def __init__(self):
        """
        車（プレイヤー）画像Surfaceを生成する
        """
        super().__init__()
        self.img = pg.transform.rotozoom(pg.image.load("ex05/fig/car.png"),0,0.17)
        self.rct = self.img.get_rect()
        self.rct.center = 200, 530  # プレイヤーの初期位置

    def update(self,screen: pg.Surface, keys):
        """
        押下キーに応じて車（プレイヤー）を移動させる
        引数1 screen：画面Surface
        引数2 keys：押下キーのリスト
        """
        sum_mv = 0
        for k , mv in __class__.delta.items():
            if keys[k]:
                sum_mv += mv
        self.rct.move_ip(sum_mv,0)
        if check_bound(self.rct) != True:
            self.rct.move_ip(-sum_mv,0)
        screen.blit(self.img, self.rct)

def main():
    global scroll_y
    pg.display.set_caption("車ゲーム")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    car = Car()  # 車（プレイヤー）のインスタンス生成
    clock =pg.time.Clock()


    obstacles = []
    score = 0
    obstacle_timer = 0
    collisions = 0  # 衝突階数

    while True:
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 障害物の生成
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = -obstacle_height
            obstacle_image = random.choice(obstacle_images)
            obstacles.append([obstacle_x, obstacle_y, obstacle_image])
            obstacle_timer = 0

        # 背景のスクロール
        screen.blit(background, (0, scroll_y))
        screen.blit(background, (0, scroll_y - HEIGHT))
        scroll_y = (scroll_y + scroll_speed) % HEIGHT

        # 障害物のスクロール
        obstacles = [[obstacle[0], obstacle[1] + obstacle_speed, obstacle[2]] for obstacle in obstacles]

        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1], obstacle[2],screen)
            #もし車と障害物が接触していたら
            if car.rct.colliderect(obstacle_rct):
                

            #if (
                    #player_x < obstacle[0] + obstacle_width
                    #and player_x + player_width > obstacle[0]
                    #and player_y < obstacle[1] + obstacle_height
                    #and player_y + player_height > obstacle[1]
            #):
                print(f"Score: {score}")
                collisions += 1
                if collisions >= 3:  # ３回衝突したら
                    print("Game Over!")
                    return

        obstacles = [obstacle for obstacle in obstacles if obstacle[1] <= HEIGHT]

        car.update(screen, keys)

        score += 1

        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    # フレームレートの制御
    clock.tick(30)
    

