import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont('Arial', 32)
large_font = pygame.font.SysFont('Arial', 50)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10

difficulty = "Medium"
paddle_speed = 10
ball_x_speed = 4
ball_y_speed = -4
score = 0
level = 1
lives = 3
paused = False
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

def create_bricks():
    bricks = []
    rows, cols = 5, 8
    brick_width, brick_height = 70, 30
    for row in range(rows):
        brick_row = []
        for col in range(cols):
            x = col * (brick_width + 10) + 50
            y = row * (brick_height + 10) + 50
            brick_row.append(pygame.Rect(x, y, brick_width, brick_height))
        bricks.append(brick_row)
    return bricks

bricks = create_bricks()

def set_difficulty(level):
    global paddle_speed, ball_x_speed, ball_y_speed, PADDLE_WIDTH, PADDLE_HEIGHT
    if level == "Easy":
        paddle_speed, ball_x_speed, ball_y_speed = 12, 3, -3
        PADDLE_WIDTH = 120
        PADDLE_HEIGHT = 30
    elif level == "Medium":
        paddle_speed, ball_x_speed, ball_y_speed = 10, 4, -4
        PADDLE_WIDTH = 100
        PADDLE_HEIGHT = 20
    elif level == "Hard":
        paddle_speed, ball_x_speed, ball_y_speed = 8, 5, -5
        PADDLE_WIDTH = 80
        PADDLE_HEIGHT = 15

def draw_gradient_background():
    for y in range(SCREEN_HEIGHT):
        color_value = int(255 * (y / SCREEN_HEIGHT))
        pygame.draw.line(screen, (color_value, 100, 255 - color_value), (0, y), (SCREEN_WIDTH, y))

def start_menu():
    global difficulty
    while True:
        screen.fill(BLACK)
        title_text = large_font.render("Brick Breaker", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        options = [
            ("Press Space to Start", 0),
            ("Press Q to Quit", 50),
            ("Press 1 for Easy", 100),
            ("Press 2 for Medium", 150),
            ("Press 3 for Hard", 200)
        ]
        for text, offset in options:
            rendered_text = font.render(text, True, WHITE)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, SCREEN_HEIGHT // 2 + offset))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Start the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    difficulty = "Easy"
                    set_difficulty(difficulty)
                    return True  # Start the game
                elif event.key == pygame.K_2:
                    difficulty = "Medium"
                    set_difficulty(difficulty)
                    return True  # Start the game
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    set_difficulty(difficulty)
                    return True  # Start the game


def reset_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_x_speed, ball_y_speed, score, level, lives, bricks
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    score = 0
    level = 1
    lives = 3
    bricks = create_bricks()
    set_difficulty(difficulty)

def game_over():
    global score
    while True:
        screen.fill(BLACK)
        game_over_text = large_font.render(f"Game Over! Score: {score}", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

        instructions = [
            ("Press R to Restart", 0),
            ("Press Q to Quit", 50),
            ("Press P to Pause/Resume", 100)
        ]
        for text, offset in instructions:
            rendered_text = font.render(text, True, WHITE)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, SCREEN_HEIGHT // 2 + offset))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    start_menu()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def pause_game():
    global paused
    paused = True
    pause_text = large_font.render("Paused - Press P to Resume", True, WHITE)
    while paused:
        screen.fill(BLACK)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
def check_ball_brick_collision():
    global score
    for row in bricks:
        for brick in row:
            ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
            if brick.colliderect(ball_rect):
                row.remove(brick)
                global ball_y_speed
                ball_y_speed = -ball_y_speed
                score += 10
                return


def check_ball_paddle_collision():
    global ball_x_speed, ball_y_speed
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    if ball_rect.colliderect(paddle_rect):
        ball_y_speed = -ball_y_speed

        ball_center = ball_x
        paddle_center = paddle_x + PADDLE_WIDTH // 2
        distance_from_center = (ball_center - paddle_center) / (PADDLE_WIDTH // 2)
        ball_x_speed += distance_from_center * 3

def game_loop():
    global paddle_x, paddle_y, ball_x, ball_y, ball_x_speed, ball_y_speed, lives, score, level, bricks
    while True:
        screen.fill(BLACK)
        draw_gradient_background()

        if not any(bricks):
            level += 1
            bricks = create_bricks()
            set_difficulty(difficulty)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        ball_x += ball_x_speed
        ball_y += ball_y_speed

        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_x_speed = -ball_x_speed
        if ball_y <= BALL_RADIUS:
            ball_y_speed = -ball_y_speed
        elif ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
            lives -= 1
            if lives == 0:
                game_over()
                reset_game()
                start_menu()
                return
            else:
                ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                ball_x_speed = 4
                ball_y_speed = -4

        check_ball_paddle_collision()
        check_ball_brick_collision()

        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

        for row in bricks:
            for brick in row:
                pygame.draw.rect(screen, GREEN, brick)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        pygame.display.update()
        pygame.time.Clock().tick(60)

start_menu()
game_loop()

pygame.quit()
quit()
