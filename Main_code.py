import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Set up the display
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Ping Pong")
background = pygame.image.load(r"C:\Users\Rahul\Desktop\background_sky_point_83482_800x600.jpg")
effects_point = pygame.mixer.Sound(r"D:\nucleon\smb_jump-small.wav")
effects_lose = pygame.mixer.Sound(r"D:\nucleon\smb_bowserfalls.wav")
effects_pause = pygame.mixer.Sound(r"D:\nucleon\smb_pause.wav")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Orange =  (255, 165, 0)

# Ball properties
BALL_RADIUS = 20
ball_color = Orange
ball_x = DISPLAY_WIDTH // 2
ball_y = DISPLAY_HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

# Paddle properties
PADDLE_WIDTH = 180
PADDLE_HEIGHT = 40
paddle_color = WHITE
paddle_x = (DISPLAY_WIDTH - PADDLE_WIDTH) // 2
paddle_y = DISPLAY_HEIGHT - PADDLE_HEIGHT - 30
PADDLE_SPEED = 5

# Boundary
boundary = pygame.Rect(3, 590, 800, 11)

# Game variables
lives = 5
score = 0
paused = False  # Track if the game is paused or not
pause_sound_played = False  # Track if the pause sound effect has been played

# Clock
clock = pygame.time.Clock()

# Main game loop
while lives > 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:  # Pause the game when space bar is pressed
                paused = not paused
                if paused and not pause_sound_played:
                    effects_pause.play()
                    pause_sound_played = True
                elif not paused:
                    pause_sound_played = False

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            paddle_x -= PADDLE_SPEED
        if keys[K_RIGHT]:
            paddle_x += PADDLE_SPEED

        paddle_x = min(max(paddle_x, 0), DISPLAY_WIDTH - PADDLE_WIDTH)

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_x <= BALL_RADIUS or ball_x >= DISPLAY_WIDTH - BALL_RADIUS:
            ball_speed_x = -ball_speed_x
        if ball_y <= BALL_RADIUS:
            ball_speed_y = -ball_speed_y

        if (ball_x + BALL_RADIUS >= paddle_x and ball_x - BALL_RADIUS <= paddle_x + PADDLE_WIDTH and
                ball_y + BALL_RADIUS >= paddle_y and ball_y - BALL_RADIUS <= paddle_y + PADDLE_HEIGHT):
            ball_speed_y = -ball_speed_y
            score += 1
            effects_point.play()

        if ball_y >= DISPLAY_HEIGHT - BALL_RADIUS:
            lives -= 1
            effects_lose.play()
            if lives > 0:
                ball_x = DISPLAY_WIDTH // 2
                ball_y = DISPLAY_HEIGHT // 2

    display_surface.blit(background, (0, 0))  # Draw background first
    pygame.draw.rect(display_surface, BLACK, (paddle_x, paddle_y, PADDLE_WIDTH + 3, PADDLE_HEIGHT + 3))
    pygame.draw.rect(display_surface, paddle_color, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(display_surface, BLACK, (ball_x, ball_y), BALL_RADIUS + 3)
    pygame.draw.circle(display_surface, ball_color, (ball_x, ball_y), BALL_RADIUS)
    pygame.draw.rect(display_surface, WHITE, boundary)

    # Draw the score and lives
    font = pygame.font.Font(r"C:\Users\Rahul\Desktop\Metropolis-Medium.ttf", 36)
    text_surface = font.render(f"Lives: {lives}                                                Score: {score}", True, WHITE)
    display_surface.blit(text_surface, (10, 10))

    # Draw pause text if the game is paused
    if paused:
        pause_font = pygame.font.Font(r"C:\Users\Rahul\Desktop\Metropolis-Medium.ttf", 50)
        pause_text = pause_font.render( "Paused", True, WHITE)
        pause_rect = pause_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        display_surface.blit(pause_text, pause_rect)

    pygame.display.update()
    clock.tick(60)

# Game Over
print("Game Over")
pygame.quit()
sys.exit()
