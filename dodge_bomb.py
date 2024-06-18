import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
# 入力に応じた移動方向を返す辞書DELTA
DELTA = {pg.K_UP   :(0, -5),
         pg.K_DOWN :(0, +5),
         pg.K_LEFT :(-5, 0),
         pg.K_RIGHT:(+5, 0)}
# 移動方向に応じて画像の角度を返す辞書ANGLE
ANGEL = {( 0,  0):0,
         (-5, +5):45,
         ( 0, +5):90,
         (+5, +5):135,
         (+5,  0):180,
         (+5, -5):225,
         ( 0, -5):270,
         (-5, -5):315,
         (-5,  0):360}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect):
    """
    こうかとんと爆弾が画面外に出ているか確認する関数
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def bb_change():
    """
    爆弾を10段階変化させる関数
    加速度、爆弾のイメージをリストで返す
    """
    bb_imgs = [] # 10個の爆弾を入れるリスト
    accs = [] # 10段階の速度を入れるリスト
    # 10個の爆弾と速度を入れる
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        accs.append(r)
    return accs, bb_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    # 爆弾の変更リストを受け取る
    bb_accs, bb_imgs = bb_change()
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        #衝突判定
        if kk_rct.colliderect(bb_rct):
            return 
        # こうかとんの挙動
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        mv_tup = tuple(sum_mv)
        # 移動方向によってこうかとんの向きが変わるように
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), ANGEL[mv_tup], 2.0)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #爆弾の挙動
        if check_bound(bb_rct)[0] == False:
            vx *= -1
        elif check_bound(bb_rct)[1] == False:
            vy *= -1
        # 爆弾の画像を選択する
        bb_img = bb_imgs[min(tmr//500, 9)]
        # 爆弾の速度を選択する
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
