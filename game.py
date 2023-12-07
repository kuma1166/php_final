import pygame
from pygame import mixer
import random
import math

# pygameの初期化（ゲーム開発開始の合図）
pygame.init()

# mixerの初期化
mixer.init()

# BGMのループ再生
bgm = mixer.Sound('bg.wav')
bgm.play(loops=-1)

# ゲーム画面のサイズ設定&初期化
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Invaders Game')

# プレーヤーのリソース
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# 敵キャラクターのリソース
enemyImg = pygame.image.load('enemy2.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 4, 40

# 銃弾のリソース
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4.5
bullet_state = 'ready'

# Scoreの初期値
score_value = 0

# プレーヤーの描画
def player(x, y):
    screen.blit(playerImg, (x, y))

# 敵キャラクターの描画
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# 銃弾の描画
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

# 敵キャラクター撃破の判定（True or False の判定をする）
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# ゲームの初期化
def reset_game():
    global score_value
    score_value = 0
    # プレーヤ一位置の初期化
    playerX = 370
    playerY = 480
    player(playerX, playerY)

# 制限時間の設定
clock = pygame.time.Clock()
game_time = 15  # 制限時間（秒）

# 描画の繰り返し処理
running = True
start_ticks = pygame.time.get_ticks()
while running:
    # 経過時間の計算
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > game_time:
        # 制限時間が過ぎたらリザルト画面を表示する
        screen.fill((155, 155, 155))
        text01 = font.render("Time's Up", True, (255, 255, 255))
        text02 = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
        screen.blit(text01, (screen_width / 2 - 100, screen_height / 2 - 20))
        screen.blit(text02, (screen_width / 2 - 100, screen_height / 2 + 20))
        pygame.display.flip()
        pygame.time.wait(5000)  # 5000(ms)=5(s)

        # ゲーム初期化関数の呼び出し
        reset_game()
        start_ticks = pygame.time.get_ticks()
        running = True  # ゲームループを続行する

    # 描画された瞬間に残像を黒く塗りつぶす
    screen.fill((0, 0, 0))

    # イベントループ処理
    for event in pygame.event.get():
        #ウィンドウが閉じた時にゲーム終了
        if event.type == pygame.QUIT:
            running = False
            mixer.quit()
        # キーボードを押した時の処理（移動開始・銃弾発射）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # キーボードを離した時の処理（移動ストップ）
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # プレーヤーの移動範囲の設定
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # 敵キャラクターの移動範囲の設定
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 1.5
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -1.5
        enemyY += enemyY_change

    # 敵キャラクター撃破時の処理（得点加算・敵キャラクターリロード・銃弾リロード）
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # 銃弾の移動範囲
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # 得点取得の処理
    font = pygame.font.SysFont(None, 36) # フォントの作成（Noneにすると初期値のfreesansbold.ttf）
    score = font.render(f"Score :  {str(score_value)}" , True, (255,255,255)) # テキストを描画したSurfaceの作成
    screen.blit(score, (20,50))

    # キャラクターの描画位置
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    # 画面を更新し続ける処理（ゲームの最後にこの処理を忘れずにする！）
    pygame.display.update()
