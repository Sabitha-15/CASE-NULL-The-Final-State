"""Bootable Pygame shell for CASE NULL."""
import sys
import pygame

WIDTH, HEIGHT = 1100, 700
BG = (12, 17, 26)
TEXT = (226, 232, 240)
ACCENT = (210, 75, 74)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("CASE NULL | The Final State")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("consolas", 64, bold=True)
    sub_font = pygame.font.SysFont("consolas", 23)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(BG)
        w, h = screen.get_size()
        title = title_font.render("CASE NULL", True, TEXT)
        subtitle = sub_font.render("THE FINAL STATE", True, ACCENT)
        status = sub_font.render("Environment ready | Investigation engine pending", True, (148, 163, 184))
        hint = sub_font.render("ESC to exit", True, (148, 163, 184))
        screen.blit(title, title.get_rect(center=(w // 2, h // 2 - 75)))
        screen.blit(subtitle, subtitle.get_rect(center=(w // 2, h // 2)))
        screen.blit(status, status.get_rect(center=(w // 2, h // 2 + 65)))
        screen.blit(hint, hint.get_rect(center=(w // 2, h - 45)))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
