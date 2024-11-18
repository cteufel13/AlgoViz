import pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Game")

# Set up player
player = pygame.Rect(375, 500, 50, 50)  # A 50x50 square player

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    # Fill the screen with black and draw the player
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 128, 255), player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
