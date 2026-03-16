"""
Web entrypoint for pygbag/itch.io HTML5 builds.
"""

import asyncio
import traceback

import pygame
from pondsolver.game import async_main


async def show_error_screen(message: str):
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("PondSolver Error")
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)
    lines = [line for line in message.splitlines() if line] or ["Unknown error"]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.KEYUP, pygame.MOUSEBUTTONDOWN):
                running = False

        screen.fill((20, 24, 32))
        title = font.render("PondSolver failed to start", True, (255, 210, 120))
        hint = small_font.render(
            "Press any key or click to close this screen.",
            True,
            (210, 210, 210),
        )
        screen.blit(title, (24, 24))
        screen.blit(hint, (24, 58))

        y = 110
        for line in lines[:18]:
            rendered = small_font.render(line[:110], True, (240, 240, 240))
            screen.blit(rendered, (24, y))
            y += 26

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


async def main():
    try:
        await async_main()
    except Exception:
        await show_error_screen(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
