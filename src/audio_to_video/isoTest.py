import sys
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_SIZE = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def draw_tile_iso(
    surface: pygame.Surface,
    gx: int,
    gy: int,
    color: tuple[int, int, int]
) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy)

    # Center the grid on screen
    cx = iso_x + SCREEN_WIDTH // 2
    cy = iso_y + 200

    # Calculate the 4 corners of the diamond
    top = (cx, cy - TILE_HEIGHT / 2)
    right = (cx + TILE_WIDTH / 2, cy)
    bottom = (cx, cy + TILE_HEIGHT / 2)
    left = (cx - TILE_WIDTH / 2, cy)

    pygame.draw.polygon(surface, color, [top, right, bottom, left])
    pygame.draw.polygon(surface, (0, 0, 0), [top, right, bottom, left], 1)  # border

TILE_WIDTH = 64
TILE_HEIGHT = 32

def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    """
    Convert grid coordinates into isometric coordinates
    """
    x = (gx - gy) * (TILE_WIDTH / 2)
    y = (gx + gy) * (TILE_HEIGHT / 2)
    return int(x), int(y)

def screen_to_grid(
    screen_x: int,
    screen_y: int
) -> tuple[int, int]:
    """
    Convert screen coordinates to grid coordinates (isometric)
    """
    # Remove the centering offset
    x = screen_x - SCREEN_WIDTH // 2
    y = screen_y - 200

    # Reverse the isometric projection formula
    gx = (y / (TILE_HEIGHT / 2) + x / (TILE_WIDTH / 2)) / 2
    gy = (y / (TILE_HEIGHT / 2) - x / (TILE_WIDTH / 2)) / 2

    return int(gx), int(gy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # Draw all tiles
    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            draw_tile_iso(screen, gx, gy, (100, 150, 100))

    #updates the screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()