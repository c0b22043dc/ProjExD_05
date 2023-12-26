import os
import pygame as pg
import random
import sys

WIDTH = 400  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#player_width, player_height = 50, 50
#player_x = WIDTH // 2 - player_width // 2
#player_y = HEIGHT - player_height -20
#player_speed = 5

#obstacle_width, obstacle_height = 50, 50
#obstacle_speed = 5

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
        pg.K_RIGHT:+5,
        pg.K_LEFT:-5
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
    pg.display.set_caption("車ゲーム")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    car = Car()  # 車（プレイヤー）のインスタンス生成
    clock =pg.time.Clock()

    obstacles = []
    score = 0

    while True:
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        #if random.randint(1, 10) == 1:
            #obstacle_x = random.randint(0, WIDTH - obstacle_width)
            #obstacle_y = -obstacle_height
            #obstacles.append([obstacle_x, obstacle_y])

        #for obstacle in obstacles:
            #obstacle[1] +- obstacle_speed
            #if(
                #player_x < obstacle[0] + obstacle_width
                #and player_x + player_width > obstacle[0]
                #and player_y < obstacle[1] + obstacle_height
                #and player_y + player_height > obstacle[1]
            #):
                #print(f"Game Over! Score: {score}")

        screen.fill(BLACK)  # 仮の背景
        car.update(screen, keys)

        #for obstacle in obstacles:
            #draw_obstacle(obstacle[0], obstacle[1])

        score += 1

        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()