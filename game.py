import pygame as pg
pg.init()

WIDTH, HEIGHT = 700, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ping-Pong")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

paddle_WIDTH, paddle_HEIGHT = 20, 100
BALL_RADIUS = 10

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

def draw(win, paddles, ball, left_score_text, right_score_text):
    win.fill(BLACK)

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pg.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    win.blit(left_score_text, (WIDTH // 4, 10))
    win.blit(right_score_text, (3 * WIDTH // 4, 10))
    
    pg.display.update()

def handle_collision(ball, left_paddle, right_paddle, left_score_text, right_score_text):
    global LEFT_SCORE, RIGHT_SCORE

    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (left_paddle.y + left_paddle.height / 2)) / (left_paddle.height / 2) * ball.MAX_VEL
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                ball.y_vel = (ball.y - (right_paddle.y + right_paddle.height / 2)) / (right_paddle.height / 2) * ball.MAX_VEL

    if ball.x + ball.radius >= WIDTH:
        LEFT_SCORE += 1
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball.x_vel = -ball.MAX_VEL
        ball.y_vel = 0
        left_score_text = FONT.render(str(LEFT_SCORE), True, WHITE)

    if ball.x - ball.radius <= 0:
        RIGHT_SCORE += 1
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball.x_vel = ball.MAX_VEL
        ball.y_vel = 0
        right_score_text = FONT.render(str(RIGHT_SCORE), True, WHITE)

    return left_score_text, right_score_text

def handle_paddle_movement(keys, left_paddle, right_paddle, ball):
    if keys[pg.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pg.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pg.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def main():
    global LEFT_SCORE, RIGHT_SCORE, FONT

    run = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - paddle_HEIGHT // 2, paddle_WIDTH, paddle_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - paddle_WIDTH, HEIGHT // 2 - paddle_HEIGHT // 2, paddle_WIDTH, paddle_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    LEFT_SCORE = 0
    RIGHT_SCORE = 0
    FONT = pg.font.Font(None, 36)
    left_score_text = FONT.render(str(LEFT_SCORE), True, WHITE)
    right_score_text = FONT.render(str(RIGHT_SCORE), True, WHITE)

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score_text, right_score_text)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        keys = pg.key.get_pressed()

        handle_paddle_movement(keys, left_paddle, right_paddle, ball)
        ball.move()
        left_score_text, right_score_text = handle_collision(ball, left_paddle, right_paddle, left_score_text, right_score_text)

        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()
