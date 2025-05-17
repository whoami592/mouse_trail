import pygame
import asyncio
import platform
from collections import deque

# Initialize Pygame
def setup():
    global screen, trail
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mouse Trail")
    trail = deque(maxlen=50)  # Store up to 50 trail points
    return screen, trail

# Update game state
def update_loop():
    global screen, trail
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

    # Get current mouse position
    mouse_pos = pygame.mouse.get_pos()
    trail.append(mouse_pos)  # Add to trail

    # Clear screen
    screen.fill((0, 0, 0))  # Black background

    # Draw trail
    for i, pos in enumerate(trail):
        # Fade effect: decrease radius and change color based on position in trail
        radius = int(10 * (1 - i / len(trail)))
        if radius > 0:
            alpha = int(255 * (1 - i / len(trail)))
            color = (255, 100, 100, alpha)  # Red with fading alpha
            # Create a surface for the circle
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, color, (radius, radius), radius)
            screen.blit(circle_surface, (pos[0] - radius, pos[1] - radius))

    pygame.display.flip()
    return True

# Main game loop
async def main():
    setup()
    while True:
        if not update_loop():
            break
        await asyncio.sleep(1.0 / 60)  # 60 FPS

# Run the game
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())