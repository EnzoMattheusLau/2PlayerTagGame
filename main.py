import pygame
import sys
import time
import random

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 300

# Colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Player properties
PLAYER_SIZE = 25
PLAYER_SPEED = 0.42

# Obstacle properties
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
NUM_OBSTACLES = 10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2-Player Tag Game")


def show_start_menu():
  font = pygame.font.Font(None, 36)
  instructions_text = font.render("Press any key to start the game!", True,
                                  (0, 0, 0))

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        return

    screen.fill(WHITE)
    screen.blit(instructions_text,
                (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2,
                 SCREEN_HEIGHT // 2))
    pygame.display.update()


def draw_it_indicator(player_x, player_y, is_it):
  indicator_radius = 8

  if is_it:
    pygame.draw.circle(screen, GREEN,
                       (player_x, player_y - PLAYER_SIZE // 2 - 10),
                       indicator_radius)
  else:
    pygame.draw.circle(screen, GREEN,
                       (player_x, player_y - PLAYER_SIZE // 2 - 10),
                       indicator_radius, 2)


def game_over(winner):
  font = pygame.font.Font(None, 48)
  if winner == 1:
    winner_text = font.render("Player 1 wins!", True, (0, 0, 0))
  else:
    winner_text = font.render("Player 2 wins!", True, (0, 0, 0))

  restart_button = pygame.Rect(100, 100, 300, 50)
  quit_button = pygame.Rect(100, 175, 300, 50)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if restart_button.collidepoint(mouse_x, mouse_y):
          main()  # Restart the game
        elif quit_button.collidepoint(mouse_x, mouse_y):
          pygame.quit()
          sys.exit()

    screen.fill(WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 100))

    # Draw restart button
    pygame.draw.rect(screen, GREEN, restart_button)
    restart_text = font.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, (190, 110))

    # Draw quit button
    pygame.draw.rect(screen, GREEN, quit_button)
    quit_text = font.render("Quit", True, (0, 0, 0))
    screen.blit(quit_text, (210, 185))

    pygame.display.update()


def generate_obstacles():
  obstacles = []
  for _ in range(NUM_OBSTACLES):
    while True:
      x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
      y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_HEIGHT)

      # Check for collision with player 1 spawn position
      player1_rect = pygame.Rect(player1_x, player1_y, PLAYER_SIZE,
                                 PLAYER_SIZE)
      if player1_rect.colliderect(
          pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)):
        continue

      # Check for collision with player 2 spawn position
      player2_rect = pygame.Rect(player2_x, player2_y, PLAYER_SIZE,
                                 PLAYER_SIZE)
      if player2_rect.colliderect(
          pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)):
        continue

      # Randomly choose the shape of the obstacle
      obstacle_shape = random.choice(
        ["rectangle", "square", "vertical_rectangle"])

      if obstacle_shape == "rectangle":
        obstacles.append(pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
      elif obstacle_shape == "square":
        obstacles.append(pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_WIDTH))
      elif obstacle_shape == "vertical_rectangle":
        obstacles.append(
          pygame.Rect(x, y, OBSTACLE_WIDTH // 2, OBSTACLE_HEIGHT))

      break

  return obstacles


def draw_obstacles(obstacles):
  for obstacle in obstacles:
    pygame.draw.rect(screen, (128, 128, 128), obstacle)


def check_collision_with_obstacles(rect, obstacles):
  for obstacle in obstacles:
    if rect.colliderect(obstacle):
      return True
  return False


def main():
  global player1_x, player1_y, player2_x, player2_y

  show_start_menu()

  # Player 1 initial position and velocity
  player1_x, player1_y = 100, SCREEN_HEIGHT // 2
  player1_vel_x, player1_vel_y = 0, 0

  # Player 2 initial position and velocity
  player2_x, player2_y = SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2
  player2_vel_x, player2_vel_y = 0, 0

  # Timer setup
  start_time = time.time()
  time_remaining = 60
  last_tag_time = start_time  # Time when last tag happened
  tag_cooldown = 1.5  # Cooldown time before the "it" indicator can be passed

  # Player roles
  is_player1_it = True

  # Generate obstacles
  obstacles = generate_obstacles()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      # Player 1 controls
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          player1_vel_y = -PLAYER_SPEED
        elif event.key == pygame.K_s:
          player1_vel_y = PLAYER_SPEED
        elif event.key == pygame.K_a:
          player1_vel_x = -PLAYER_SPEED
        elif event.key == pygame.K_d:
          player1_vel_x = PLAYER_SPEED
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w or event.key == pygame.K_s:
          player1_vel_y = 0
        elif event.key == pygame.K_a or event.key == pygame.K_d:
          player1_vel_x = 0

      # Player 2 controls
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          player2_vel_y = -PLAYER_SPEED
        elif event.key == pygame.K_DOWN:
          player2_vel_y = PLAYER_SPEED
        elif event.key == pygame.K_LEFT:
          player2_vel_x = -PLAYER_SPEED
        elif event.key == pygame.K_RIGHT:
          player2_vel_x = PLAYER_SPEED
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          player2_vel_y = 0
        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          player2_vel_x = 0

    # Update player positions
    player1_x += player1_vel_x
    player1_y += player1_vel_y

    player2_x += player2_vel_x
    player2_y += player2_vel_y

    # Check collision with obstacles for player 1
    player1_rect = pygame.Rect(player1_x, player1_y, PLAYER_SIZE, PLAYER_SIZE)
    if check_collision_with_obstacles(player1_rect, obstacles):
      player1_x -= player1_vel_x
      player1_y -= player1_vel_y

    # Check collision with obstacles for player 2
    player2_rect = pygame.Rect(player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE)
    if check_collision_with_obstacles(player2_rect, obstacles):
      player2_x -= player2_vel_x
      player2_y -= player2_vel_y

    # Check for collisions (tagging) and apply cooldown
    if time.time() - last_tag_time > tag_cooldown:
      if abs(player1_x -
             player2_x) < PLAYER_SIZE - 2 and abs(player1_y -
                                                  player2_y) < PLAYER_SIZE - 2:
        if is_player1_it:
          is_player1_it = False
        else:
          is_player1_it = True
        last_tag_time = time.time()

    # Screen boundary check
    player1_x = max(0, min(player1_x, SCREEN_WIDTH - PLAYER_SIZE))
    player1_y = max(0, min(player1_y, SCREEN_HEIGHT - PLAYER_SIZE))

    player2_x = max(0, min(player2_x, SCREEN_WIDTH - PLAYER_SIZE))
    player2_y = max(0, min(player2_y, SCREEN_HEIGHT - PLAYER_SIZE))

    # Timer update
    elapsed_time = time.time() - start_time
    time_remaining = max(0, 60 - int(elapsed_time))

    # Clear the screen
    screen.fill(WHITE)

    # Draw obstacles
    draw_obstacles(obstacles)

    # Draw players on the screen
    pygame.draw.rect(screen, (255, 0, 0),
                     (player1_x, player1_y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, (0, 0, 255),
                     (player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE))

    # Draw it indicator
    draw_it_indicator(player1_x + PLAYER_SIZE // 2,
                      player1_y + PLAYER_SIZE // 2, is_player1_it)
    draw_it_indicator(player2_x + PLAYER_SIZE // 2,
                      player2_y + PLAYER_SIZE // 2, not is_player1_it)

    # Display time remaining
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time remaining: {time_remaining}", True,
                             (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    # Check if time is up
    if time_remaining <= 0:
      if is_player1_it:
        game_over(2)  # Player 2 wins
      else:
        game_over(1)  # Player 1 wins

    # Update the display
    pygame.display.update()


if __name__ == "__main__":
  main()
