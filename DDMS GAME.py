import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBSTACLE_SIZE = 50
COIN_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple 2D Game')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10
player_speed = 5

obstacles = []
coins = []
score = 0

# Font for score
font = pygame.font.SysFont('Arial', 30)

# Function to draw the player
def draw_player(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, PLAYER_SIZE, PLAYER_SIZE))

# Function to draw an obstacle
def draw_obstacle(x, y):
    pygame.draw.rect(screen, RED, (x, y, OBSTACLE_SIZE, OBSTACLE_SIZE))

# Function to draw a coin
def draw_coin(x, y):
    pygame.draw.circle(screen, YELLOW, (x + COIN_SIZE // 2, y + COIN_SIZE // 2), COIN_SIZE // 2)

# Function to handle obstacle movement
def move_obstacles():
    global score
    for obstacle in obstacles:
        obstacle['y'] += 5  # Move the obstacle down
        if obstacle['y'] > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            obstacles.append({'x': random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE), 'y': -OBSTACLE_SIZE})
        # Check if the player collides with an obstacle
        if player_x < obstacle['x'] + OBSTACLE_SIZE and player_x + PLAYER_SIZE > obstacle['x'] and player_y < obstacle['y'] + OBSTACLE_SIZE and player_y + PLAYER_SIZE > obstacle['y']:
            return True
    return False

# Function to handle coin movement
def move_coins():
    global score
    for coin in coins:
        coin['y'] += 3  # Move the coin down
        if coin['y'] > SCREEN_HEIGHT:
            coins.remove(coin)
            coins.append({'x': random.randint(0, SCREEN_WIDTH - COIN_SIZE), 'y': -COIN_SIZE})
        # Check if the player collects the coin
        if player_x < coin['x'] + COIN_SIZE and player_x + PLAYER_SIZE > coin['x'] and player_y < coin['y'] + COIN_SIZE and player_y + PLAYER_SIZE > coin['y']:
            coins.remove(coin)
            score += 1
            coins.append({'x': random.randint(0, SCREEN_WIDTH - COIN_SIZE), 'y': -COIN_SIZE})

# Main game loop
def game_loop():
    global player_x, player_y, score
    run_game = True
    while run_game:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
            player_x += player_speed

        # Move obstacles and coins
        if move_obstacles():
            game_over()

        move_coins()

        # Draw the player, obstacles, and coins
        draw_player(player_x, player_y)
        for obstacle in obstacles:
            draw_obstacle(obstacle['x'], obstacle['y'])
        for coin in coins:
            draw_coin(coin['x'], coin['y'])

        # Display the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Control the frame rate
        clock.tick(60)

# Game over screen
def game_over():
    global score
    screen.fill(WHITE)
    game_over_text = font.render("GAME OVER!", True, RED)
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Spawn initial obstacles and coins
for _ in range(5):
    obstacles.append({'x': random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE), 'y': -OBSTACLE_SIZE})
for _ in range(3):
    coins.append({'x': random.randint(0, SCREEN_WIDTH - COIN_SIZE), 'y': -COIN_SIZE})

# Start the game loop
game_loop()
