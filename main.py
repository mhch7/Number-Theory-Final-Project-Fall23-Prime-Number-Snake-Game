import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize fonts
font = pygame.font.SysFont(None, 40)

# Function to display text on the screen
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to reset the game
def reset_game():
    global snake, snake_direction, apple, score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2

game_state = START
running = True
clock = pygame.time.Clock()

# Game variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

#Game Loop
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = PLAYING
                reset_game()

        if game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = PLAYING
                reset_game()

    if game_state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if keys[pygame.K_DOWN] and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if keys[pygame.K_LEFT] and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if keys[pygame.K_RIGHT] and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # Update snake position and speed based on whether score is a prime number
        if is_prime(score):
            snake_speed = 2  # Increase the snake's speed when the score is a prime number
        else:
            snake_speed = 1  # Maintain the default speed

        # Update snake position based on speed
        if snake_direction == 'UP':
            new_head = (snake[0][0], snake[0][1] - snake_speed)
        elif snake_direction == 'DOWN':
            new_head = (snake[0][0], snake[0][1] + snake_speed)
        elif snake_direction == 'LEFT':
            new_head = (snake[0][0] - snake_speed, snake[0][1])
        elif snake_direction == 'RIGHT':
            new_head = (snake[0][0] + snake_speed, snake[0][1])

        # Check collision with itself or boundaries
        if (new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_state = GAME_OVER

        # Update snake
        snake.insert(0, new_head)

        # Check collision with apple
        if new_head == apple:
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1
        else:
            snake.pop()

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw apple
        pygame.draw.rect(screen, RED, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Display score
        display_text(f"Score: {score}", WHITE, 10, 10)

    if game_state == START:
        display_text("Press SPACE to start", WHITE, 220, 250)

    if game_state == GAME_OVER:
        display_text("Game Over. Press SPACE to retry", WHITE, 180, 250)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
