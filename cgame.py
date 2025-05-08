import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player car
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 100
player_speed = 5

# Obstacle (enemy car)
obstacle_size = 50
obstacle_x = random.randint(0, WIDTH - obstacle_size)
obstacle_y = -obstacle_size
obstacle_speed = 5

# Score
score = 0
font = pygame.font.SysFont("arial", 30)

# Clock for frame rate
FPS = 60
clock = pygame.time.Clock()

def setup():
    global player_x, player_y, obstacle_x, obstacle_y, score
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 100
    obstacle_x = random.randint(0, WIDTH - obstacle_size)
    obstacle_y = -obstacle_size
    score = 0

def update_loop():
    global player_x, obstacle_x, obstacle_y, score, obstacle_speed

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Move obstacle
    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = -obstacle_size
        obstacle_x = random.randint(0, WIDTH - obstacle_size)
        score += 10
        obstacle_speed += 0.2  # Increase difficulty

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size)
    if player_rect.colliderect(obstacle_rect):
        game_over()

    # Draw
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, WHITE, (obstacle_x, obstacle_y, obstacle_size, obstacle_size))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

def game_over():
    global score
    game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    setup()

async def main():
    setup()
    while True:
        update_loop()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())