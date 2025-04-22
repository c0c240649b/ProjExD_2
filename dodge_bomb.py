import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル（横、縦）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True  # 横，縦方向用の変数
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface) -> None:
    """
    引数：screen
    戻り値：なし
    """

    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, ("#000000"), (0,0,WIDTH, HEIGHT))
    pg.Surface.set_alpha(gg_img, 128)
    gg_rct = gg_img.get_rect()
    gg_rct.center = WIDTH/2,HEIGHT/2
    screen.blit(gg_img, gg_rct)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [WIDTH/2-100, HEIGHT/2-50])
  
    nn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    nn_rct = nn_img.get_rect()
    nn_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(nn_img, [WIDTH/2-140, HEIGHT/2-50])
    screen.blit(nn_img, [WIDTH/2+220, HEIGHT/2-50])

    time_sleep(5)


def time_sleep(time: int) -> None:
    pg.display.update()
    pg.time.wait(time*1000)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：拡大リストと速度リスト
    """
    
    # 加速度
    bb_accs = [a for a in range(1, 11)]

    # 拡大
    kakudais=[]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        kakudais.append(bb_img)
        bb_img.set_colorkey((0, 0, 0))
    return kakudais,bb_accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface :
    """
    引数：タプル
    戻り値：Surface
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if sum_mv[0] >0:
        if sum_mv[1] >0: 
            kk_img = pg.transform.rotate(kk_img,135)
        elif sum_mv[1] == 0:
            kk_img = pg.transform.rotate(kk_img, 180)
        else:
            kk_img = pg.transform.rotate(kk_img, -135)
    elif sum_mv[0] ==0:
        if sum_mv[1] >0: 
            kk_img = pg.transform.rotate(kk_img,90)
        elif sum_mv[1] == 0:
            kk_img = pg.transform.rotate(kk_img,0)
        else:
            kk_img = pg.transform.rotate(kk_img,-90)
    else:
        if sum_mv[1] >0: 
            kk_img = pg.transform.rotate(kk_img,45)
        elif sum_mv[1] == 0:
            kk_img = pg.transform.rotate(kk_img,0)
        else:
            kk_img = pg.transform.rotate(kk_img,-45)

    return kk_img


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5 , +5
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0]) 

        # こうかとんと爆弾が重なってたら
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右方向
                sum_mv[1] += mv[1]  # 上下方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        
        kk_img = get_kk_img((0,0))
        kk_img = get_kk_img(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        # 爆弾変化
        bb_imgs, bb_accs = init_bb_imgs()
        a = bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(vx*a, vy*a)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
